
import json
import os
import sys
import src.main.utils.constants as consts

import random
import numpy as np

def randomSampler(nodeMap, article_list):

    samplerNodesList = []

    # if article["political_inclination"] it could be a neutral article and should be allowed to be sampled by both groups. 

    
    for article in article_list:
        if article["political_inclination"] ==

    consts.ARTICLE_SAMPLER_COUNT