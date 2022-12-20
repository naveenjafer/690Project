import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import argparse
import os

def compare_adoptions_by_threshold_weights(cat_1_attractive_agg, cat_2_attractive_agg, cat_3_attractive_agg, active_counter_category, w1, w2, w3, outputFolder, proxyName):
    # plot lines
    plt.plot(cat_1_attractive_agg["polarity"], cat_1_attractive_agg[active_counter_category], label = "weight:"+w1)
    plt.plot(cat_2_attractive_agg["polarity"], cat_2_attractive_agg[active_counter_category], label = "weight:"+w2)
    plt.plot(cat_3_attractive_agg["polarity"], cat_3_attractive_agg[active_counter_category], label = "weight:"+w3)
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
    parser.add_argument("--model_w1_path")
    parser.add_argument("--model_w2_path")
    parser.add_argument("--model_w3_path")
    parser.add_argument("--w1")
    parser.add_argument("--w2")
    parser.add_argument("--w3")
    parser.add_argument("--w4")
    parser.add_argument("--outputFolder")
    args = parser.parse_args()

    df_1_connections = pd.read_csv(args.model_w1_path)
    df_2_connections = pd.read_csv(args.model_w2_path)
    df_3_connections = pd.read_csv(args.model_w3_path)

    agg_1 = get_agg_results_for_attractive_articles(df_1_connections, 0)
    agg_2 = get_agg_results_for_attractive_articles(df_2_connections, 0)
    agg_3 = get_agg_results_for_attractive_articles(df_3_connections, 0)

    if not os.path.isdir(args.outputFolder):
        os.mkdir(args.outputFolder)
    
    args.model_w1_path = args.model_w1_path.split("/")[-1]
    args.model_w2_path = args.model_w2_path.split("/")[-1]
    args.model_w3_path = args.model_w3_path.split("/")[-1]

    output_file_name = os.path.join(args.outputFolder, args.model_w1_path + "___" + args.model_w2_path)
    if not os.path.isdir(output_file_name):
        os.mkdir(output_file_name)

    compare_adoptions_by_threshold_weights(agg_1, agg_2, agg_3, "activeCongruentFinal", args.w1, args.w2, args.w3, output_file_name, "# of Congruent Active Nodes")
    compare_adoptions_by_threshold_weights(agg_1, agg_2, agg_3, "activeNonCongruentFinal", args.w1, args.w2, args.w3, output_file_name, "# of Non-Congruent Active Nodes")
    compare_adoptions_by_threshold_weights(agg_1, agg_2, agg_3, "activeCounter", args.w1, args.w2, args.w3, output_file_name,  "# of Active Nodes")
    compare_adoptions_by_threshold_weights(agg_1, agg_2, agg_3, "roundsCounter", args.w1, args.w2, args.w3, output_file_name, "# of timesteps to convergence" )
    compare_adoptions_by_threshold_weights(agg_1, agg_2, agg_3, "activationsPerRound", args.w1, args.w2, args.w3, output_file_name,  "# of activations/timestep")

    args = parser.parse_args()
