import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
from datetime import datetime
from . import utils

def main(difficultyFileName):
    figureAxisType = "blockNumber" # "timestamp"
    df1 = utils.readFile(difficultyFileName)    

    blockNumber = df1["number"]
    difficulty = df1["difficulty"]
    codelength = df1["codeLength"]
    timestamp = df1["timestamp"]
    blockTime = df1["elapsed"]

    flopData = np.multiply(difficulty.to_numpy(), (435.0 * codelength.to_numpy() + 26020) )
    flop = pd.Series(flopData)
    dateTime = [datetime.fromtimestamp(items) for items in timestamp]

    BGTHist = blockTime.groupby(blockTime.values).count()
    histIndex = np.arange(math.ceil(blockTime.max())) + 1.0
    BGTHist = BGTHist .reindex(histIndex).fillna(value=0)

    figureRange = [0.0, 100.0]
    # exponential model with data mean
    xaxis = np.arange(math.ceil(figureRange[1])) + 1
    pdf_exp = np.exp(-xaxis/blockTime.mean()) / blockTime.mean()

    print("-------- Data General --------")
    print("    number of data = ", len(blockTime))
    print("    data from ", dateTime[0], ", blk#", blockNumber.iloc[0])
    print("    data to ", dateTime[-1], ", blk#", blockNumber.iloc[-1])
    print("---------------------------------")

    print("-------- Data Statistics (blocktime) --------")
    print("    mean block time = ", blockTime.mean())
    print("    variance = ", blockTime.var())
    print("    max value = ", blockTime.max())
    print("---------------------------------")

    print("-------- Data Statistics (difficulty) --------")
    print("    mean = ", difficulty.mean())
    print("    variance = ", difficulty.var())
    print("    max value = ", difficulty.max())
    print("    min value = ", difficulty.min())
    print("----------------------------------------------")

    print("-------- Data Statistics (difficulty, FLOP) --------")
    print("    mean = ", flop.mean())
    print("    variance = ", flop.var())
    print("    max value = ", flop.max())
    print("    min value = ", flop.min())
    print("----------------------------------------------------")

    print("-------- Data Statistics (code length) --------")
    print("    mean = ", codelength.mean())
    print("    variance = ", codelength.var())
    print("    max value = ", codelength.max())
    print("    max value = ", codelength.min())
    print("-----------------------------------------------")

    if figureAxisType == "blockNumber":
        figureBaseAxis = blockNumber
    else:
        figureBaseAxis = timestamp
    plt.figure()
    plt.plot(figureBaseAxis, blockTime)
    plt.grid(True)
    plt.title("block time")
    plt.xlabel(figureAxisType)
    plt.ylabel("time [sec]")

    fig, ax = plt.subplots()
    ax.plot(xaxis, pdf_exp)
    ax.bar(histIndex, BGTHist/float(len(blockTime)), color="brown")
    plt.grid(True)
    plt.title("block generation time frequency / PDF")
    plt.xlabel("block generation time (sec)")
    plt.ylabel("probability")
    plt.legend(["exponential model (mean=" + str(blockTime.mean()) + ")", "observed"])

    plt.figure()
    plt.plot(blockNumber, difficulty)
    plt.grid(True)
    plt.title("block difficulty")
    plt.xlabel(figureAxisType)
    plt.ylabel("difficulty [decodings]")

    plt.figure()
    plt.plot(blockNumber, codelength)
    plt.grid(True)
    plt.title("code length")
    plt.xlabel(figureAxisType)
    plt.ylabel("code length")

    plt.figure()
    plt.plot(blockNumber, flop)
    plt.grid(True)
    plt.title("block difficulty [FLOP]")
    plt.xlabel(figureAxisType)
    plt.ylabel("difficulty [FLOP]")

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

    # ------------------------------------------------
    # BOX PLOT

    # groupSize = 10000
    groupSize = math.ceil(len(difficulty) / 10)
    numberofGroup = math.floor(len(difficulty) / groupSize)
    boxPoints = []
    for i in range(numberofGroup):
        if figureAxisType == "blockNumber":
            boxPoints.append("#"+ str(blockNumber[(i+1)*groupSize - 1]))
        else:
            boxPoints.append(str(dateTime[(i+1)*groupSize - 1].date()))

    dataGrouped = difficulty.loc[:groupSize*numberofGroup - 1].to_numpy()
    dataGrouped = dataGrouped.reshape((numberofGroup, groupSize)).transpose()
    dataGrouped = pd.DataFrame(data=dataGrouped, columns=boxPoints)

    codelengthGrouped = codelength.loc[:groupSize*numberofGroup - 1].to_numpy()
    codelengthGrouped = codelengthGrouped.reshape((numberofGroup, groupSize)).transpose()
    codelengthGrouped = pd.DataFrame(data=codelengthGrouped, columns=boxPoints) 

    flopGrouped = flop.loc[:groupSize*numberofGroup - 1].to_numpy()
    flopGrouped = flopGrouped.reshape((numberofGroup, groupSize)).transpose()
    flopGrouped = pd.DataFrame(data=flopGrouped, columns=boxPoints) 
    
    print("----------- Box Plot ------------")
    print("    box size = ", groupSize)
    print("    number of boxes = ", numberofGroup)
    print("---------------------------------")
    # print(dataGrouped.head())

    plt.figure()
    dataGrouped.boxplot()
    plt.title("box plot for difficulty")
    plt.xlabel("time")
    plt.ylabel("difficulty [decodings]")

    plt.figure()
    codelengthGrouped.boxplot()
    plt.title("box plot for code length")
    plt.xlabel("time")
    plt.ylabel("codelength")

    plt.figure()
    flopGrouped.boxplot(showfliers=False)
    plt.title("box plot for difficulty [FLOP]")
    plt.xlabel("time")
    plt.ylabel("difficulty [FLOP]")
    # ------------------------------------------------

    plt.show()

if __name__ == "__main__":
    # difficultyFileName = os.path.join(os.path.join("temp","WL"), "difficultyResult_processed.csv")
    # difficultyFileName = os.path.join(os.path.join("temp","WL"), "testnetDifficultyResult_processed.csv")
    difficultyFileName = "difficultyResult_processed.csv"
    main(difficultyFileName)
