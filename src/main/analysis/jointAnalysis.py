import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import argparse
import os

def compare_adoptions_by_homophily_index(cat_1_attractive_agg, cat_2_attractive_agg, active_counter_category, mu1, mu2, outputFolder, proxyName):
    # plot lines
    plt.plot(cat_1_attractive_agg["polarity"], cat_1_attractive_agg[active_counter_category], label = "homophily index:"+mu1)
    plt.plot(cat_2_attractive_agg["polarity"], cat_2_attractive_agg[active_counter_category], label = "homophily index:"+mu2)
    plt.xlabel("polarity")
    plt.title(f"Polarity vs {proxyName}")
    plt.ylabel(active_counter_category)
    plt.legend()
    plt.savefig(os.path.join(outputFolder, f"polarity_{active_counter_category}.png"))
    plt.show()

def get_agg_results_for_attractive_articles(df, attractiveness_factor):
    bins = []
    bin_start, bin_end = 0,1
    total_polarity_bins = 20
    polarity_bin_len = (bin_end-bin_start)/total_polarity_bins
    bin_iterator = 0.5
    while bin_iterator<=bin_end:
        bins.append(bin_iterator)
        bin_iterator=round(bin_iterator+polarity_bin_len,3)

    cat_df_attractive = df[df["attractiveness"] >= attractiveness_factor]
    cat_df_attractive['bin_polarity'] = pd.cut(cat_df_attractive['polarity'], bins)
    cat_df_attractie_agg = cat_df_attractive.groupby(['bin_polarity']).mean()
    return cat_df_attractie_agg

if __name__ == "__main__":
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--model1_path")
    parser.add_argument("--model2_path")
    parser.add_argument("--mu1")
    parser.add_argument("--mu2")
    parser.add_argument("--outputFolder")
    args = parser.parse_args()

    df_1_connections = pd.read_csv(args.model1_path)
    df_2_connections = pd.read_csv(args.model2_path)

    agg_1 = get_agg_results_for_attractive_articles(df_1_connections, 0)
    agg_2 = get_agg_results_for_attractive_articles(df_2_connections, 0)

    if not os.path.isdir(args.outputFolder):
        os.mkdir(args.outputFolder)
    
    args.model1_path = args.model1_path.split("/")[-1]
    args.model2_path = args.model2_path.split("/")[-1]
    if not os.path.isdir(os.path.join(args.outputFolder, args.model1_path + "___" + args.model2_path)):
        os.mkdir(os.path.join(args.outputFolder, args.model1_path + "___" + args.model2_path))

    compare_adoptions_by_homophily_index(agg_1, agg_2, "activeCongruentFinal", args.mu1, args.mu2, os.path.join(args.outputFolder, args.model1_path + "___" + args.model2_path), "# of Congruent Active Nodes")
    compare_adoptions_by_homophily_index(agg_1, agg_2, "activeNonCongruentFinal", args.mu1, args.mu2, os.path.join(args.outputFolder, args.model1_path + "___" + args.model2_path), "# of Non-Congruent Active Nodes")
    compare_adoptions_by_homophily_index(agg_1, agg_2, "activeCounter", args.mu1, args.mu2, os.path.join(args.outputFolder, args.model1_path + "___" + args.model2_path),  "# of Active Nodes")
    compare_adoptions_by_homophily_index(agg_1, agg_2, "roundsCounter", args.mu1, args.mu2, os.path.join(args.outputFolder, args.model1_path + "___" + args.model2_path), "# of timesteps to convergence" )
    compare_adoptions_by_homophily_index(agg_1, agg_2, "activationsPerRound", args.mu1, args.mu2, os.path.join(args.outputFolder, args.model1_path + "___" + args.model2_path),  "# of activations/timestep")

    args = parser.parse_args()
