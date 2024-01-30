import os
import pandas as pd

def dataPath():
    rootpath = os.getcwd()
    datadirpath = os.path.join(rootpath, "data")
    return datadirpath

def makeDataDir():
    datadirpath = dataPath()
    try:
        if not os.path.exists(datadirpath):
            os.makedirs(datadirpath)
    except OSError:
        print("Error: Failed to create the directory.")

def saveFile(df, fileName):
    datadirpath = dataPath()
    makeDataDir()
    writeFileName = os.path.join(datadirpath, fileName)
    df.to_csv(writeFileName)

def readFile(fileName):
    datadirpath = dataPath()
    readFileName = os.path.join(datadirpath, fileName)
    df = pd.read_csv(readFileName)
    return df

def mergeBatch(nameSeparator, batchNumber):
    df = []
    for i in range(batchNumber):
        name = nameSeparator + str(i) + ".csv"
        df.append(readFile(name).set_index("number"))
    saveFile(pd.concat(df), nameSeparator+".csv")

def clearIntermediate(nameSeparator, batchNumber):
    datadirpath = dataPath()
    for i in range(batchNumber):
        name = nameSeparator + str(i) + ".csv"
        path = os.path.join(datadirpath, name)
        if os.path.isfile(path):
            os.remove(path)