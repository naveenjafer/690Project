
import json
import os
from platform import node
import sys
import src.main.utils.constants as consts

import random
import numpy as np
import datetime
import networkx as nx


def generateNetwork(homophilyIndex, nodeCount, edgeCountMean, edgeCountVar):

    #homophilyIndex = 0 for a mixture and 1 for a fully homophilic network
    networkConfig = {
        "homophilyIndex" : homophilyIndex,
        "nodeCount" : nodeCount, 
        "edgeCountMean" : edgeCountMean,
        "edgeCountVar" : edgeCountVar
    }

    edgeCountPerNode = np.random.normal(edgeCountMean, edgeCountVar, nodeCount)
    print("Edge count per node", edgeCountPerNode)
    nodeMap = {k:{"polInc" : 0, "following" : [], "activated" : False} for k in range(nodeCount)}
    nodeMap, pol_cat_0_users, pol_cat_1_users = politicalInclinationSampler(nodeMap)
    G = nx.DiGraph()
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
        G.add_node(nodeIndex, polInc=nodeMap[nodeIndex]["polInc"], activated=False)
        G.add_edges_from([(nodeIndex,node) for node in nodeMap[nodeIndex]["following"]])
    return writeNodeMapToDisk(G)
    

def writeNodeMapToDisk(node_graph):
    if not os.path.exists(consts.DATA_SIMULATION_FOLDER):
        os.mkdir(consts.DATA_SIMULATION_FOLDER)

    datestring = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    os.mkdir(os.path.join(consts.DATA_SIMULATION_FOLDER, datestring))
    node_graph_path = os.path.join(consts.DATA_SIMULATION_FOLDER, datestring, consts.NETWORK_ORIGINAL_FILENAME)
    nx.write_gml(node_graph, node_graph_path)
    return os.path.join(consts.DATA_SIMULATION_FOLDER, datestring), node_graph


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
    