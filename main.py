from blockTimeStatistics import analysis, fetch, genBlockTime, utils

if __name__=="__main__":
    endpoint = "http://127.0.0.1:8545"
    # endpoint = "https://gwangju.worldland.foundation"
    # endpoint = "https://mainnet.infura.io/v3/{API_KEY}"
    
    ## milstones WL
    # blk 0 (genesis) at 1691449688 (2023-08-07 23:08:08 +0)
    # blk 189820 at 1693526400 (2023-09-01 00:00:00 +0)
    # blk 1171763 at 1704067200 (2024-01-01 00:00:00 +0)
    # blk 1428982 at 1706745600 (2024-02-01 00:00:00 +0)
    blockTo = fetch.fetchLatestBlockNumber(endpoint) + 1 
    blockFrom = 2194400 # at Annapurna Testnet

    ## milstones ETH
    # blk 6988614 # at 1546300800 (2019-01-01 00:00:00 +0)
    # blk 10247483 # at (2020-06-12 00:00:01 +0)
    # blk 10570485 # at (2020-08-01 00:00:12 +0)
    # blk 13916165 # at 1640995200 (2022-01-01 00:00:00 +0)
    # blk 15047598 # at 1656547200 (2022-06-30 00:00:00 +0)
    # blk 15537394 # at 1663224179 (2022-09-15 06:42:59 +0), The merge
    # blk 18908894 # at 1704067200 (2024-01-01 00:00:00 +0)
    # blockFrom = 10247483
    # blockTo = blockFrom + 20001
    
    batchSize = 10 # 10000
    batchCnt = 0
    # nameSeparator = "difficultyResult"
    nameSeparator = "testnetDifficultyResult"
    while(blockTo-blockFrom > 0):
        print("fetching batch " + str(batchCnt) + " ...")
        batchEnd = min(blockFrom + batchSize, blockTo)
        df = fetch.fetchDifficulty(endpoint, blockFrom, batchEnd) 
        fileName = nameSeparator + str(batchCnt) + ".csv"
        utils.saveFile(df, fileName)
        batchCnt = batchCnt + 1
        blockFrom = batchEnd
    print("done!")
    utils.mergeBatch(nameSeparator, batchCnt)
    utils.clearIntermediate(nameSeparator, batchCnt)
    df = genBlockTime.genData(nameSeparator + ".csv")
    postProcessed = nameSeparator + "_processed.csv"
    utils.saveFile(df, postProcessed)
    analysis.main(postProcessed)