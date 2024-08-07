import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
from datetime import datetime
from . import utils

def main(minersFileName):
    figureAxisType = "blockNumber" # "timestamp"
    df1 = utils.readFile(minersFileName)    

    blockNumber = df1["number"]
    miners = df1["miner"]

    minerHist = miners.groupby(miners.values).count()


    print("-------- Data General --------")
    print("    number of data = ", len(blockNumber))
    print("    data from blk#", blockNumber.iloc[0])
    print("    data to blk#", blockNumber.iloc[-1])
    print("---------------------------------")

    print("-------- Data Statistics (miners) --------")
    print("    top miner = ", minerHist.idxmax())
    print("    number of successive miners = ", len(minerHist))
    print("    percentage of the top miner = ", float(minerHist.max())/float(len(blockNumber)))
    print("---------------------------------")

    minerHistDecending = minerHist.sort_values(ascending=False)
    minerHistTop10 = minerHistDecending.iloc[0:10]
    minerElsewhere = minerHistDecending.iloc[10:].values.sum()
    label_cut = [item[0:6]+"..." for item in minerHistTop10.index]
    minerHistElsewhere = pd.Series(data= [minerElsewhere], index=["etc"])
    minerHistTop10 = pd.concat([minerHistTop10, minerHistElsewhere])
    label_cut.append("etc")

    # PI calculation
    numberOfHeavy = math.ceil(len(minerHistDecending) / 10.0)
    minedByHeavy = minerHistDecending[0:numberOfHeavy].values.sum()
    minedByTotal = minerHistDecending.values.sum()
    shareHeavy = float(minedByHeavy) / float(minedByTotal)
    print("Polarization Index (to 10%): ", shareHeavy)

    print(label_cut)
    utils.saveFile(minerHistDecending,"ranking")

    plt.figure()
    minerHistDecending.plot.pie(labels = None, autopct="%1.1f%%", legend=False)
    plt.grid(True)
    plt.title("miners histogram")

    plt.figure()
    minerHistTop10.plot.pie(labels = label_cut, autopct="%1.1f%%")
    plt.grid(True)
    plt.title("miners histogram (Top10)")


    # # ------------------------------------------------
    # # MOVING AVERAGE

    # # windowSize = 1000
    # windowSize = math.ceil(len(difficulty) / 100)
    # roll = difficulty.rolling(windowSize)
    # movingAverage = roll.mean()
    # movingAverage = movingAverage.loc[windowSize-1:]
    # if figureAxisType == "blockNumber":
    #     xaxis = blockNumber.loc[windowSize-1:]
    # else:
    #     xaxis = timestamp.loc[windowSize-1:]

    # plt.figure()
    # plt.plot(xaxis, blockTime.rolling(windowSize).mean().loc[windowSize-1:])
    # plt.grid(True)
    # plt.title("block time (moving average)")
    # plt.xlabel(figureAxisType)
    # plt.ylabel("block time")

    # plt.figure()
    # plt.plot(xaxis, difficulty.rolling(windowSize).mean().loc[windowSize-1:])
    # plt.grid(True)
    # plt.title("block difficulty (moving average)")
    # plt.xlabel(figureAxisType)
    # plt.ylabel("difficulty")

    # plt.figure()
    # plt.plot(xaxis, codelength.rolling(windowSize).mean().loc[windowSize-1:])
    # plt.grid(True)
    # plt.title("code length (moving average)")
    # plt.xlabel(figureAxisType)
    # plt.ylabel("code length")

    # plt.figure()
    # plt.plot(xaxis, flop.rolling(windowSize).mean().loc[windowSize-1:])
    # plt.grid(True)
    # plt.title("block difficulty (moving average) [flop]")
    # plt.xlabel(figureAxisType)
    # plt.ylabel("difficulty [flop]")
    # # ------------------------------------------------

    plt.show()

if __name__ == "__main__":
    # difficultyFileName = os.path.join(os.path.join("temp","WL"), "difficultyResult_processed.csv")
    # difficultyFileName = os.path.join(os.path.join("temp","WL"), "testnetDifficultyResult_processed.csv")
    difficultyFileName = "minersResult.csv"
    main(difficultyFileName)
