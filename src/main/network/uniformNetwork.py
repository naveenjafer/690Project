
import json
import os
from platform import node
import sys
import src.main.utils.constants as consts

import random
import numpy as np
import datetime

def generateNetwork(homophilyIndex, nodeCount, edgeCountMean, edgeCountVar):

    #homophilyIndex = 0 for a mixture and 1 for a fully homophilic network
    networkConfig = {
        "homophilyIndex" : homophilyIndex,
        "nodeCount" : nodeCount, 
        "edgeCountMean" : edgeCountMean,
        "edgeCountVar" : edgeCountVar
    }

    edgeCountPerNode = np.random.normal(edgeCountMean, edgeCountVar, nodeCount)

    nodeMap = {k:{"polInc" : 0, "following" : [], "activated" : False} for k in range(nodeCount)}
    nodeMap, pol_cat_0_users, pol_cat_1_users = politicalInclinationSampler(nodeMap)

    print("[INFO] Assigned political identities")
    # to do, for each user, use the corresponding entry from edgeCountPerNode to follow other users
    for nodeIndex in range(nodeCount):
        if nodeIndex % 100 == 0:
            print("[INFO] Completed configuring ", nodeIndex, " users out of ", nodeCount)
        cat_0_weight = 0.5
        cat_1_weight = 0.5

        if nodeMap[nodeIndex]["polInc"] == consts.INCLINATIONS[0]:
            cat_0_weight += homophilyIndex*0.5
            cat_1_weight -= homophilyIndex*0.5
        
        else:
            cat_0_weight -= homophilyIndex*0.5
            cat_1_weight += homophilyIndex*0.5
        
        pol_cat_0_users_following = random.sample(pol_cat_0_users, int( edgeCountPerNode[nodeIndex] * cat_0_weight))
        pol_cat_1_users_following = random.sample(pol_cat_1_users, int( edgeCountPerNode[nodeIndex] * cat_1_weight))

        if len(pol_cat_0_users_following) + len(pol_cat_1_users_following) <= edgeCountPerNode[nodeIndex]:
            ...
            # need to add the condition to make sure that the count is exact, will not affect results much at the moment.
        
        nodeMap[nodeIndex]["following"] = pol_cat_0_users_following + pol_cat_1_users_following

    return writeNodeMapToDisk(nodeMap)
    
def writeNodeMapToDisk(nodeMap):
    if not os.path.exists(consts.DATA_SIMULATION_FOLDER):
        os.mkdir(consts.DATA_SIMULATION_FOLDER)

    datestring = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    os.mkdir(os.path.join(consts.DATA_SIMULATION_FOLDER, datestring))

    with open(os.path.join(consts.DATA_SIMULATION_FOLDER, datestring, consts.NETWORK_ORIGINAL_FILENAME), "w") as f:
        json.dump(nodeMap, f, indent=4)
    return os.path.join(consts.DATA_SIMULATION_FOLDER, datestring)


def politicalInclinationSampler(nodeMap, skew=0.5):

    nodeList = list(nodeMap.keys())
    nodeInclinationsList = []
    inclination_0_users = random.sample(nodeList, int(len(nodeList)*skew))
    inclination_1_users = list(set(nodeList) - set(inclination_0_users))

    for node in inclination_0_users:
        nodeMap[node]["polInc"] = consts.INCLINATIONS[0]

    for node in inclination_1_users:
        nodeMap[node]["polInc"] = consts.INCLINATIONS[1]

    return nodeMap, inclination_0_users, inclination_1_users

    #assign political inclinations
    