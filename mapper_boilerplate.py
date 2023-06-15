import kmapper as km
import numpy as np
import pandas as pd
import geopandas as gpd
from statistics import mode
import sys, os

cubes = 40    # number of intervals
overlap = 0.2 # how much they overlap
col_names = ["HVAP_pct", "WVAP_pct", "BVAP_pct", "ASIANVAP_pct", "GARCIA_G15_pct"] # variables we're passing to mapper
data_path = "data/Chicago_mayoral.csv"


df = pd.read_csv(data_path) # import the data

## select the columns we want to consider
input_df = df[col_names]
input_data = np.array(input_df)

proj_axis_idx = input_df.columns.get_loc("GARCIA_G15_pct")  # get index of the projection axis

## instantiate the mapper object (why is this even a class? nobody knows)
mapper_instance = km.KeplerMapper()

## project the data onto the % support for garcia axis, do not rescale output
## other projections are available
input_data_proj = mapper_instance.project(input_data, projection = [proj_axis_idx], scaler = None)

# cover =  # instantiate the cover

## this is the part that actually runs the mapper algorithm
## this is also the stage where you could specify an alternate clusterer 
output_graph = mapper_instance.map(input_data_proj, input_data, cover=km.Cover(n_cubes=cubes, perc_overlap=overlap))

mapper_instance.visualize(output_graph, 
    path_html = "outputs/area_vaps_garciasupport_mapper.html", 
    title="Chicago Mapper with Area and VAPs", 
    color_values = input_data[:,0], 
    color_function_name = "shape_area",
    X = input_data, 
    X_names = col_names)

mapper_instance.to_json(
    output_graph,
    input_data_proj,
    input_data,
    col_names,
    "data/chicago_mayoral.csv",
    "outputs/test.json"
)





