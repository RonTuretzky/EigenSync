import requests

from setting import SUBGRAPH_URL


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
