import requests
import pandas as pd
from . import utils

def genBlockByNumberQuery(id, blockNumber):
    query = {
        "method": "eth_getBlockByNumber",
        "params": [hex(blockNumber), False],
        "id": id,
        "jsonrpc": "2.0"
    }
    return query

def fetchTimestamp(endpoint, blockFrom, blockTo):
    batchRequest = []
    for i in range(blockFrom, blockTo):
        batchRequest.append(genBlockByNumberQuery(i-blockFrom, i))
    
    response = requests.post(endpoint, json=batchRequest)

    data = [{"number": int(item["result"]["number"], 16), 
            "timestamp": int(item["result"]["timestamp"], 16)} for item in response.json()]
    df = pd.DataFrame(data=data).set_index("number", drop=True)

    return df

def fetchLatestBlockNumber(url):
    req = {
        "method": "eth_blockNumber",
        "params": [],
        "id": 0,
        "jsonrpc": "2.0"
    }
    response = requests.post(url, json=req)
    return int(response.json()["result"], 16)
