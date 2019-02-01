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

