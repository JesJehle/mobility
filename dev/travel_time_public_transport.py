# from pandas import DataFrame
# import folium
# from random import randint
# from numpy import nan
# import osmnx as ox

import sys
sys.path.append('/home/jesjehle/Documents/Mobility/sumo/tools')
import os
from shapely.geometry import Point, Polygon
import datetime
import pandas as pd
import json
from api_keys import here_app_code, here_app_id
import requests
import geopandas as gpd


# functions

def get_time_difference(stringDep, StringArr):

    dep_time = datetime.datetime.strptime(stringDep.split('T')[1], '%H:%M:%S').time()
    dep_time_delta = datetime.timedelta(
        hours=dep_time.hour, minutes=dep_time.minute, seconds=dep_time.second)

    arr_time = datetime.datetime.strptime(StringArr.split('T')[1], '%H:%M:%S').time()
    arr_time_delta = datetime.timedelta(
        hours=arr_time.hour, minutes=arr_time.minute, seconds=arr_time.second)

    difference = arr_time_delta - dep_time_delta
    return int(difference.total_seconds()/60)


#
# # get data ------------------------------------------
# grid_pop = gpd.read_file('data/freiburg/grid_pop_fr_wgs.shp')
# stations = gpd.read_file('data/freiburg/stations.shp')
# # interesect stations with pop grid
# grid_station_intersection = gpd.sjoin(grid_pop[['id', 'geometry']], stations[[
#                                       'station_id', 'geometry']], how='right')
# station_in_grid = grid_station_intersection['index_left'].notna()
# grid_in_station = grid_station_intersection[station_in_grid]
#
# # inspect and save data
# grid_in_station.plot()
# grid_in_station.to_file('data/freiburg/grid_in_station_as_points.shp')
#
#
# # create a subsample to reduce the requests
# grid_in_station_sample = grid_in_station.sample(100)
# grid_in_station_sample.to_file('data/freiburg/grid_in_station_sample_points.shp')

# -------------------------------------------------------------------------

# grid_in_station_sample = gpd.read_file('data/freiburg/grid_in_station_sample_points.shp')
# grid = grid_in_station_sample[['station_id', 'geometry']]

station = gpd.read_file('data/freiburg/grid_in_station_as_points.shp')
station = station[['station_id', 'geometry']]

crs_meters = {'init': 'epsg:25832'}
station_buffer = station.to_crs(crs_meters)
station_buffer['geometry'] = station_buffer.buffer(100)


# make requests

transit_route_url = 'https://transit.api.here.com/v3/route.json'
params = {}
params['app_id'] = here_app_id
params['app_code'] = here_app_code
params['routing'] = 'tt'

params['time'] = '2019-02-24T12:30:54'
params['graph'] = 1

y = station['geometry'].y.tolist()
x = station['geometry'].x.tolist()
station_id_index = station.set_index('station_id')


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
                if isinstance(i, dict) and not i.get('dep') is None:
                    time_diff_ = get_time_difference(dep_time_, i.get('dep'))
                    time.append(time_diff_)
                    ids.append(i['Stn']['id'])
                    stops_x.append(i['Stn']['x'])
                    stops_y.append(i['Stn']['y'])
                    names.append(i['Stn']['name'])


    return time, ids, stops_x, stops_y, names

times_dict = add_to_dict(times_dict, time, ids)


for dep in range(len([1])):
    dep_y = y[4]
    dep_x = x[4]
    params['dep'] = str(dep_y) + ',' + str(dep_x)
    dep_point = Point([dep_y, dep_x])

    station_to_search_index = station_id_index.index.tolist()
    counter = 0

    times_dict = {}
    while not len(station_to_search_index) == 0:

        # find point with highest distance to first deparuture
        farest_point = station_id_index.loc[station_to_search_index].distance(
            dep_point).sort_values().head(1).index
        farest_point_geom = station_id_index.loc[farest_point]
        print(farest_point_geom)
        arr_y = farest_point_geom.geometry.y
        arr_x = farest_point_geom.geometry.x
        params['arr'] = str(arr_y.values[0]) + ',' + str(arr_x.values[0])
        # make request
        response = requests.get(transit_route_url, params=params)
        # parse response
        res_json = response.json()
        try:
            extract_travel_times()

            # make df of lists
            df_new_stations_test = pd.DataFrame.from_dict(
                {'station': all_stops,
                'names': names,
                'travel_time': time,
                'x': stops_x,
                'y': stops_y})

            # make geo_df of df
            mean_travel_time = df_new_stations_test.groupby('station').mean()
            geometry = [Point(xy) for xy in zip(mean_travel_time.x, mean_travel_time.y)]
            mean_travel_time['geometry'] = geometry
            gdf_mean_travel_time = gpd.GeoDataFrame(mean_travel_time, geometry='geometry')
            gdf_mean_travel_time.crs = grid.crs

            # create buffers
            crs_meters = {'init': 'epsg:25832'}
            traveled_buffer = gdf_mean_travel_time.to_crs(crs_meters)
            traveled_buffer['geometry'] = traveled_buffer.buffer(1000)

            # join already reached stations with stations
            stations_join = gpd.sjoin(station_buffer, traveled_buffer[[
                                      'travel_time', 'geometry']], how='left')

            reached_stations_index = stations_join[stations_join['travel_time'].notna(
            )]['station_id'].tolist()

            for i in reached_stations_index:
                try:
                    station_to_search_index.remove(i)
                except:
                    pass

            print('departer:', dep, ' with round: ', counter, ' with: ',
                  len(station_to_search_index), ' stations left')
            counter = + 1
        except Exception as e:
            print(e)


len(stations_join)
len(reached_stations_index)
len(station_to_search_index)
len(times_dict.keys())
type(stations_join)

stations_join[stations_join['travel_time'].notna()].to_file('data/freiburg/reached_stations.shp')
farest_point_geom.to_file('data/freiburg/farest_stations.shp')


def add_to_dict(times_dict, new_times, new_stations):
    for i in range(len(new_times)):
        try:
            times_dict[new_stations[i]].append(new_times[i])
        except KeyError:
            times_dict.update(
            {new_stations[i]: [new_times[i]]})

    return times_dict


def add_to_dict_old(times_dict, new_times, new_stations, y, x):
    for i in range(len(new_times)):
        try:
            times_dict[new_stations[i]]['travel_times'].append(new_times[i])
        except KeyError:
            times_dict.update(
            {new_stations[i]: {'travel_times': [new_times[i]], 'y': y[i], 'x': x[i]}})

    return times_dict


for dep in range(len([1])):
    dep_y = y[dep]
    dep_x = x[dep]
    params['dep'] = str(dep_y) + ',' + str(dep_x)
    for arr in range(len(x)):
        arr_y = y[arr]
        arr_x = x[arr]
        params['arr'] = str(arr_y) + ',' + str(arr_x)

        # make request
        response = requests.get(transit_route_url, params=params)
        # parse response
        res_json = response.json()
        connection_time = []
        try:
            for connections in res_json['Res']['Connections']['Connection']:
                dep_time = connections['Dep']['time']
                arr_time = connections['Arr']['time']
                time_diff = get_time_difference(dep_time, arr_time)
                connection_time.append(time_diff)

            mean_travel_time = pd.Series(connection_time).mean().round()
            travel_time.append(mean_travel_time)
            print('departer:', dep, ' with arrival: ', arr)
        except:
            print(res_json)
            travel_time.append(0)


with open('transit-routing_full.json', 'w') as fp:
    json.dump(res_json, fp)


# load data ##############################

print(os.getcwd())
path = "transit-routing_full.json"
with open(path, 'r') as d:
    res_json = json.load(d)


%load_ext autoreload
%autoreload

################################################

time = []
all_stops = []
stops_x = []
stops_y = []
names = []
for connection in res_json['Res']['Connections']['Connection']:
    dep_time_ = connection['Dep']['time']
    for section in connection['Sections']['Sec']:
        for i in section['Journey'].get('Stop', '0'):
            if isinstance(i, dict):
                if not i.get('dep') is None:
                    time_diff_ = get_time_difference(dep_time_, i.get('dep'))
                    time.append(time_diff_)
                    all_stops.append(i['Stn']['id'])
                    stops_x.append(i['Stn']['x'])
                    stops_y.append(i['Stn']['y'])
                    names.append(i['Stn']['name'])


len(time)
len(all_stops)
len(stops_x)


# try to find the right ids

#
# url = 'https://transit.api.here.com/v3/multiboard/by_geocoord.json'
# params = {}
# params['app_id'] = here_app_id
# params['app_code'] = here_app_code
# params['center'] = str(stops_y[1]) + ',' + str(stops_x[1])
# params['time'] = '2019-01-24T12:30:54'
# response = requests.get(url, params=params)
# response_jsom = response.json()


df_new_stations_test = pd.DataFrame.from_dict(
    {'station': all_stops,
    'names': names,
    'travel_time': time,
    'x': stops_x,
    'y': stops_y})


mean_travel_time = df_new_stations_test.groupby('station').mean()
geometry = [Point(xy) for xy in zip(mean_travel_time.x, mean_travel_time.y)]
mean_travel_time['geometry'] = geometry
gdf_mean_travel_time = gpd.GeoDataFrame(mean_travel_time, geometry='geometry')
gdf_mean_travel_time.crs = grid.crs
gdf_mean_travel_time.to_file('data/freiburg/new_stations_test.shp')


crs_meters = {'init': 'epsg:25832'}
traveled_buffer = gdf_mean_travel_time.to_crs(crs_meters)
traveled_buffer['geometry'] = traveled_buffer.buffer(50)
traveled_buffer.to_file('data/freiburg/traveled_buffer.shp')

station_buffer = station.to_crs(crs_meters)
station_buffer['geometry'] = station_prj.buffer(50)
station_buffer.to_file('data/freiburg/stations_buffer.shp')


stations_join = gpd.sjoin(station_buffer, traveled_buffer[['travel_time', 'geometry']], how='left')

len(stations_join[stations_join['travel_time'].isna()])


len(station)


station.plot()


def add_to_dict(times_dict, new_times, new_stations, y, x):
    for i in range(len(new_times)):
        try:
            times_dict[new_stations[i]]['travel_times'].append(new_times[i])
        except KeyError:
            times_dict.update(
            {new_stations[i]: {'travel_times': [new_times[i]], 'y': y[i], 'x': x[i]}})

    return times_dict


test = {'efa_bla': {'times': [1, 2, 3], 'y': 123, 'x': 2}}

test['efa_bla']['times'].append(2)


times_dict = add_to_dict({}, time, all_stops, stops_y, stops_x)


times_dict.keys()


station = gpd.read_file('data/freiburg/stations.shp')

stations_names = station['station_na'].tolist()

stations_names_clean = [i.casefold().strip() for i in stations_names]
names_clean_routing = [i.casefold().replace('freiburg', '').strip() for i in names]


matching = [s for s in stations_test if "Bahnhof" in s]

for s in stations_names_clean:
    for r in names_clean_routing:
        print(r)
        if r.find(s) is not -1:
            print(r, '=', s)


all(elem in stations_test for elem in times_test)

grid_in_station.set_index('station_id').loc[test_index2]
grid_with_index.loc[list(times_dict)]

list(times_dict)
grid_with_index.loc[(grid_with_index[list(times_dict)] == pd.Series(times_dict)).all(axis=1)]

grid_with_index


grid['station_id'] in list(times_dict)

# to geo_df
grid['']
##################################################################


len(deps)

journey = get_keys_from_json(res_json, 'Journey')
stops = get_keys_from_json(journey, 'Stop')
len(stops)


deps = get_keys_from_json(stops, 'dep')
len(deps)
arr = get_keys_from_json(journey, 'arr')
len(arr)
stn = get_keys_from_json(journey, 'Stn')
len(stn)


for i in res_json['Res']['Connections']['Connection'][0]['Sections']['Sec'][0]['Journey']:
    for e in i:
        print(e['Stop'])

test = res_json['Res']['Connections']['Connection'][0]['Sections']['Sec'][1]['Journey']
for i in test:
    print(test['Stop'])
test['Stop']
   if parts == 'Stop':
        print(parts[0])

    try:
        for stops in parts['Stop']:
            print(stops)
    except:
        pass

test_travel_time = travel_time[0:100]

grid[station_id[0]] = test_travel_time


grid.to_file('data/freiburg/test_public_transport_travel_time.shp')

ax = grid.plot(column='db_808174', legend='True')
grid[grid['station_id'] == station_id[0]].plot(ax=ax, color='red')

grid.plot(column='travel_time_db_808174', legend='True')


def get_iso_lines(points_gdf, times=[5, 10, 15]):

    iso_df = pd.DataFrame.from_dict(
        {'station': points_gdf['station_id'].tolist()})

    for time in times:
        iso_poly = []
        for i in range(len(points_gdf)):

            test_iso = points_gdf.iloc[i]
            test_iso_x = test_iso.geometry.x
            test_iso_y = test_iso.geometry.y

            isochrone_url = 'https://isoline.route.api.here.com/routing/7.2/calculateisoline.json'
            params = {}
            params['app_code'] = here_app_code
            params['app_id'] = here_app_id
            params['mode'] = 'fastest;pedestrian'
            params['start'] = 'geo!' + str(test_iso_y) + ',' + str(test_iso_x)
            params['rangetype'] = 'time'
            params['range'] = time * 60

            response_iso = requests.get(isochrone_url, params=params)
            resp_iso_json = response_iso.json()

            shape_list = resp_iso_json['response']['isoline'][0]['component'][0]['shape']

            iso_poly.append(Polygon([list(map(float, reversed(yx.split(','))))
                                     for yx in shape_list]))
            print('For', time, ': ', i, 'of 100')
        iso_df['iso' + str(time)] = iso_poly

    return iso_df


iso_df = get_iso_lines(grid)


iso_gdf = gpd.GeoDataFrame(iso_df, geometry='iso_line')
iso_gdf.crs = grid.crs
iso_gdf.to_file('data/freiburg/iso_10m_stations.shp')
iso_gdf.plot()


# for section in res_json['Res']['Connections']['Connection'][0]['Sections']['Sec']:
#     print(section)
#
#
# for sub_section in res_json['Res']['Connections']['Connection'][0]['Sections']['Sec'][1]:
#     print(sub_section)
#
# section_test = res_json['Res']['Connections']['Connection'][0]['Sections']['Sec'][1]
#
#
# with open('transit-routing.json', 'w') as fp:
#     json.dump(res_json['Res']['Connections']['Connection'][0], fp)
