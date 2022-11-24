# The entry point for the simulation.

import json
import os
import sys

import src.main.utils.constants as consts

from src.main.network.uniformNetwork import generateNetwork

def networkCreator():
    generateNetwork(
        consts.HOMOPHILY_INDEX,
        consts.NODE_COUNT,
        consts.EDGE_COUNT_MEAN,
        consts.EDGE_COUNT_VAR
    )

if __name__ == "__main__":
    networkCreator()