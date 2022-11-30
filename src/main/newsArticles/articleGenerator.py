import os
import json
import random
import numpy as np
from src.main.utils.helpers import get_truncated_normal
import src.main.utils.constants as consts

def generateArticles(
        article_attractiveness_range,
        article_attractiveness_mean,
        article_attractiveness_var,
        article_polarity_range,
        article_polarity_mean,
        article_polarity_var,
        article_count,
        networkFolder
    ):

    attractiveness_norm = get_truncated_normal(
            mean=article_attractiveness_mean,
            sd=article_attractiveness_var ** 0.5,
            low=article_attractiveness_range[0],
            upp=article_attractiveness_range[1]
        )
    
    polarity_norm = get_truncated_normal(
            mean=article_polarity_mean,
            sd=article_polarity_var ** 0.5,
            low=article_polarity_range[0],
            upp=article_polarity_range[1]
        )

    political_inclination = [random.sample(consts.INCLINATIONS,1)[0] for i in range(article_count)]
    

    attractiveness_values = attractiveness_norm.rvs(article_count)
    polarity_values = polarity_norm.rvs(article_count)

    article_list = list()
    for index in range(article_count):
        article_list.append({
            "attractiveness" : attractiveness_values[index], 
            "polarity" : polarity_values[index], 
            "political_inclination" : political_inclination[index]})

    with open(os.path.join(networkFolder, consts.ARTICLES_FILENAME), "w") as f:
        json.dump(article_list, f, indent=4)

    print("[INFO] Articles generated and stored at ", os.path.join(networkFolder, consts.ARTICLES_FILENAME))
    return article_list

    
        

