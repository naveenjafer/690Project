# The entry point for the simulation.

import json
import os
import sys

import src.main.utils.constants as consts

from src.main.network.uniformNetwork import generateNetwork
from src.main.newsArticles.articleGenerator import generateArticles
from src.main.network.articleSampler import sameInclinationSampler, staggeredInclinationSampler
from src.main.simulation.simulate_rounds import roundsSimulator
from src.main.analysis.endOfRoundAnalysis import analyzeHistograms, analyzeHistogramsAggregated  
import networkx as nx
import matplotlib.pyplot as plt
import datetime

NUMBER_OF_RUNS = 10

def networkCreator():
    # generate network
    dateString = datetime.datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
    config = [item for item in dir(consts) if not item.startswith("__")]
    if not os.path.exists(consts.DATA_SIMULATION_FOLDER):
        os.mkdir(consts.DATA_SIMULATION_FOLDER)
    
    if not os.path.exists(os.path.join(consts.DATA_SIMULATION_FOLDER, dateString)):
        os.mkdir(os.path.join(consts.DATA_SIMULATION_FOLDER, dateString))

    with open(os.path.join(consts.DATA_SIMULATION_FOLDER, dateString, "config.json"), "w") as f:
        json.dump(config, f, indent=4)

    activationStatsAll = []
    for i in range(NUMBER_OF_RUNS):
        print(f"************************ RUN {i} of {NUMBER_OF_RUNS}*********************")
        networkFolder, nodeGraph = generateNetwork(
            consts.HOMOPHILY_INDEX,
            consts.NODE_COUNT,
            consts.EDGE_COUNT_MEAN,
            consts.EDGE_COUNT_VAR,
            dateString,
            i
        )
        
        articleList = generateArticles(
            consts.ARTICLE_ATTRACTIVENESS_RANGE,
            consts.ARTICLE_ATTRACTIVENESS_MEAN,
            consts.ARTICLE_ATTRACTIVENESS_VAR,
            consts.ARTICLE_POLARITY_RANGE,
            consts.ARTICLE_POLARITY_MEAN,
            consts.ARTICLE_POLARITY_VAR,
            consts.ARTICLE_COUNT,
            networkFolder
        )

        samplers = staggeredInclinationSampler(nodeGraph, articleList)

        activationStats = roundsSimulator(
            nodeGraph,
            articleList,
            samplers
        )
        activationStatsAll.append(activationStats)
    
    #analyzeHistograms(activationStatsAll[0])

    analyzeHistogramsAggregated(activationStatsAll, consts.HOMOPHILY_INDEX,  os.path.join(consts.DATA_SIMULATION_FOLDER, dateString))
    return networkFolder, articleList


def visualize_network(network_path):
    G = nx.read_gml(network_path)
    political_map = nx.get_node_attributes(G, "polInc")
    colors = [consts.COLOR_MAP[political_inclination] for node, political_inclination in political_map.items()]
    nx.draw_networkx(G, node_color=colors, with_labels=True)
    plt.show()

if __name__ == "__main__":
    networkFolder,  article_list = networkCreator()
    # visualize graph
    visualize_network(os.path.join(networkFolder, consts.NETWORK_ORIGINAL_FILENAME))
