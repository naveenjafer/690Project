# The entry point for the simulation.

import json
import os
import sys

import src.main.utils.constants as consts

from src.main.network.uniformNetwork import generateNetwork
from src.main.newsArticles.articleGenerator import generateArticles
import networkx as nx
import matplotlib.pyplot as plt

def networkCreator():
    networkFolder, nodeGraph = generateNetwork(
        consts.HOMOPHILY_INDEX,
        consts.NODE_COUNT,
        consts.EDGE_COUNT_MEAN,
        consts.EDGE_COUNT_VAR
    )
    
    article_list = generateArticles(
        consts.ARTICLE_ATTRACTIVENESS_RANGE,
        consts.ARTICLE_ATTRACTIVENESS_MEAN,
        consts.ARTICLE_ATTRACTIVENESS_VAR,
        consts.ARTICLE_POLARITY_RANGE,
        consts.ARTICLE_POLARITY_MEAN,
        consts.ARTICLE_POLARITY_VAR,
        consts.ARTICLE_COUNT,
        networkFolder
    )
    return networkFolder, article_list

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