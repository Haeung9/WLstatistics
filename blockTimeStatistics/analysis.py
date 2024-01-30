import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from . import utils

if __name__ == "__main__":
    df = utils.readFile("genResult.csv")
    maxValue = df["elapsed"].max()
    numberValue = len(df["elapsed"])
    plt.hist(df["elapsed"], weights= np.ones(len(df)) / len(df), bins= int(maxValue), cumulative= True, range=[0.0, 50.0], histtype= "step")
    plt.grid(True)
    plt.xlabel("block generation time (sec)")
    plt.ylabel("frequency")
    plt.title("block generation time frequency (cumulative)")
    plt.show()