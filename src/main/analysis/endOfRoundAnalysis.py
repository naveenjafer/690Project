import os
import pandas as pd
import seaborn as sns
import copy
import matplotlib.pyplot as plt

def analyzeHistograms(activationStats):
    activationStatsDF = convertToPandasDF(activationStats)
    plotHistograms("polarity", "activeCounter", activationStatsDF)

def convertToPandasDF(activationStats):
    activationStatsCopy = copy.deepcopy(activationStats)
    for item in activationStatsCopy:
        for subItem in item["endOfRoundStats"]:
            item[subItem] = item["endOfRoundStats"][subItem]
        del item["endOfRoundStats"]
    return pd.DataFrame(activationStatsCopy)

def plotHistograms(xLabel, yLabel, activationStatsDF):
    sns.histplot(activationStatsDF, x="polarity", y="activeCounter", kde = True, cbar=True, pthresh=0.1)
    plt.show()


