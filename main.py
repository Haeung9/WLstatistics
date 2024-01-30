from blockTimeStatistics import fetch, genBlockTime, utils


def analysis():
    return genBlockTime.genData()

if __name__=="__main__":
    endpoint = "http://127.0.0.1:8545"
    blockTo = fetch.fetchLatestBlockNumber(endpoint) + 1
    blockFrom = 187004 # (closest block at unixtime: 1693494000)
    batchSize = 10000
    batchCnt = 0
    nameSeparator = "fetchResult"
    while(blockTo-blockFrom > 0):
        print("fetching batch " + str(batchCnt) + " ...")
        batchEnd = min(blockFrom + batchSize, blockTo)
        df = fetch.fetchTimestamp(endpoint, blockFrom, batchEnd)
        fileName = nameSeparator + str(batchCnt) + ".csv"
        utils.saveFile(df, fileName)
        batchCnt = batchCnt + 1
        blockFrom = batchEnd
    print("done!")
    utils.mergeBatch(nameSeparator, batchCnt)
    utils.clearIntermediate(nameSeparator, batchCnt)
    df = genBlockTime.genData(nameSeparator + ".csv")
    utils.saveFile(df, "genResult.csv")