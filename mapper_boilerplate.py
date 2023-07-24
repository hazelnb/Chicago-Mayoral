import kmapper as km
import numpy as np
import pandas as pd
import geopandas as gpd
from statistics import mode
import matplotlib.pyplot as plt
import sys, os
import time
import sklearn

data_path = "data/enriched_chicago_mayoral.csv"
df = pd.read_csv(data_path) 

cubes = 40   # number of intervals
overlap = 0.6 # how much they overlap
cover     = km.Cover(n_cubes=cubes, perc_overlap=overlap)
clusterer = sklearn.cluster.MiniBatchKMeans()

fname_suffix = "15runoff+geog"
html_path =  f"outputs/chicago_{fname_suffix}.html"
json_path  = f"outputs/chicago_{fname_suffix}.json"
title = "Chicago '15 Mayoral Runoff w/ Geog. Vars (Log Area)"

input_col_names = ["RO_GARCIA_G15_pct","HVAP_pct", "BVAP_pct", "WVAP_pct", "ASIANVAP_pct", "normalized_log_area"] + [col for col in df.columns if "K_pct" in col or col == "200K_MORE_pct" or "normalized_centroid" in col] # variables we're passing to mapper
color_col_names = input_col_names #let's us color by columns we're not running mapper on
proj_axis_idx = input_col_names.index("RO_GARCIA_G15_pct")


## select the columns we want to consider
input_df = df[input_col_names].copy()
input_data = np.array(input_df)

## instantiate the mapper object (why is this even a class? nobody knows)
mapper_instance = km.KeplerMapper()

## project the data onto the % support for garcia axis, do not rescale output
## other projections are available
input_data_proj = mapper_instance.project(input_data, projection = [proj_axis_idx], scaler = None)

## this is the part that actually runs the mapper algorithm
## this is also the stage where you could specify an alternate clusterer 
output_graph = mapper_instance.map(input_data_proj, input_data, clusterer=clusterer, cover=cover)

mapper_instance.visualize(output_graph, 
    path_html = html_path,
    title=title, 
    color_values = list(df[color_col_names]),
    color_function_name = color_col_names, 
    custom_tooltips = np.array([f"Ward {int(prct[1]['ward'])} Precinct {int(prct[1]['precinct'])}" for prct in df.iterrows()]),
    X = input_data, 
    X_names = input_col_names)

km.adapter.to_json(
    output_graph,
    input_data_proj,
    input_data,
    input_col_names,
    data_path,
    json_path,
)





