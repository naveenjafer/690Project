import os
import pandas as pd
import seaborn as sns
import copy
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")
import numpy as np

#bins = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

'''
def drawWeightedCounterGraph(activationStatsDF, base_col, analysis_col, axs):
<<<<<<< HEAD
    total_polarity_bins, bin_start, bin_end, bin_iterator = 20, 0, 1, 0.5
=======
    total_polarity_bins, bin_start, bin_end = 20, 0, 1
>>>>>>> 339a6aab0869f3721b0deea9ee851e70c2577703
    if base_col == 'polarity':
        bin_start = 0.5
    bin_iterator = bin_start
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


def drawSubPlotsToShowActivationTrends(activationStatsDF, homiphily_index, runBaseFolder, polarity_col, analysis_col):
    fig, axs = plt.subplots(1, 2, figsize=(14,7))
    fig.suptitle(polarity_col+" VS "+analysis_col+" WITH Homophily Index - "+str(homiphily_index))
    plotHistograms(polarity_col, analysis_col, activationStatsDF, axs)
    drawWeightedCounterGraph(activationStatsDF, polarity_col, analysis_col, axs)
    plt.savefig(os.path.join(runBaseFolder, f"{polarity_col}_{analysis_col}.png"))
    plt.show()
    '''

def analyzeHistograms(activationStats):
    activationStatsDF = convertToPandasDF(activationStats)
    fig, axs = plt.subplots(1, 2, figsize=(14,7))
    plotHistograms("polarity", "activeCounter", activationStatsDF, axs)

def analyzeHistogramsAggregated(activationStatsAll, homiphily_index, runBaseFolder):
    allDFs = []
    for activationStat in activationStatsAll:
        activationStatsDF = convertToPandasDF(activationStat)
        allDFs.append(activationStatsDF)
    activationStatsDFAll = pd.concat(allDFs)

    activationStatsDFAll.to_csv(os.path.join(runBaseFolder, f"activationStatsDFAll_{homiphily_index}.csv"))

    plotHistogramsWithoutAxs("polarity", "activeCounter", activationStatsDFAll, runBaseFolder)
    #plotHistogramsWithoutAxs("polarity", "activeCongruentFinal", activationStatsDFAll, runBaseFolder)
    #plotHistogramsWithoutAxs("polarity", "activeNonCongruentFinal", activationStatsDFAll, runBaseFolder)

    print("activationStatsDFAll head is")
    print(activationStatsDFAll.head())
    
    activationStatsDFAllBinned = get_agg_results_for_attractive_articles(activationStatsDFAll)

    activationStatsDFAllBinned.to_csv(os.path.join(runBaseFolder, f"activationStatsDFAllBinned_{homiphily_index}.csv"))

    print("activationStatsDFAllBinned's head is")
    print(activationStatsDFAllBinned.head())


    compare_adoptions_by_homophily_index(activationStatsDFAllBinned, "activeCounter", runBaseFolder, "# of Active Nodes")
    compare_adoptions_by_homophily_index(activationStatsDFAllBinned, "activeCongruentFinal", runBaseFolder, "# of Congruent Active Nodes")
    compare_adoptions_by_homophily_index(activationStatsDFAllBinned, "activeNonCongruentFinal", runBaseFolder, "# of Non-Congruent Active Nodes")
    compare_adoptions_by_homophily_index(activationStatsDFAllBinned, "roundsCounter", runBaseFolder, "# of timesteps to convergence")
    compare_adoptions_by_homophily_index(activationStatsDFAllBinned, "activationsPerRound", runBaseFolder, "# of activations/timestep")
    
    '''
    drawSubPlotsToShowActivationTrends(activationStatsDFAll, homiphily_index, runBaseFolder, "polarity", "activeCounter")
    drawSubPlotsToShowActivationTrends(activationStatsDFAll, homiphily_index, runBaseFolder, "attractiveness", "activeCounter")
    drawSubPlotsToShowActivationTrends(activationStatsDFAll, homiphily_index, runBaseFolder, "polarity", "activeCongruentFinal")
    drawSubPlotsToShowActivationTrends(activationStatsDFAll, homiphily_index, runBaseFolder, "polarity", "activeNonCongruentFinal")
    drawSubPlotsToShowActivationTrends(activationStatsDFAll, homiphily_index, runBaseFolder, "attractiveness", "activeCongruentFinal")
    drawSubPlotsToShowActivationTrends(activationStatsDFAll, homiphily_index, runBaseFolder, "attractiveness", "activeNonCongruentFinal")
    '''

def convertToPandasDF(activationStats):
    activationStatsCopy = copy.deepcopy(activationStats)
    for item in activationStatsCopy:
        for subItem in item["endOfRoundStats"]:
            item[subItem] = item["endOfRoundStats"][subItem]
        del item["endOfRoundStats"]
    return pd.DataFrame(activationStatsCopy)

def plotHistograms(xLabel, yLabel, activationStatsDF, axs):
    sns.histplot(activationStatsDF, x=xLabel, y=yLabel, kde = True, cbar=True, pthresh=0.1, bins=20, ax=axs[0])
    #plt.title(f"Heatmap of {xLabel} vs {yLabel} averaged across runs")
    #plt.show()
    #plt.savefig(os.path.join(runBaseFolder, "heatmap.png"))

def plotHistogramsWithoutAxs(xLabel, yLabel, activationStatsDF, runBaseFolder):
    sns.histplot(activationStatsDF, x=xLabel, y=yLabel, kde = True, cbar=True, pthresh=0.1, bins=20)
    plt.title(f"Heatmap of {xLabel} vs {yLabel} averaged across runs")
    plt.savefig(os.path.join(runBaseFolder, "heatmap.png"))
    plt.show()
    
def get_agg_results_for_attractive_articles(df, attractiveness_factor = 0):
    bins = []
    bin_start, bin_end = 0,1
    total_polarity_bins = 20
    polarity_bin_len = (bin_end-bin_start)/total_polarity_bins
    bin_iterator = 0.5
    while bin_iterator<=bin_end:
        bins.append(bin_iterator)
        bin_iterator=round(bin_iterator+polarity_bin_len,3)

    cat_df_attractive = df[df["attractiveness"] >= attractiveness_factor]
    cat_df_attractive['bin_polarity'] = pd.cut(cat_df_attractive['polarity'], bins)
    cat_df_grouped = cat_df_attractive.groupby(['bin_polarity'])
    size_df_grouped = cat_df_grouped.size()
    print("*****interest point******")
    print(size_df_grouped)
    cat_df_attractie_agg = cat_df_grouped.mean()
    return cat_df_attractie_agg

def compare_adoptions_by_homophily_index(activationStatsDFAllBinned, active_counter_category, runBaseFolder, proxyName):
    plt.plot(activationStatsDFAllBinned["polarity"], activationStatsDFAllBinned[active_counter_category])
    plt.title(f"Polarity vs {proxyName}")
    plt.xlabel("polarity")
    plt.ylabel(active_counter_category)
    plt.legend()
    plt.savefig(os.path.join(runBaseFolder, f"polarity_{active_counter_category}.png"))
    plt.show()

def plotBoxPlotOfActivations(p_listsAll):
    p_listsAll
    p_listNew = []
    for item in p_listsAll:
        p_listNew.append([item[0], "p_a"])
        p_listNew.append([item[1], "p_n"])
        p_listNew.append([item[2], "p_p"])
    p_listNewDF = pd.DataFrame(p_listNew, columns=["x", "y"])


    sns.violinplot(data = p_listNewDF, x = "y", y = "x")
    plt.show()

def analyzeNetworkDynamics(activationDynamicsStatsAll, homiphily_index, runBaseFolder):
    maxRounds = 0
    for item in activationDynamicsStatsAll:
        maxRounds = max(len(item["dynamics"]), maxRounds)
    
    for item in activationDynamicsStatsAll:
        if len(item["dynamics"]) < maxRounds:
            item["dynamics"] = item["dynamics"] + [item["dynamics"][-1]] * (maxRounds - len(item["dynamics"]))
        item["dynamics"] = np.array(item["dynamics"])
    #print(maxRounds)
    binsForDynamics = [0.5, 0.6, 0.7, 0.8, 0.9, 1]
    activationDynamicsStatsAll = pd.DataFrame(activationDynamicsStatsAll)

    activationDynamicsStatsAll['bin_polarity'] = pd.cut(activationDynamicsStatsAll['polarity'], binsForDynamics)
    activationDynamicsStatsAllGrouped = activationDynamicsStatsAll.groupby(['bin_polarity'])

    ankitaVariable = activationDynamicsStatsAllGrouped["dynamics"].apply(np.array)
    #print(ankitaVariable)
    #print(np.vstack( ankitaVariable.iloc[0]))

    ankitaVariable = ankitaVariable.apply(lambda x: np.vstack(x))
    #print(ankitaVariable)
    newVariable = ankitaVariable.apply(lambda x : np.mean(x, axis=0))
    #print(type(newVariable))

    for items in newVariable.iteritems():
        #print(str(items[0]))
        plt.plot(range(len(items[1])), items[1], label=str(items[0]))
    
    plt.xlabel("iterations")
    plt.ylabel("number of active Nodes")
    plt.title("Activation dynamics over iterations for different polarities (diffusion trend)")
    plt.legend()
    plt.savefig(os.path.join(runBaseFolder, "activationDynamics.png"))
    plt.show()
    

    
    

