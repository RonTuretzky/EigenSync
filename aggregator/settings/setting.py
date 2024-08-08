import json


def load_abi_from_file(file_path):
    with open(file_path, "r") as abi_file:
        abi = json.load(abi_file)
    return abi


SIMPLE_EIGEN_ADDRESS = "0x92046d0Ae13Fe69ce5bf681925957dBfC5D2269b"
SUBGRAPH_URL = (
    "https://api.studio.thegraph.com/query/85556/bls_apk_registry/version/latest"
)

SIMPLE_EIGEN_ABI = load_abi_from_file("ABIs/simple_eigen_abi.json")

GAS = 4000000

Action = {"ADD": 0, "DELETE": 1, "UPDATE": 2, "UPSERT": 3}

AGGREGATOR_DELAY = 5
