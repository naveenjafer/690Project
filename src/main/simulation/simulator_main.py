# The entry point for the simulation.

import json
import os
import sys

import src.main.utils.constants as consts

from src.main.network.uniformNetwork import generateNetwork
from src.main.newsArticles.articleGenerator import generateArticles

def networkCreator():
    networkFolder, nodeMap = generateNetwork(
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

    

if __name__ == "__main__":
    networkCreator()