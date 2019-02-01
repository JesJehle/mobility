import datetime
from pandas import DataFrame
import requests
from geopandas import GeoDataFrame, sjoin
from shapely.geometry import Point


def format_time_for_request(time_datetime: datetime) -> str:
	time = time_datetime.time().strftime('%H:%M:%S')
	date = time_datetime.date().strftime('%Y-%m-%d')
	request_string = date + 'T' + time
	return request_string


def get_time_difference(stringDep, StringArr):
	dep_time = datetime.datetime.strptime(stringDep.split('T')[1], '%H:%M:%S').time()
	dep_time_delta = datetime.timedelta(
		hours=dep_time.hour, minutes=dep_time.minute, seconds=dep_time.second)

	arr_time = datetime.datetime.strptime(StringArr.split('T')[1], '%H:%M:%S').time()
	arr_time_delta = datetime.timedelta(
		hours=arr_time.hour, minutes=arr_time.minute, seconds=arr_time.second)

	difference = arr_time_delta - dep_time_delta
	return int(difference.total_seconds() / 60)


def request_pt_route(here_app_id:str, here_app_code:str, datetime:datetime, depyx:list, arryx:list, graph=True) -> dict:
	"""Requests public transport routing from the here api for a given departure, arrival and time"""

	transit_route_url = 'https://transit.api.here.com/v3/route.json'
	params = {}
	params['app_id'] = here_app_id
	params['app_code'] = here_app_code
	params['routing'] = 'tt'
	params['time'] = format_time_for_request(datetime)
	params['graph'] = int(graph)
	params['dep'] = ','.join(list(map(str, depyx)))
	params['arr'] = ','.join(list(map(str, arryx)))

	response = requests.get(transit_route_url, params=params)
	res_json = response.json()
	if not res_json['Res'].get('Message') is None:
		raise ValueError(res_json['Res'].get('Message'))

	return res_json



def add_to_dict(times_dict, new_times, new_stations):
	for i in range(len(new_times)):
		try:
			times_dict[new_stations[i]].append(new_times[i])
		except KeyError:
			times_dict.update(
				{new_stations[i]: [new_times[i]]})

	return times_dict


def extract_travel_times(here_pt_response):
	time = []
	ids = []
	stops_x = []
	stops_y = []
	names = []
	for connection in here_pt_response['Res']['Connections']['Connection']:
		dep_time_ = connection['Dep']['time']
		for section in connection['Sections']['Sec']:
			for i in section['Journey'].get('Stop', '0'):
				if isinstance(i, dict):
					try:
						time_ = i['arr']
					except KeyError:
						time_ = i['dep']
					finally:
						time_diff_ = get_time_difference(dep_time_, time_)
						time.append(time_diff_)
						ids.append(i['Stn']['id'])
						stops_x.append(i['Stn']['x'])
						stops_y.append(i['Stn']['y'])
						names.append(i['Stn']['name'])


	stations_df = DataFrame.from_dict(
		{'station': ids,
		 'names': names,
		 'travel_time': time,
		 'x': stops_x,
		 'y': stops_y})

	return stations_df




def find_reached_stations(reached_stations_df, target_stations, buffer):
	mean_travel_time = reached_stations_df.groupby('station').mean()
	geometry = [Point(xy) for xy in zip(mean_travel_time.x, mean_travel_time.y)]
	mean_travel_time['geometry'] = geometry
	gdf_mean_travel_time = GeoDataFrame(mean_travel_time, geometry='geometry')
	gdf_mean_travel_time.crs = {'init': 'epsg:4326'}

	# create buffers for reached stations
	crs_meters = {'init': 'epsg:25832'}
	traveled_buffer = gdf_mean_travel_time.to_crs(crs_meters)
	traveled_buffer['geometry'] = traveled_buffer.buffer(buffer)


	target_stations_buffer = target_stations.to_crs(crs_meters)
	target_stations_buffer['geometry'] = target_stations_buffer.buffer(buffer)

	# join already reached stations with stations
	stations_join = sjoin(target_stations_buffer, traveled_buffer[[
		'travel_time', 'geometry']], how='left')

	reached_stations_index = stations_join[stations_join['travel_time'].notna(
	)]['station_id'].tolist()
	return reached_stations_index



