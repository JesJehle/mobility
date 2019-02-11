import datetime
import json
from tools.api_keys import here_app_code, here_app_id
from tools.travel_time_pt import request_pt_route


# create pt routing response and save as json
date_time = datetime.datetime(2019, 2, 2, 10, 0)

Reuterbachgasse = [48.022917, 7.858326]
Hauptstrasse = [48.007457, 7.855260]

response = request_pt_route(here_app_id, here_app_code,date_time, Reuterbachgasse, Hauptstrasse)
with open('test_pt_route_simple.json', 'w') as f:
    json.dump(response, f)



# create buffered pt stations
import geopandas as gpd
station = gpd.read_file('../data/freiburg/grid_in_station_as_points.shp')
station = station[['station_id', 'geometry']]
station.crs = {'init': 'epsg:4326'}

random_point = station.sample(1).geometry

index_nearest = station.distance(random_point.iloc[0]).sort_values().head(20).index

station.iloc[index_nearest].plot()

station.iloc[index_nearest].to_file('data/test_sample_target_stations.shp')



# create stations_df

import json
from tools.travel_time_pt import extract_travel_times
with open("data/pt_test_route_simple.json", 'r') as f:
    response = json.load(f)

stations_df = extract_travel_times(response)
stations_df.to_csv('data/test_station_df.csv')

# create pt accessibility map


import geopandas as gpd
import pandas as pd
from tools.travel_time_pt import create_travel_time_df, get_accessibility_gdf
from pandas import DataFrame
import datetime

# target_stations = gpd.read_file('../data/freiburg/grid_in_station_as_points.shp')
# target_stations.crs = {'init': 'epsg:4326'}
# target_stations = target_stations[['station_id', 'geometry']]
# # origin = target_stations.sample(1).geometry
# date_time = datetime.datetime(2019, 3, 4, 10, 0)
# travel_time_test = create_travel_time_df(target_stations, date_time)
#
# travel_time_test.to_csv('../data/freiburg/pt_accessibility.csv')

travel_time_df = pd.read_csv('../data/freiburg/pt_accessibility.csv')
pt_accessibility_pgd = get_accessibility_gdf(travel_time_df)

pt_accessibility_pgd.to_file('../data/freiburg/pt_accessibility.shp')

