import datetime
import requests
from geopandas import GeoDataFrame, sjoin, read_file
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point, Polygon
from tools.api_keys import here_app_code, here_app_id

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
		if not res_json['Res'].get('Message').get('subcode') == 'DEP_ARR_TOO_CLOSE':
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





def add_to_dict_xy(times_dict, new_times, new_stations, y, x):
	for i in range(len(new_times)):
		try:
			times_dict[new_stations[i]]['travel_times'].append(new_times[i])
		except KeyError:
			times_dict.update(
			{new_stations[i]: {'travel_times': [new_times[i]], 'y': y[i], 'x': x[i]}})

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
				if i == '0':
					time_ = section['Arr'].get('time')
					address = section['Arr'].get('Addr')
					if address is None:
						stn = section['Arr'].get('Stn')
						ids.append(stn['id'])
						stops_x.append(stn['x'])
						stops_y.append(stn['y'])
						names.append(stn['name'])
						time_diff_ = get_time_difference(dep_time_, time_)
						time.append(time_diff_)
					else:
						time_diff_ = get_time_difference(dep_time_, time_)
						time.append(time_diff_)
						ids.append('NoID')
						stops_x.append(address['x'])
						stops_y.append(address['y'])
						names.append('Walk')

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


	stations_df = pd.DataFrame.from_dict(
		{'station': ids,
		 'names': names,
		 'travel_time': time,
		 'x': stops_x,
		 'y': stops_y})

	return stations_df




def find_reached_stations(reached_stations_df: pd.DataFrame,
						  target_stations: GeoDataFrame,
						  buffer: int,
						  counter: int = 1) -> list:
	mean_travel_time = reached_stations_df.groupby('station').mean()
	geometry = [Point(xy) for xy in zip(mean_travel_time.x, mean_travel_time.y)]
	mean_travel_time['geometry'] = geometry
	gdf_mean_travel_time = GeoDataFrame(mean_travel_time, geometry='geometry')
	gdf_mean_travel_time.crs = {'init': 'epsg:4326'}

	# create buffers for reached stations
	crs_meters = {'init': 'epsg:25832'}
	traveled_buffer = gdf_mean_travel_time.to_crs(crs_meters)
	traveled_buffer['geometry'] = traveled_buffer.buffer(buffer)

	# buffer target stations
	target_stations_buffer = target_stations.to_crs(crs_meters)
	target_stations_buffer['geometry'] = target_stations_buffer.buffer(buffer)

	# for debugging
	# if buffer >= 50:
	# 	traveled_buffer.to_file('data/debug/traveled_' + str(counter) + '.shp')
	# 	target_stations_buffer.to_file('data/debug/target_' + str(counter) + '.shp')

	# join already reached stations with stations
	stations_join = sjoin(target_stations_buffer, traveled_buffer[[
		'travel_time', 'geometry']], how='left')

	reached_stations_index = stations_join[stations_join['travel_time'].notna(
	)]['station_id'].tolist()
	return reached_stations_index


import betamax


class PubTransRouter:



	def __init__(self, app_id, app_code):
		if app_id is None or app_code is None:
			raise ValueError(
				"A HERE app ID and app Code is needed."
			)
		self.session = requests.Session()
		self.session.params = {}
		self.session.params['app_id'] = app_id
		self.session.params['app_code'] = app_code
		self.session.params['routing'] = 'tt'

		self.HERE_TRANSIT_ROUTING_URL = 'https://transit.api.here.com/v3/route.json'

	def request_route(self, date_time:datetime, origin_yx:list, destination_yx:list, graph=True) -> dict:
		self.session.params['time'] = format_time_for_request(date_time)
		self.session.params['graph'] = int(graph)
		self.session.params['dep'] = ','.join(list(map(str, origin_yx)))
		self.session.params['arr'] = ','.join(list(map(str, destination_yx)))


		# CASSETTE_LIBRARY_DIR = 'data/cassettes/'
		# match_on = ['uri']
		#
		# recorder = betamax.Betamax(
		# 	self.session, cassette_library_dir=CASSETTE_LIBRARY_DIR
		# )
		#
		# with recorder.use_cassette('here_pub_trans_responses', record='new_episodes', match_requests_on=match_on):
		# 	response = self.session.get(url=self.HERE_TRANSIT_ROUTING_URL)
		#
		#
		response = self.session.get(url=self.HERE_TRANSIT_ROUTING_URL)

		res_json = response.json()
		if not res_json['Res'].get('Message') is None:
			if not res_json['Res'].get('Message').get('subcode') == 'DEP_ARR_TOO_CLOSE':
				raise ValueError(res_json['Res'].get('Message'))

		return res_json



def request_travel_times(target_stations:gpd.GeoDataFrame,
						 origin:gpd.geoseries.GeoSeries,
						 date_time:datetime.datetime):

	times_dict = {}
	last_index = 0
	buffer = 50
	counter = 1

	router = PubTransRouter(here_app_id, here_app_code)

	while len(target_stations) > 0:


		index_farest = target_stations.distance(origin.geometry).sort_values(ascending=False).head(1).index
		farest_y = target_stations.loc[index_farest].geometry.centroid.y
		farest_x = target_stations.loc[index_farest].geometry.centroid.x

		pt_request = router.request_route(date_time,
										  [origin.geometry.y,origin.geometry.x],
										  [farest_y.iloc[0],farest_x.iloc[0]],
										  False)
		try:

			travel_times = extract_travel_times(pt_request)

			times_dict = add_to_dict_xy(times_dict,
										travel_times['travel_time'].tolist(),
										travel_times['station'].tolist(),
										travel_times['y'].tolist(),
										travel_times['x'].tolist())

			if last_index == index_farest:
				buffer = buffer + 50
			else:
				buffer = 50

			reached_stations = find_reached_stations(travel_times,
													 target_stations,
													 buffer)

			target_stations = target_stations[~target_stations['station_id'].isin(reached_stations)]

			last_index = index_farest
			counter += 1

			print(counter, '. Round')
			print(len(target_stations), ' stations left')
			if buffer > 50:
				print(buffer, ' buffer')
		except:
			print('Problem')
			print(pt_request)
			try:
				target_stations = target_stations.loc[~index_farest]
			except TypeError:
				target_stations = target_stations.iloc[0:0]


	return times_dict


def create_travel_time_df(stations: gpd.GeoDataFrame, date_time: datetime):
	stations_df = pd.DataFrame(columns=['station', 'depature', 'travel_time', 'x', 'y'])
	outer_counter = 1

	for ix, origin in stations.iterrows():
		print(outer_counter, 'OUTER RUN')

		travel_times_dict = request_travel_times(stations, origin, date_time)

		travel_times_list = [pd.Series(v.get('travel_times')).mean().astype('int') for k, v in
							 travel_times_dict.items()]
		ids_list = [k for k, v in travel_times_dict.items()]
		x_list = [v.get('x') for k, v in travel_times_dict.items()]
		y_list = [v.get('y') for k, v in travel_times_dict.items()]

		stations_new_df = pd.DataFrame.from_dict(
			{'station': ids_list,
			 'depature': [origin['station_id']] * len(ids_list),
			 'travel_time': travel_times_list,
			 'x': x_list,
			 'y': y_list})

		stations_df = pd.concat([stations_df, stations_new_df])
		outer_counter += 1

	# stations_df.to_csv('pt_travel_time_test_result.csv')
	# stations_df = pd.read_csv('pt_travel_time_test_result.csv')
	stations_df['travel_time'] = stations_df['travel_time'].astype(int)

	return stations_df


def get_accessibility_gdf(travel_time_df):
	station_by_count = travel_time_df.groupby('station').count()
	threshold = len(station_by_count) / 3
	connected_stations = station_by_count[station_by_count['travel_time'] > threshold].index

	mean_accessibility = travel_time_df.groupby('station').mean()
	mean_accessibility_filtered = mean_accessibility.loc[connected_stations]
	#mean_accessibility_filtered = mean_accessibility.loc[~mean_accessibility_filtered.index.isin(['NoID'])]

	mean_accessibility_gpd = mean_accessibility_filtered[['travel_time', 'x', 'y']]
	geometry = [Point(xy) for xy in zip(mean_accessibility_gpd.x, mean_accessibility_gpd.y)]
	mean_accessibility_gpd['geometry'] = geometry
	mean_accessibility_gpd = GeoDataFrame(mean_accessibility_gpd, geometry='geometry')
	mean_accessibility_gpd.crs = {'init': 'epsg:4326'}
	mean_accessibility_gpd.reset_index(level=0, inplace=True)
	mean_accessibility_gpd = mean_accessibility_gpd[mean_accessibility_gpd['station'] != 'NoID']
	return mean_accessibility_gpd



def get_iso_lines(points_gdf, times=[1, 5, 11]):


	iso_df = pd.DataFrame.from_dict(
		{'station': points_gdf['station'].tolist()})


	session = requests.Session()
	session.params = {}
	isochrone_url = 'https://isoline.route.api.here.com/routing/7.2/calculateisoline.json'
	session.params = {}
	session.params['app_code'] = here_app_code
	session.params['app_id'] = here_app_id
	session.params['mode'] = 'fastest;pedestrian'
	session.params['rangetype'] = 'time'

	for time in times:

		session.params['range'] = time * 60
		iso_poly = []

		for i in range(len(points_gdf)):

			test_iso = points_gdf.iloc[i]
			test_iso_x = test_iso.geometry.x
			test_iso_y = test_iso.geometry.y

			session.params['start'] = 'geo!' + str(test_iso_y) + ',' + str(test_iso_x)

			response_iso = session.get(url=isochrone_url)
			resp_iso_json = response_iso.json()

			shape_list = resp_iso_json['response']['isoline'][0]['component'][0]['shape']

			iso_poly.append(Polygon([list(map(float, reversed(yx.split(','))))
									 for yx in shape_list]))
			print('For', time, ': ', i, 'of 100')
		iso_df['iso' + str(time)] = iso_poly

	return iso_df

