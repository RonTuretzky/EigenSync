from eigensdk.crypto.bls.attestation import (
    g1_to_tupple,
    g2_to_tupple,
)
from web3 import Web3

from settings.local_setting import (
    INFURA_KEY,
    CHAIN_ID,
    ACCOUNT_ADDRESS,
    KEY_PAIR1,
)
from settings.setting import (
    SIMPLE_EIGEN_ADDRESS,
    SIMPLE_EIGEN_ABI,
)
from utils import (
    add_operators_dao,
)

sepolia_w3 = Web3(Web3.HTTPProvider(f"https://sepolia.infura.io/v3/{INFURA_KEY}"))
holesky_w3 = Web3(Web3.HTTPProvider(f"https://holesky.infura.io/v3/{INFURA_KEY}"))
eigen_contract = sepolia_w3.eth.contract(
    address=SIMPLE_EIGEN_ADDRESS, abi=SIMPLE_EIGEN_ABI
)

op = {
    "opAddress": ACCOUNT_ADDRESS,
    "socket": "http://127.0.0.1:8000",
    "stakedAmount": int(1e22),
    "pubG1": g1_to_tupple(KEY_PAIR1.pub_g1),
    "pubG2": g2_to_tupple(KEY_PAIR1.pub_g2),
}

add_operators_dao(sepolia_w3, ACCOUNT_ADDRESS, op, CHAIN_ID)
