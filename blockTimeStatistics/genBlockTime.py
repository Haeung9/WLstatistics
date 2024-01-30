import pandas as pd
from . import utils

def genData(fetchFileName = "fetchResult.csv"):
    # Calculate block generation times
    df = utils.readFile(fetchFileName)
    block_generation_times = df["timestamp"].diff().rename("elapsed")
    df = pd.concat([df, block_generation_times], axis=1).set_index("number").dropna()
    return df

if __name__=="__main__":
    df = genData()
    utils.saveFile(df, "genResult.csv")
    