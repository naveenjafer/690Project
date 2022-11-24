# The entry point for the simulation.

import json
import os
import sys
from src.main.utils.constants import config_consts, consts

from src.main.network.uniformNetwork import generateNetwork

def networkCreator():
    generateNetwork(
        config_consts["homophilyIndex"], 
        config_consts["nodeCount"], 
        config_consts["edgeCountMean"],
        config_consts["edgeCountVar"])


if __name__ == "__main__":
    networkCreator()