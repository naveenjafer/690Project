The repo for the final Project for 690.

Please do the following to be able to run our code.

1. Switch to the graphviz branch

2. Setup a venv and run 
`pip install -r requirements.txt`

3. Set python path for successful imports
`export PYTHONPATH='.'`

# Running the simulation
As of now, creating a network with a configurable set of parameters is done. The actual simulation needs to be done. Run the following to create the network.

To run the threshold model, use 
`python3 src/main/simulation/simulator_main.py --algoType threshold`

To run the weighted threshold, use
`python3 src/main/simulation/simulator_main.py --algoType weighted_threshold`

To run the baseline, use
`python3 src/main/simulation/simulator_main.py --algoType baseline`

The results are generated in data_simulation folder with a timestamp. All the graphs presented in the paper get generated in the respective folders.



