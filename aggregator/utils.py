import time

import requests

from settings.local_setting import PRIVATE_KEY
from settings.setting import SIMPLE_EIGEN_ADDRESS, SIMPLE_EIGEN_ABI, GAS, SUBGRAPH_URL


def query_subgraph(number: int, number_gte: int):
    query = f"""
    query MyQuery {{
      operators(
        block: {{number: {number}}}
        where: {{_change_block: {{number_gte: {number_gte}}}}}
        orderBy: blockNumber
      ) {{
        blockNumber
        blockTimestamp
        id
        logIndex
        operatorId
        pubkeyG1_X
        pubkeyG1_Y
        pubkeyG2_X
        pubkeyG2_Y
        registered
        socket
        stake
        transactionHash
      }}
    }}"""
    payload = {"query": query}
    response = requests.post(SUBGRAPH_URL, json=payload)
    if response.status_code == 200:
        data = response.json()
        registrations = data["data"]["operators"]
        return registrations
    else:
        print(f"Error: {response.status_code}")
        return response.text


def add_operators(w3, account, op, signature, signature_nonce, chain_id):
    eigen_contract = w3.eth.contract(address=SIMPLE_EIGEN_ADDRESS, abi=SIMPLE_EIGEN_ABI)

    # Prepare transaction
    nonce = w3.eth.get_transaction_count(account)
    tx = eigen_contract.functions.addOperatorSig(
        op, signature, signature_nonce
    ).build_transaction(
        {
            "chainId": chain_id,  # Mainnet
            "gas": GAS,
            "gasPrice": w3.eth.gas_price * 3,
            "nonce": nonce,
        }
    )

    # Sign and send transaction
    signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

    # Wait for transaction receipt
    time.sleep(20)
    w3.eth.wait_for_transaction_receipt(tx_hash)
    return tx_hash.hex()


def upsert_operators(w3, account, op, signature, signature_nonce, chain_id):
    eigen_contract = w3.eth.contract(address=SIMPLE_EIGEN_ADDRESS, abi=SIMPLE_EIGEN_ABI)

    # Prepare transaction
    nonce = w3.eth.get_transaction_count(account)
    tx = eigen_contract.functions.upsertOperatorSig(
        op, signature, signature_nonce
    ).build_transaction(
        {
            "chainId": chain_id,  # Mainnet
            "gas": GAS,
            "gasPrice": w3.eth.gas_price * 3,
            "nonce": nonce,
        }
    )

    # Sign and send transaction
    signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

    # Wait for transaction receipt
    time.sleep(20)
    w3.eth.wait_for_transaction_receipt(tx_hash)
    return tx_hash.hex()


def add_operators_dao(w3, account, op, chain_id):
    eigen_contract = w3.eth.contract(address=SIMPLE_EIGEN_ADDRESS, abi=SIMPLE_EIGEN_ABI)

    # Prepare transaction
    nonce = w3.eth.get_transaction_count(account)
    tx = eigen_contract.functions.addOperatorDAO(op).build_transaction(
        {
            "chainId": chain_id,  # Mainnet
            "gas": GAS,
            "gasPrice": w3.eth.gas_price * 3,
            "nonce": nonce,
        }
    )

    # Sign and send transaction
    signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

    # Wait for transaction receipt
    time.sleep(20)
    w3.eth.wait_for_transaction_receipt(tx_hash)
    return tx_hash.hex()


def update_operators(w3, account, op, signature, signature_nonce, chain_id):
    eigen_contract = w3.eth.contract(address=SIMPLE_EIGEN_ADDRESS, abi=SIMPLE_EIGEN_ABI)

    # Prepare transaction
    nonce = w3.eth.get_transaction_count(account)
    tx = eigen_contract.functions.updateOperatorSig(
        op, signature, signature_nonce
    ).build_transaction(
        {
            "chainId": chain_id,  # Mainnet
            "gas": GAS,
            "gasPrice": w3.eth.gas_price * 3,
            "nonce": nonce,
        }
    )

    # Sign and send transaction
    signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

    # Wait for transaction receipt
    time.sleep(20)
    w3.eth.wait_for_transaction_receipt(tx_hash)
    return tx_hash.hex()


def delete_operators(w3, account, op_address, signature, signature_nonce, chain_id):
    eigen_contract = w3.eth.contract(address=SIMPLE_EIGEN_ADDRESS, abi=SIMPLE_EIGEN_ABI)

    # Prepare transaction
    nonce = w3.eth.get_transaction_count(account)
    tx = eigen_contract.functions.deleteOperatorSig(
        op_address, signature, signature_nonce
    ).build_transaction(
        {
            "chainId": chain_id,  # Mainnet
            "gas": GAS,
            "gasPrice": w3.eth.gas_price * 3,
            "nonce": nonce,
        }
    )

    # Sign and send transaction
    signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

    # Wait for transaction receipt
    time.sleep(20)
    w3.eth.wait_for_transaction_receipt(tx_hash)
    return tx_hash.hex()
