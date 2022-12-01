
import json
import os
import sys
import src.main.utils.constants as consts

import random
import numpy as np

def randomArticleSampler(nodeGraph, articleList):

    samplerNodesList = []

    nodeList = list(nodeGraph.nodes(data=True))
    # if article["political_inclination"] it could be a neutral article and should be allowed to be sampled by both groups. 
    
    cat_0_nodes = [node for node in nodeList if node[1]["polInc"] == consts.INCLINATIONS[0]]
    cat_1_nodes = [node for node in nodeList if node[1]["polInc"] == consts.INCLINATIONS[1]]


    for article in articleList:
        if article["political_inclination"] == consts.INCLINATIONS[0]:
            samplerNodesList.append(random.sample(cat_0_nodes, consts.ARTICLE_SAMPLER_COUNT))
        else:
            samplerNodesList.append(random.sample(cat_1_nodes, consts.ARTICLE_SAMPLER_COUNT))

    return samplerNodesList