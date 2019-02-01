

def test_format_time_for_request():
	from tools.travel_time_pt import format_time_for_request
	import datetime
	time_input = datetime.datetime(2019, 2, 2, 10, 0)
	time_output = '2019-02-02T10:00:00'
	assert format_time_for_request(time_input) == time_output



def test_request_pt_route():
	import datetime
	from tools.api_keys import here_app_code, here_app_id
	from tools.travel_time_pt import request_pt_route

	date_time = datetime.datetime(2019, 2, 2, 10, 0)
	start = [48.022917, 7.858326]
	end = [48.007457, 7.855260]

	route = request_pt_route(here_app_id, here_app_code, date_time, start, end)
	assert isinstance(route['Res'], dict)


def test_extract_travel_times():
	import json
	from pandas import DataFrame
	from tools.travel_time_pt import extract_travel_times
	with open("data/test_pt_route_simple.json", 'r') as f:
		response = json.load(f)

	stations_df = extract_travel_times(response)

	assert isinstance(stations_df, DataFrame)



def test_find_reached_stations():
	from tools.travel_time_pt import find_reached_stations
	from geopandas import read_file
	import pandas as pd

	target_stations = read_file('data/test_sample_target_stations.shp')
	target_stations.crs = {'init': 'epsg:4326'}
	stations_df = pd.read_csv('data/test_station_df.csv')
	found_stations = find_reached_stations(stations_df, target_stations_buffer, 50)
	assert isinstance(found_stations, list)




from geopandas import read_file
from tools.travel_time_pt import request_pt_route, extract_travel_times, add_to_dict, find_reached_stations
from tools.api_keys import here_app_code, here_app_id
import datetime

# get targets

target_stations = read_file('../data/freiburg/grid_in_station_as_points.shp')
target_stations.crs = {'init': 'epsg:4326'}
target_stations = target_stations[['station_id', 'geometry']]
# get departure point


departure = target_stations.sample(1).geometry
date_time = datetime.datetime(2019, 2, 2, 10, 0)
times_dic = {}
last_index = 0
buffer = 50
while len(target_stations) > 0:


	index_farest = target_stations.distance(departure.iloc[0]).sort_values(ascending=False).head(1).index
	farest_y = target_stations.loc[index_farest].geometry.centroid.y
	farest_x = target_stations.loc[index_farest].geometry.centroid.x

	pt_request = request_pt_route(here_app_id, here_app_code, date_time, [departure.y.iloc[0], departure.x.iloc[0]], [farest_y.iloc[0], farest_x.iloc[0]], False)
	travel_times = extract_travel_times(pt_request)

	times_dic = add_to_dict(times_dic, travel_times['travel_time'].tolist(), travel_times['station'].tolist())
	if last_index == index_farest:
		buffer = buffer + 50
	else:
		buffer = 50

	reached_stations = find_reached_stations(travel_times, target_stations, buffer)

	target_stations = target_stations[~target_stations['station_id'].isin(reached_stations)]
	last_index = index_farest
	print(len(target_stations), ' stations left')
	print(buffer, ' buffer')
	print(target_stations)





