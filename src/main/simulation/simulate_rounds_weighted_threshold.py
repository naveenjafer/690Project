import networkx as nx
import copy
import src.main.utils.constants as consts
from src.main.utils.helpers import get_truncated_normal

def roundsSimulatorWeightedThreshold(nodeGraph, articleList, samplers):

    activationStats = []
    p_a_avg, p_n_avg, p_p_avg, avgCounter = 0,0,0,0
    p_list = []
    polIncGetter, weightageCongruentGetter, weightageNonCongruentGetter, thresholdAlphaGetter = getStaticAttributeGetters(nodeGraph)
    activationDynamicsStats = []
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
        activationsPerRound = []
        numberOfActivations = len(samplers[index])
        activationsPerRound.append(numberOfActivations)
        while True:
            newActivations = 0
            for nodeIndex in range(consts.NODE_COUNT):
                activationStateGetter = nx.get_node_attributes(nodeGraphRound, "activated")   
                if activationStateGetter[nodeIndex] == True:
                    # the node is already activated
                    continue
                avgCounter += 1
                P_a = None # comes from article
                P_n = None # comes from user user interaction
                P_p = None # comes from article user interaction

                P_a = article["attractiveness"]
                p_a_avg += P_a

                # start of calculating P_n 
                P_n = calculate_p_n_mode_1(activationStateGetter, nodeGraphRound, nodeIndex, polIncGetter, weightageCongruentGetter, weightageNonCongruentGetter)
                
                # end of calculating P_n
                if P_n == 0:
                    # implies that this node is not exposed to this article
                    continue
                p_n_avg += P_n
                # start of calculating P_p
                P_p = calculate_p_p_mode_1(article, polIncGetter, nodeIndex)
                # end of calculating P_p
                p_p_avg += P_p

                p_list.append([P_a, P_p, P_n])
             

                if  consts.WEIGHT_P_N * P_n + consts.WEIGHT_P_P * P_p > thresholdAlphaGetter[nodeIndex]:
                    nx.set_node_attributes(nodeGraphRound, {nodeIndex : True}, 'activated')
                    newActivations += 1
                    numberOfActivations += 1
            roundsCounter += 1
            
            activationsPerRound.append(numberOfActivations)
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

        articleLevelStatsCopyForDynamics = copy.deepcopy(articleLevelStats) # copying this to avoid rewriting
        articleLevelStatsCopyForDynamics["dynamics"] = activationsPerRound
        activationDynamicsStats.append(articleLevelStatsCopyForDynamics) 

        # pretty much just collating information for easy analysis.

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
        articleLevelStats["endOfRoundStats"]["roundsCounter"] = roundsCounter
        articleLevelStats["endOfRoundStats"]["activeCongruentInitial"] = activeCongruentInitial
        articleLevelStats["endOfRoundStats"]["activeNonCongruentInitial"] = activeNonCongruentInitial
        articleLevelStats["endOfRoundStats"]["activeCongruentFinal"] = activeCongruentFinal
        articleLevelStats["endOfRoundStats"]["activeNonCongruentFinal"] = activeNonCongruentFinal
        articleLevelStats["endOfRoundStats"]["activeCounter"] = activeCounter
        articleLevelStats["endOfRoundStats"]["activationsPerRound"] = activeCounter/roundsCounter
        activationStats.append(articleLevelStats)
    p_a_avg, p_n_avg, p_p_avg = p_a_avg/avgCounter, p_n_avg/avgCounter, p_p_avg/avgCounter
    p_avgs = [p_a_avg, p_n_avg, p_p_avg]

    return activationDynamicsStats, activationStats, p_avgs, p_list

def getStaticAttributeGetters(nodeGraph):
    polIncGetter = nx.get_node_attributes(nodeGraph, 'polInc')
    weightageCongruentGetter = nx.get_node_attributes(nodeGraph, 'weightageCongruent')
    weightageNonCongruentGetter = nx.get_node_attributes(nodeGraph, 'weightageNonCongruent')
    thresholdAlphaGetter = nx.get_node_attributes(nodeGraph, 'thresholdAlpha')
    return polIncGetter, weightageCongruentGetter, weightageNonCongruentGetter, thresholdAlphaGetter

def calculate_p_n_mode_1(activationStateGetter, nodeGraphRound, nodeIndex, polIncGetter, weightageCongruentGetter, weightageNonCongruentGetter):
            
      
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
    return P_n

def calculate_p_n_without_congruency(activationStateGetter, nodeGraphRound, nodeIndex):
    followingNodes = nodeGraphRound.neighbors(nodeIndex)
    countNbrsActive = 0
    totalNbrs = 0
    for followingNodeIndex in followingNodes:
        if activationStateGetter[followingNodeIndex] == True:
            countNbrsActive += 1
        totalNbrs += 1
    P_n = countNbrsActive / totalNbrs
    return P_n

def calculate_p_p_mode_1(article, polIncGetter, nodeIndex):
    if article["political_inclination"] == polIncGetter[nodeIndex]:
        P_p = article["polarity"]
    else:
        P_p = 1-article["polarity"]
    return P_p

def calculate_p_p_mode_2(article, polIncGetter, nodeIndex):
    article_polarity_gap = article["polarity"] - (1 - article["polarity"])
    article_polarity_gap_offsetted = article_polarity_gap * consts.USER_ARTICLE_OFFSET_FACTOR
    
    if article["political_inclination"] == polIncGetter[nodeIndex]:
        P_p_mean = article["polarity"] - article_polarity_gap_offsetted
        lowerBound = 0.5
        upperBound = 1
    else:
        P_p_mean = 1-article["polarity"] + article_polarity_gap_offsetted
        upperBound = 0.5
        lowerBound = 0
    
    articleUser_norm = get_truncated_normal(
            mean=P_p_mean,
            sd=consts.USER_ARTICLE_VAR ** 0.5,
            low=lowerBound,
            upp=upperBound
        )
    P_p = articleUser_norm.rvs(1)[0]
    return P_p

