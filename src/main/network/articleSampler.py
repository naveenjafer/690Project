
import json
import os
import sys
import src.main.utils.constants as consts

import random
import numpy as np

def sameInclinationSampler(nodeGraph, articleList):
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

def staggeredInclinationSampler(nodeGraph, articleList):
    samplerNodesList = []
    nodeList = list(nodeGraph.nodes(data=True))

    cat_0_nodes = [node for node in nodeList if node[1]["polInc"] == consts.INCLINATIONS[0]]
    cat_1_nodes = [node for node in nodeList if node[1]["polInc"] == consts.INCLINATIONS[1]]

    # the mapping follows the method used here - https://stackoverflow.com/a/5732390 
    for article in articleList:
        slope = (consts.ARTICLE_SAMPLER_COUNT - int(consts.ARTICLE_SAMPLER_COUNT/2)) / (consts.ARTICLE_POLARITY_RANGE[1] - consts.ARTICLE_POLARITY_RANGE[0])
        output = int(consts.ARTICLE_SAMPLER_COUNT/2) + slope * (article["polarity"] - consts.ARTICLE_POLARITY_RANGE[0])
        output = int(output)
        if output < consts.ARTICLE_SAMPLER_COUNT:
            output += consts.ARTICLE_SAMPLER_COUNT_OFFSET
        #print(output)
        assert output >= int(consts.ARTICLE_SAMPLER_COUNT/2) and output <= consts.ARTICLE_SAMPLER_COUNT

        samplerNodesBuilder = []
        samplerNodesBuilder += random.sample(cat_0_nodes, output)
        samplerNodesBuilder += random.sample(cat_1_nodes, consts.ARTICLE_SAMPLER_COUNT - output)
        
        samplerNodesList.append(samplerNodesBuilder)
    #quit(1)
    return samplerNodesList


