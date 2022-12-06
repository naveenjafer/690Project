import os
import pandas as pd
import seaborn as sns
import copy
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

def drawWeightedCounterGraph(activationStatsDF, base_col, analysis_col, axs):
    total_polarity_bins, bin_start, bin_end, bin_iterator =20, 0, 1, 0.5
    if base_col == 'polarity':
        bin_start = 0.5
    polarity_bin_len = (bin_end-bin_start)/total_polarity_bins
    bins = []
    bin_col = base_col + '_bins'
    weightedColumn = 'weightedColumn'
    political_inclination = 'political_inclination'
    analysis_col_count = analysis_col + '_count'

    activationStatsDF_new = activationStatsDF.copy()[[base_col, analysis_col, political_inclination]]

    while bin_iterator<=bin_end:
        bins.append(bin_iterator)
        bin_iterator=round(bin_iterator+polarity_bin_len,3)

    labels = bins.copy()
    labels.remove(bin_end)


    activationStatsDF_new[bin_col] = pd.cut(activationStatsDF_new[base_col], bins=bins, labels=labels).astype(float)
    activationStatsDF_new = activationStatsDF_new.groupby([bin_col, analysis_col, 'political_inclination'])[analysis_col].count().to_frame().rename(columns={analysis_col: analysis_col_count}).reset_index()
    activationStatsDF_new['total_count'] = activationStatsDF_new[analysis_col]*activationStatsDF_new[analysis_col_count]
    activationStatsDF_new = activationStatsDF_new.groupby([bin_col, 'political_inclination'])[analysis_col_count, 'total_count'].sum().reset_index()
    activationStatsDF_new[weightedColumn] = activationStatsDF_new["total_count"]/activationStatsDF_new[analysis_col_count]
    activationStatsDF_new_left = activationStatsDF_new[activationStatsDF_new[political_inclination]==-1]
    activationStatsDF_new_right = activationStatsDF_new[activationStatsDF_new[political_inclination]==1]
    axs[1].scatter(activationStatsDF_new_left[bin_col], activationStatsDF_new_left[weightedColumn], color='blue', label='left leaning')
    axs[1].scatter(activationStatsDF_new_right[bin_col], activationStatsDF_new_right[weightedColumn], color='red', label ='right leaning')
    axs[1].legend(loc='upper left')
    axs[1].set_xlabel(bin_col)
    axs[1].set_ylabel('Weighted Count of '+analysis_col)

def drawSubPlotsToShowActivationTrends(activationStatsDF, homiphily_index, polarity_col, analysis_col):
    fig, axs = plt.subplots(1, 2, figsize=(14,7))
    fig.suptitle(polarity_col+" VS "+analysis_col+" WITH Homophily Index - "+str(homiphily_index))
    plotHistograms(polarity_col, analysis_col, activationStatsDF, axs)
    drawWeightedCounterGraph(activationStatsDF, polarity_col, analysis_col, axs)
    plt.show()

def analyzeHistograms(activationStats):
    activationStatsDF = convertToPandasDF(activationStats)
    plotHistograms("polarity", "activeCounter", activationStatsDF)

def analyzeHistogramsAggregated(activationStatsAll, homiphily_index):
    allDFs = []
    for activationStat in activationStatsAll:
        activationStatsDF = convertToPandasDF(activationStat)
        allDFs.append(activationStatsDF)
    activationStatsDFAll = pd.concat(allDFs)
    drawSubPlotsToShowActivationTrends(activationStatsDFAll, homiphily_index, "polarity", "activeCounter")
    drawSubPlotsToShowActivationTrends(activationStatsDFAll, homiphily_index, "attractiveness", "activeCounter")
    drawSubPlotsToShowActivationTrends(activationStatsDFAll, homiphily_index, "polarity", "activeCongruentFinal")
    drawSubPlotsToShowActivationTrends(activationStatsDFAll, homiphily_index, "polarity", "activeNonCongruentFinal")
    drawSubPlotsToShowActivationTrends(activationStatsDFAll, homiphily_index, "attractiveness", "activeCongruentFinal")
    drawSubPlotsToShowActivationTrends(activationStatsDFAll, homiphily_index, "attractiveness", "activeNonCongruentFinal")

def convertToPandasDF(activationStats):
    activationStatsCopy = copy.deepcopy(activationStats)
    for item in activationStatsCopy:
        for subItem in item["endOfRoundStats"]:
            item[subItem] = item["endOfRoundStats"][subItem]
        del item["endOfRoundStats"]
    return pd.DataFrame(activationStatsCopy)



def plotHistograms(xLabel, yLabel, activationStatsDF, axs):
    sns.histplot(activationStatsDF, x=xLabel, y=yLabel, kde = True, cbar=True, pthresh=0.1, bins=20, ax=axs[0])


