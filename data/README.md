# Data used for this project
A quick rundown:
 - `acs_tables/` all of the ACS 2018 detailed tables aggregated on blockgroups in Cook County used for this code
 - `precincts_shapefile/` shapefile for Chicago's 2012 precincts, ([source](https://data.cityofchicago.org/Facilities-Geographic-Boundaries/Boundaries-Ward-Precincts-2012-2022-/uvpq-qeeq))
 - `tl_2010_17031_bg10/`, `tl_2010_17031_tabblock10/` 2010 census blockgroup and block shapefiles for Cook County
 - `10decPL_chicago_blocks_raw.csv` tables P1, P2, P3, P4 and H1 from the 2010 PL redistricting data on blocks in Cook County
 - `10decPL_chicago_blocks_summary.csv` summarized race computed categories for population over 18 computed from above data. See `~/summarize_pl.py` for the computation.
 - `10decPL_chicago_blocks_summary_pct.csv` same but as percents of VAP
 - `acs_dataset_bgs.csv` several variables computed from `acs_tables` on blockgroups in Cook County. See `~/notebooks/get_new_acs_dataset.ipynb` for details
 - `Chicago_mayoral.csv` dataset with demographic and mayoral election columns with little known provenance
 - `chicago_mayoral_with_ro_pct.csv` above with runoff columns as percents of total vote
 - `enriched_chicago_mayoral.csv` above with normalized geographic variables + first round vote normalized so that Garcia vote percent and Rahm vote percent sum to 1
 - `chicago_mayoral_acs_counts.csv` above joined with variables from `acs_dataset_bgs.csv` after being disaggregated onto blocks then reaggregated onto precincts
 - `chicago_mayoral_acs_counts.csv` above with acs columns normalized in per case ways
 - `chicago_2015_mayoral_runoff.csv` clean election results from [the chicago election commission](https://chicagoelections.gov/en/election-results.html) for verifying the correctness of `Chicago_mayoral.csv`