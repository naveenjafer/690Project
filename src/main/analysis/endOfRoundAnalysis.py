import os
import pandas as pd
import seaborn as sns
import copy
import matplotlib.pyplot as plt

def analyzeHistograms(activationStats):
    activationStatsDF = convertToPandasDF(activationStats)
    plotHistograms("polarity", "activeCounter", activationStatsDF)

def analyzeHistogramsAggregated(activationStatsAll, runBaseFolder):
    allDFs = []
    for activationStat in activationStatsAll:
        activationStatsDF = convertToPandasDF(activationStat)
        allDFs.append(activationStatsDF)
    activationStatsDFAll = pd.concat(allDFs)
    plotHistograms("polarity", "activeCounter", activationStatsDFAll, runBaseFolder)

def convertToPandasDF(activationStats):
    activationStatsCopy = copy.deepcopy(activationStats)
    for item in activationStatsCopy:
        for subItem in item["endOfRoundStats"]:
            item[subItem] = item["endOfRoundStats"][subItem]
        del item["endOfRoundStats"]
    return pd.DataFrame(activationStatsCopy)



def plotHistograms(xLabel, yLabel, activationStatsDF, runBaseFolder):
    sns.histplot(activationStatsDF, x=xLabel, y=yLabel, kde = True, cbar=True, pthresh=0.1)
    plt.title(f"Heatmap of {xLabel} vs {yLabel} averaged across runs")
    plt.show()
    plt.savefig(os.path.join(runBaseFolder))


