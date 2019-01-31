import datetime
import json
from tools.api_keys import here_app_code, here_app_id
from tools.travel_time_pt import request_pt_route


# create pt routing response and save as json
date_time = datetime.datetime(2019, 2, 2, 10, 0)

Reuterbachgasse = [48.022917, 7.858326]
Hauptstrasse = [48.007457, 7.855260]

response = request_pt_route(here_app_id, here_app_code,date_time, Reuterbachgasse, Hauptstrasse)
with open('pt_test_route_simple.json', 'w') as f:
    json.dump(response, f)



# create buffered pt stations
import geopandas as gpd
station = gpd.read_file('data/freiburg/grid_in_station_as_points.shp')
station = station[['station_id', 'geometry']]
station.crs = {'init': 'epsg:4326'}

crs_meters = {'init': 'epsg:25832'}
station_buffer = station.to_crs(crs_meters)
station_buffer['geometry'] = station_buffer.buffer(50)

station_buffer.to_file('tests/data/test_target_stations_buffer_50.shp')