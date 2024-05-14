import requests
import pandas as pd
import json

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

    try:
        data = [{"number": int(item["result"]["number"], 16), 
                "timestamp": int(item["result"]["timestamp"], 16)} for item in response.json()]
        df = pd.DataFrame(data=data).set_index("number", drop=True)
    except:
        print(response.json())
        raise(Exception("response error"))

    return df

def fetchDifficulty(endpoint, blockFrom, blockTo):
    batchRequest = []
    for i in range(blockFrom, blockTo):
        batchRequest.append(genBlockByNumberQuery(i-blockFrom, i))
    
    response = requests.post(endpoint, json=batchRequest)

    try:
        data = [{"number": int(item["result"]["number"], 16), 
                "difficulty": int(item["result"]["difficulty"], 16),
                "codeLength": int(item["result"]["codelength"], 16),
                "timestamp": int(item["result"]["timestamp"], 16)} for item in response.json()]
        df = pd.DataFrame(data=data).set_index("number", drop=True)
    except:
        print(response.json())
        raise(Exception("response error"))

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

def fetchClosestBlockNumberAtTimestamp(timestamp, closest = "before"):
    endpoint = "https://scan.worldland.foundation/api" # use scan.worldland.foundation/api
    req = {
        "module": "block",
        "action": "getblocknobytime",
        "timestamp": str(timestamp),
        "closest": closest
    }
    url = endpoint +"?module=" +req["module"] + "&action=" +req["action"] + "&timestamp=" +req["timestamp"] + "&closest=" +req["closest"]
    response = requests.get(url)
    return response.json()["result"]["blockNumber"]

def fetchBlocks(endpoint, blockFrom, blockTo):
    batchRequest = []
    for i in range(blockFrom, blockTo):
        batchRequest.append(genBlockByNumberQuery(i-blockFrom, i))
    response = requests.post(endpoint, json=batchRequest)
    print(json.dumps(response.json(), indent=4))
