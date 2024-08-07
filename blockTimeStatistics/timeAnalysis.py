import numpy as np
import pandas as pd
import math
import os
import matplotlib.pyplot as plt
from scipy.stats import chi2, chisquare
from . import utils

if __name__ == "__main__":
    # fileName = "difficultyResult_processed.csv"
    fileName = os.path.join("temp",os.path.join("ETH_10570486", "genResult.csv"))
    df = utils.readFile(fileName)
    useFullData = True
    if useFullData:
        data = df["elapsed"]
    else:
        dataFrom = 189820
        dataEnd = 1428982
        data = df["elapsed"].loc[dataFrom:dataEnd]
    maxValue = data.max()
    numberValue = len(data)
    mean = data.mean()
    variance = data.var()
    print("-------- Data Statistics --------")
    print("    number of data = ", numberValue)
    print("    mean block time = ", mean)
    print("    variance = ", variance)
    print("    max value = ", maxValue)
    print("---------------------------------")


    # sampling
    samples = data.sample(min(20000,len(data)), random_state=1)
    sampleMean = samples.mean()
    sampleVariance = samples.var()
    sampleMaxValue = samples.max()
    sampleTailPoint = math.ceil( 2.2 * math.sqrt(sampleVariance))

    dataHist = data.groupby(data.values).count()
    histIndex = np.arange(math.ceil(maxValue)) + 1.0
    dataHist = dataHist.reindex(histIndex).fillna(value=0)
    sampleHist = samples.groupby(samples.values).count()
    newIndex = np.arange(math.ceil(sampleMaxValue)) + 1.0
    sampleHist = sampleHist.reindex(newIndex).fillna(value=0) # zero padding
    
    print("-------- Sample Statistics --------")
    print("    number of samples = ", len(samples))
    print("    sample mean = ", sampleMean)
    print("    sample variance = ", sampleVariance)
    print("-----------------------------------")

    figureRange = [0.0, 100.0]

    # geometric model with data mean
    xaxis = np.arange(math.ceil(figureRange[1])) + 1
    pdf = (1.0 - (1.0 / mean))**(xaxis-1) / mean
    cdf = 1.0 - (1.0 - (1.0 / mean))**xaxis
    # exponential model with data mean
    pdf_exp = np.exp(-xaxis/mean) / mean
    cdf_exp = 1.0 - np.exp(-xaxis/mean)

    # geometric model with sample mean
    pdf_sample = (1.0 - (1.0 / sampleMean))**(xaxis-1) / sampleMean
    cdf_sample = 1.0 - (1.0 - (1.0 / sampleMean))**xaxis
    # exponential model with sample mean
    pdf_sample_exp = np.exp(-xaxis/sampleMean) / sampleMean
    cdf_sample_exp = 1.0 - np.exp(-xaxis/sampleMean)

    # Chi-Square Test with Samples
    ## 1. Expected Frequency
    xaxis_aggTail = np.arange(sampleTailPoint) + 1
    pdf_aggTail = (1.0 - (1.0 / sampleMean))**(xaxis_aggTail-1) / sampleMean
    pdf_aggTail[-1] = (1.0 - (1.0 / sampleMean))**(sampleTailPoint-1)
    expectedFrequency = pdf_aggTail * len(samples)

    ## 2. Observed Frequency
    observedData = sampleHist.loc[:sampleTailPoint].copy()
    observedTailWeight = sampleHist.loc[sampleTailPoint:].sum().copy()
    observedData.loc[sampleTailPoint] = observedTailWeight
    observed = observedData.to_numpy(dtype="float")

    print("-------- Contingency Table --------")
    print(pd.DataFrame([observed, expectedFrequency]))
    print("-----------------------------------")

    ## 3. Test
    degreeOfFreedom = sampleTailPoint - 1
    criticalValue = chi2(degreeOfFreedom).ppf(0.95)
    result = chisquare(f_obs=observed, f_exp=expectedFrequency)
    numberOfBadCells = len(np.where(observed<5))
    print("-------- Chi-Square Test --------")
    print("    degree of freedom = ", degreeOfFreedom)
    print("    critical value (significance level = 0.05) = ", criticalValue)
    print("    test statistic = ", result.statistic)
    print("    p-value = ", result.pvalue)
    print("    test pass? ", result.pvalue > 0.05)
    print("---------------------------------")

    fig1, ax1 = plt.subplots()
    ax1.plot(xaxis, pdf_exp)
    # ax1.step(xaxis, pdf)
    ax1.plot(histIndex, dataHist/float(len(data)))
    plt.grid(True)
    plt.title("block generation time frequency / PDF")
    plt.xlabel("block generation time (sec)")
    plt.ylabel("probability")
    plt.legend(["exponential model (mean=" + str(mean) + ")", "observed"])
    
    fig2, ax2 = plt.subplots()
    ax2.plot(xaxis, cdf_exp)
    # ax2.step(xaxis, cdf)
    ax2.hist(data, density=True, bins= int(maxValue), cumulative=True, range=figureRange)
    plt.grid(True)
    plt.title("block generation time cumulative frequency / CDF")
    plt.xlabel("block generation time (sec)")
    plt.ylabel("probability (cumulative)")
    plt.legend(["exponential model (mean=" + str(mean) + ")", "observed"])
    
    fig3, ax3 = plt.subplots()
    ax3.plot(xaxis, pdf_sample_exp)
    # ax3.step(xaxis, pdf_sample)
    ax3.plot(newIndex, sampleHist/float(len(samples)))
    plt.grid(True)
    plt.title("block generation time frequency / PDF")
    plt.xlabel("block generation time (sec)")
    plt.ylabel("probability")
    plt.legend(["exponential model (mean=" + str(sampleMean) + ")", "observed"])
    
    fig4, ax4 = plt.subplots()
    ax4.plot(xaxis, cdf_sample_exp)
    # ax4.step(xaxis, cdf_sample)
    ax4.hist(samples, density=True, bins= int(maxValue), range=figureRange, cumulative= True, histtype= "step")
    plt.grid(True)
    plt.title("block generation time cumulative frequency / CDF")
    plt.xlabel("block generation time (sec)")
    plt.ylabel("probability (cumulative)")
    plt.legend(["exponential model (mean=" + str(sampleMean) + ")", "observed"])

    # filtering out elapsed <= 1
    filteredData = data[data > 1.0]
    maxValueFiltered = filteredData.max()
    numberValueFiltered = len(filteredData)
    meanFiltered = filteredData.mean()
    varianceFiltered = filteredData.var()

    print(filteredData.head(10))
    print("mean block time (filtered)= ", meanFiltered)
    print("variance (filtered) = ", varianceFiltered)

    # plt.figure(11)
    # plt.hist(filteredData, density=True, bins= int(maxValueFiltered), range=figureRange, histtype="step")
    # plt.grid(True)
    # plt.title("block generation time frequency (excluding 1s-blocks)")
    # plt.xlabel("block generation time (sec)")
    # plt.ylabel("frequency")

    # plt.figure(22)
    # plt.hist(filteredData, density=True, bins= int(maxValueFiltered), range=figureRange, cumulative=True, histtype="step")
    # plt.grid(True)
    # plt.title("block generation time frequency (cumulative, excluding 1s-blocks)")
    # plt.xlabel("block generation time (sec)")
    # plt.ylabel("frequency (cumulative)")

    pdfFiltered = (1.0 - (1.0 / meanFiltered))**(xaxis-1) / meanFiltered
    cdfFiltered = 1.0 - (1.0 - (1.0 / meanFiltered))**xaxis

    # plt.figure(33)
    # plt.step(xaxis, pdfFiltered)
    # plt.title("Geometric PDF, mean = " + str(meanFiltered))
    # plt.xlabel("block generation time")
    # plt.ylabel("PDF")
    # plt.grid(True)

    # plt.figure(44)
    # plt.step(xaxis, cdfFiltered)
    # plt.title("Geometric CDF, mean = " + str(meanFiltered))
    # plt.xlabel("block generation time")
    # plt.ylabel("CDF")
    # plt.grid(True)

    roi = 20
    frq = dataHist.loc[:roi].to_numpy()/20000.0
    cumfrq = frq.copy()
    for i in range(roi-1):
        cumfrq[i+1] = cumfrq[i] + cumfrq[i+1]
    # print(frq)
    print(cumfrq)
    print(cdf_exp[:roi])
    print(cdf[:roi])

    print(frq)
    print(pdf_exp[:roi])
    print(pdf[:roi])

    # print(dataHist[:3].sum())
    # print(dataHist[:14].sum())
    # print(dataHist[:27].sum())
    plt.show()

