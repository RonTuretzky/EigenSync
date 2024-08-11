import time
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from eigensdk.crypto.bls.attestation import g1_to_tupple
from web3 import Web3

from local_setting import INFURA_KEY, KEY_PAIR, PORT
from setting import OPERATOR_REGISTRY_ADDRESS, OPERATOR_REGISTRY_ABI, Action
from utils import query_subgraph

app = FastAPI()

signatures = {}


class NonceRequest(BaseModel):
    nonce: int


@app.get("/get-signature/{nonce}")
def get_signature(nonce: int):
    if nonce in signatures:
        return {"nonce": nonce, "signature": g1_to_tupple(signatures[nonce])}
    else:
        raise HTTPException(status_code=404, detail="Signature not found")


def main_loop():
    sepolia_w3 = Web3(Web3.HTTPProvider(f"https://sepolia.infura.io/v3/{INFURA_KEY}"))
    holesky_w3 = Web3(Web3.HTTPProvider(f"https://holesky.infura.io/v3/{INFURA_KEY}"))
    eigen_contract = sepolia_w3.eth.contract(
        address=OPERATOR_REGISTRY_ADDRESS, abi=OPERATOR_REGISTRY_ABI
    )

    last_signature_nonce = eigen_contract.functions.lastNonce().call()
    last_nonce = last_signature_nonce[0]
    lats_block = last_signature_nonce[1]

    current_block = holesky_w3.eth.block_number
    while True:
        changes = query_subgraph(current_block, lats_block)
        for record in changes:
            op_address: str = Web3.to_checksum_address(record["id"])
            registered: bool = record["registered"]
            last_nonce += 1
            if registered is True:
                # Update Operator
                msgHash = Web3.solidity_keccak(
                    [
                        "uint8",
                        "address",
                        "string",
                        "uint256",
                        "uint256",
                        "uint256",
                        "uint256[]",
                        "uint256[]",
                        "uint256",
                        "uint256",
                        "uint256",
                        "uint256",
                    ],
                    [
                        Action["UPSERT"],
                        op_address,
                        record["socket"],
                        int(record["stake"]),
                        int(record["pubkeyG1_X"]),
                        int(record["pubkeyG1_Y"]),
                        [int(i) for i in record["pubkeyG2_X"]],
                        [int(i) for i in record["pubkeyG2_Y"]],
                        last_nonce,
                        int(record["blockNumber"]),
                        int(record["transactionHash"], 16),
                        int(record["logIndex"]),
                    ],
                )

            elif registered is False:
                # Delete Operator
                msgHash = Web3.solidity_keccak(
                    ["uint8", "address", "uint256", "uint256", "uint256", "uint256"],
                    [
                        int(Action["DELETE"]),
                        op_address,
                        int(last_nonce),
                        int(record["blockNumber"]),
                        int(record["transactionHash"], 16),
                        int(record["logIndex"]),
                    ],
                )

            sign = KEY_PAIR.sign_message(msgHash)
            signatures[last_nonce] = sign

        print(
            lats_block,
            current_block,
            "\nsignatures",
            {key: g1_to_tupple(value) for key, value in signatures.items()},
        )

        time.sleep(30)
        lats_block = current_block
        current_block = holesky_w3.eth.block_number


if __name__ == "__main__":
    import threading

    main_thread = threading.Thread(target=main_loop)
    main_thread.start()
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=PORT)
