from tmap.tda import mapper, Filter
from tmap.tda.cover import Cover
from tmap.netx.SAFE import *
from tmap.tda.plot import vis_progressX, Color
import numpy as np
import pandas as pd
import geopandas as gpd
from statistics import mode
import matplotlib.pyplot as plt
import sys, os
import time
import sklearn

tm = mapper.Mapper(verbose=1)

data_path = "data/enriched_chicago_mayoral.csv"
df = pd.read_csv(data_path) 

cubes = 40   # number of intervals
overlap = 0.6 # how much they overlap
clusterer = sklearn.cluster.DBSCAN()
clusterer.metric = "euclidean"

fname_suffix = "15runoff+geog"
html_path =  f"outputs/chicago_{fname_suffix}.html"
json_path  = f"outputs/chicago_{fname_suffix}.json"
title = "Chicago '15 Mayoral Runoff w/ Geog. Vars (Log Area)"

input_col_names = ["RO_GARCIA_G15_pct","HVAP_pct", "BVAP_pct", "WVAP_pct", "ASIANVAP_pct", "normalized_log_area"] + [col for col in df.columns if "K_pct" in col or col == "200K_MORE_pct" or "normalized_centroid" in col] # variables we're passing to mapper
color_col_names = input_col_names
proj_axis_idx = input_col_names.index("RO_GARCIA_G15_pct")


## select the columns we want to consider
input_df = df[input_col_names].copy()
input_data = np.array(input_df)
# input_data = np.random.uniform(size=(2000,2))
# input_data = np.hstack((input_data, (np.transpose(input_data)[0]**2 + np.transpose(input_data)[1]**2)[:, None]))

## project the data onto the % support for garcia axis, do not rescale output
## other projections are available
lens = [Filter.Filters(components = [proj_axis_idx])]
input_data_proj = tm.filter(input_data, lens)
cover           = Cover(projected_data = input_data_proj, resolution=cubes, overlap=overlap)

# cover =  # instantiate the cover

## this is the part that actually runs the mapper algorithm
## this is also the stage where you could specify an alternate clusterer 
output_graph = tm.map(data=input_data, clusterer=clusterer, cover=cover)

# tm.visualize(output_graph, 
#     path_html = html_path,
#     title=title, 
#     color_values = list(df[color_col_names]),
#     color_function_name = color_col_names, 
#     custom_tooltips = np.array([f"Ward {int(prct[1]['ward'])} Precinct {int(prct[1]['precinct'])}" for prct in df.iterrows()]),
#     X = input_data, 
#     X_names = input_col_names)

# km.adapter.to_json(
#     output_graph,
#     input_data_proj,
#     input_data,
#     input_col_names,
#     data_path,
#     json_path,
# )

safe_scores = SAFE_batch(output_graph, metadata=input_data, n_iter=1000,_mode='enrich', verbose=1)
safe_summary = get_SAFE_summary(graph=output_graph, metadata=input_data, safe_scores=safe_scores,
                                n_iter=1000, p_value=0.01)
