
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
	with open("data/pt_test_route_simple.json", 'r') as f:
		response = json.load(f)

	stations_df = extract_travel_times(response)

	assert isinstance(stations_df, DataFrame)







from geopandas import GeoDataFrame, sjoin, read_file
from shapely.geometry import Point

read_file('data/')


def find_reached_stations(reached_stations_df, target_stations_buffer, buffer):
	mean_travel_time = reached_stations_df.groupby('station').mean()
	geometry = [Point(xy) for xy in zip(mean_travel_time.x, mean_travel_time.y)]
	mean_travel_time['geometry'] = geometry
	gdf_mean_travel_time = GeoDataFrame(mean_travel_time, geometry='geometry')
	gdf_mean_travel_time.crs = {}

	# create buffers for reached stations
	crs_meters = {'init': 'epsg:25832'}
	traveled_buffer = gdf_mean_travel_time.to_crs(crs_meters)
	traveled_buffer['geometry'] = traveled_buffer.buffer(buffer)

	# join already reached stations with stations
	stations_join = sjoin(target_stations_buffer, traveled_buffer[[
		'travel_time', 'geometry']], how='left')

	reached_stations_index = stations_join[stations_join['travel_time'].notna(
	)]['station_id'].tolist()
	return reached_stations_index




