import time
import requests
from eigensdk.crypto.bls.attestation import (
    g1_to_tupple,
    g2_to_tupple,
    G1Point,
    G2Point,
    Signature,
)
from web3 import Web3

from local_setting import (
    INFURA_KEY,
    CHAIN_ID,
    ACCOUNT_ADDRESS,
)
from setting import (
    SIMPLE_EIGEN_ADDRESS,
    SIMPLE_EIGEN_ABI,
    AGGREGATOR_DELAY,
)
from utils import (
    delete_operators,
    upsert_operators,
    query_subgraph,
)

sepolia_w3 = Web3(Web3.HTTPProvider(f"https://sepolia.infura.io/v3/{INFURA_KEY}"))
holesky_w3 = Web3(Web3.HTTPProvider(f"https://holesky.infura.io/v3/{INFURA_KEY}"))
eigen_contract = sepolia_w3.eth.contract(
    address=SIMPLE_EIGEN_ADDRESS, abi=SIMPLE_EIGEN_ABI
)

last_signature_nonce = eigen_contract.functions.lastNonce().call()
last_nonce = last_signature_nonce[0]
lats_block = last_signature_nonce[1]

operators = {}
operators_info = eigen_contract.functions.getOperators(0, 0).call()
for record in operators_info:
    op = {
        "opAddress": record[0],
        "socket": record[1],
        "stakedAmount": record[2],
        "pubG1": record[3],
        "pubG2": record[4],
    }
    operators[record[0]] = op

print("operators:", operators.keys())

current_block = holesky_w3.eth.block_number - AGGREGATOR_DELAY

while True:
    print(f"checking blocks from {lats_block} to {current_block}")
    changes = query_subgraph(current_block, lats_block)
    for record in changes:
        op_address: str = Web3.to_checksum_address(record["id"])
        op = {
            "opAddress": op_address,
            "socket": record["socket"],
            "stakedAmount": int(record["stake"]),
            "pubG1": (int(record["pubkeyG1_X"]), int(record["pubkeyG1_Y"])),
            "pubG2": (
                [int(i) for i in record["pubkeyG2_X"]],
                [int(i) for i in record["pubkeyG2_Y"]],
            ),
        }

        registered: bool = record["registered"]
        print("Last used signature nonce:", last_nonce)
        last_nonce += 1
        signature_nonce = {
            "nonce": last_nonce,
            "blockNumber": int(record["blockNumber"]),
            "txNumber": int(record["transactionHash"], 16),
            "eventNumber": int(record["logIndex"]),
        }
        signature_timestamp = int(record["blockTimestamp"])
        aggregatedPubG1 = G1Point(0, 0)
        aggregatedPubG2 = G2Point(0, 0, 0, 0)
        aggregatedSignature = Signature(0, 0)

        non_signers = []

        # Fetch signature from API
        for operator_address, operator in operators.items():
            op_socket = operator["socket"]
            pubG1 = G1Point(*operator["pubG1"])
            pubG2 = G2Point(*operator["pubG2"][0], *operator["pubG2"][1])
            aggregatedPubG1.setStr((aggregatedPubG1 + pubG1).getStr(10))
            aggregatedPubG2.setStr((aggregatedPubG2 + pubG2).getStr(10))

            print(
                f"For {last_nonce} asking {operator_address} from {op_socket} for signature."
            )
            response = requests.get(f"{op_socket}/get-signature/{last_nonce}")
            if response.status_code == 200:
                signature_data = response.json()
                single_signature = Signature(*signature_data["signature"])
                aggregatedSignature.setStr(
                    (aggregatedSignature + single_signature).getStr(10)
                )
            else:
                print(
                    f"Error fetching signature for nonce {last_nonce}: {response.text}"
                )
                non_signers.append(
                    eigen_contract.functions.address2Index(operator_address).call()
                )
                continue

        signature = {
            "apkG1": g1_to_tupple(aggregatedPubG1),
            "apkG2": g2_to_tupple(aggregatedPubG2),
            "sigma": g1_to_tupple(aggregatedSignature),
            "nonSignerIndices": non_signers,
        }

        if registered is True:
            # Add Operator
            print(
                f"For {last_nonce}, the signatures are aggregated and sending upserting transaction."
            )
            upsert_operators(
                sepolia_w3, ACCOUNT_ADDRESS, op, signature, signature_nonce, CHAIN_ID
            )
            operators[op_address] = op

        elif registered is False:
            # Delete Operator
            print(
                f"For {last_nonce}, the signatures are aggregated and sending deleting transaction."
            )
            delete_operators(
                sepolia_w3,
                ACCOUNT_ADDRESS,
                op_address,
                signature,
                signature_nonce,
                CHAIN_ID,
            )
            del operators[op_address]

    time.sleep(10)
    lats_block = current_block
    current_block = holesky_w3.eth.block_number - AGGREGATOR_DELAY
