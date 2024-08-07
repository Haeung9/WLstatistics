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

def fetchMiners(endpoint, blockFrom, blockTo):
    batchRequest = []
    for i in range(blockFrom, blockTo):
        batchRequest.append(genBlockByNumberQuery(i-blockFrom, i))
    
    response = requests.post(endpoint, json=batchRequest)

    try:
        data = [{"number": int(item["result"]["number"], 16), 
                "miner": str(item["result"]["miner"])} for item in response.json()]
        df = pd.DataFrame(data=data).set_index("number", drop=True)
    except:
        print(response.json())
        raise(Exception("response error"))
    return df

def fetchBlocks(endpoint, blockFrom, blockTo):
    batchRequest = []
    for i in range(blockFrom, blockTo):
        batchRequest.append(genBlockByNumberQuery(i-blockFrom, i))
    response = requests.post(endpoint, json=batchRequest)
    
    # print(json.dumps(response.json(), indent=4))
    try:
        data = [{"result": item["result"]} for item in response.json()]
        # df = pd.DataFrame(data=data).set_index("number", drop=True)
        print(json.dumps(data, indent=4))
    except:
        print(response.json())
        raise(Exception("response error"))

def fetchAllTransactionsInBlocks(endpoint, blockFrom, blockTo):
    batchRequest = []
    for i in range(blockFrom, blockTo):
        batchRequest.append(genBlockByNumberQuery(i-blockFrom, i))
    response = requests.post(endpoint, json=batchRequest)
    transactionHash = []
    try:
        for item in response.json():
            txlist = item["result"]["transactions"]
            for tx in txlist:
                transactionHash.append(tx)
        return transactionHash
    except:
        print(response.json())
        raise(Exception("response error"))
    
def fetchValuesInTransactions(endpoint, transactionHash):
    batchRequest = []
    for i in range(len(transactionHash)):
        req = {
            "method": "eth_getTransactionByHash",
            "params": [transactionHash[i]],
            "id": 0,
            "jsonrpc": "2.0"
        }
        batchRequest.append(req)
    response = requests.post(endpoint, json=batchRequest)
    try:
        values = [item["result"]["value"] for item in response.json()]
    except:
        print(response.json())
        raise Exception("response error")
    return values

def fetchATransactionByHash(endpoint, transactionHash):
    req = {
        "method": "eth_getTransactionByHash",
        "params": [transactionHash],
        "id": 0,
        "jsonrpc": "2.0"
    }
    response = requests.post(endpoint, json=req)
    return json.dumps(response.json(),indent=4)


def fetchAllUnclesInBlocks(endpoint, blockFrom, blockTo):
    batchRequest = []
    for i in range(blockFrom, blockTo):
        batchRequest.append(genBlockByNumberQuery(i-blockFrom, i))
    response = requests.post(endpoint, json=batchRequest)
    uncles = []
    try:
        for item in response.json():
            uncleList = item["result"]["uncles"]
            for uncle in uncleList:
                uncles.append(uncle)
        return uncles
    except:
        print(response.json())
        raise(Exception("response error"))