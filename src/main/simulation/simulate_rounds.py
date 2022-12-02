import networkx as nx
import copy
import src.main.utils.constants as consts

def roundsSimulator(nodeGraph, articleList, samplers):

    activationStats = []

    print("samplers")
    #print(samplers)
    polIncGetter, weightageCongruentGetter, weightageNonCongruentGetter, thresholdAlphaGetter = getStaticAttributeGetters(nodeGraph)
    for index, article in enumerate(articleList):
        if index % 50 == 0:
            print("[SIMULATION-INFO]: Spreading Article ", index, " of ", len(articleList))
        article_political_inclination = article["political_inclination"]
        article_attractiveness = article["attractiveness"]
        article_polarity = article["polarity"]

        nodeGraphRound = copy.deepcopy(nodeGraph)
        # activate the samplers before iterating
        nodeEditGraph = {}
        for nodeIndex in samplers[index]:

            nodeEditGraph[nodeIndex[0]] = True
        nx.set_node_attributes(nodeGraphRound, nodeEditGraph, 'activated')

        roundsCounter = 0

        while True:
            newActivations = 0
            for nodeIndex in range(consts.NODE_COUNT):

                P_a = None # comes from article
                P_n = None # comes from user user interaction
                P_p = None # comes from article user interaction

                P_a = article["attractiveness"]

                # start of calculating P_n 
                activationStateGetter = nx.get_node_attributes(nodeGraphRound, "activated")
                
                if activationStateGetter[nodeIndex] == True:
                    # the node is already activated
                    continue
                
                followingNodes = nodeGraphRound.neighbors(nodeIndex)
                nodePoliticalInc = polIncGetter[nodeIndex]

                countCongActive, countNonCongActive, countCong, countNonCong = 0,0,0,0

                for followingNodeIndex in followingNodes:
                    if polIncGetter[followingNodeIndex] == nodePoliticalInc:
                        countCong += 1
                        if activationStateGetter[followingNodeIndex] == True:
                            countCongActive += 1
                    
                    else:
                        countNonCong += 1
                        if activationStateGetter[followingNodeIndex] == True:
                            countNonCongActive += 1

                P_n = ((countCongActive * weightageCongruentGetter[followingNodeIndex]) + (countNonCongActive * weightageNonCongruentGetter[followingNodeIndex])) / ((countCong * weightageCongruentGetter[followingNodeIndex]) + (countNonCong * weightageNonCongruentGetter[followingNodeIndex]))

                # end of calculating P_n

                # start of calculating P_p
                if article["political_inclination"] == polIncGetter[nodeIndex]:
                    P_p = article["polarity"]
                else:
                    P_p = 1-article["polarity"]
                # end of calculating P_p

                if P_a * P_n * P_p > thresholdAlphaGetter[nodeIndex]:
                    nx.set_node_attributes(nodeGraphRound, {nodeIndex : True}, 'activated')
                    newActivations += 1
            roundsCounter += 1

            #print("[SIMULATION-INFO]: Activated ", newActivations, " nodes in round ", roundsCounter)
            if newActivations == 0:
                # round is complete as there is equillibrium in the network, propogate the next article through network
                break
        
        # after completion of a round, glean insights to track and plot stats

        articleLevelStats = {}
        articleLevelStats["initialActive"] = len(samplers[index])
        articleLevelStats["attractiveness"] = article["attractiveness"]
        articleLevelStats["polarity"] = article["polarity"]
        articleLevelStats["political_inclination"] = article["political_inclination"]

        # prettu much just collating information for easy analysis.

        activationStateGetter = nx.get_node_attributes(nodeGraphRound, "activated")
        activeCounter = 0
        activeCongruentInitial = articleLevelStats["initialActive"]
        activeNonCongruentInitial = 0
        activeCongruentFinal = 0
        activeNonCongruentFinal = 0

        for nodeIndex in range(consts.NODE_COUNT):
            if activationStateGetter[nodeIndex] == True:
                if article["political_inclination"] == polIncGetter[nodeIndex]:
                    activeCongruentFinal += 1
                else:
                    activeNonCongruentFinal += 1
        #print(activeCongruentFinal, activeNonCongruentFinal)
        activeCounter = activeCongruentFinal + activeNonCongruentFinal
        articleLevelStats["endOfRoundStats"] = {}
        articleLevelStats["endOfRoundStats"]["activeCongruentInitial"] = activeCongruentInitial
        articleLevelStats["endOfRoundStats"]["activeNonCongruentInitial"] = activeNonCongruentInitial
        articleLevelStats["endOfRoundStats"]["activeCongruentFinal"] = activeCongruentFinal
        articleLevelStats["endOfRoundStats"]["activeNonCongruentFinal"] = activeNonCongruentFinal
        articleLevelStats["endOfRoundStats"]["activeCounter"] = activeCounter
        activationStats.append(articleLevelStats)
    return activationStats

def getStaticAttributeGetters(nodeGraph):
    polIncGetter = nx.get_node_attributes(nodeGraph, 'polInc')
    weightageCongruentGetter = nx.get_node_attributes(nodeGraph, 'weightageCongruent')
    weightageNonCongruentGetter = nx.get_node_attributes(nodeGraph, 'weightageNonCongruent')
    thresholdAlphaGetter = nx.get_node_attributes(nodeGraph, 'thresholdAlpha')

    return polIncGetter, weightageCongruentGetter, weightageNonCongruentGetter, thresholdAlphaGetter