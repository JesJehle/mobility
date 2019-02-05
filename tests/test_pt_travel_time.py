

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



import geopandas as gpd
from tools.travel_time_pt import request_travel_times
# from tools.api_keys import here_app_code, here_app_id
import datetime
import pandas as pd

# get targets

# target_stations = read_file('../data/freiburg/grid_in_station_as_points.shp')
target_stations = gpd.read_file('data/test_sample_target_stations.shp')

target_stations.crs = {'init': 'epsg:4326'}
target_stations = target_stations[['station_id', 'geometry']]
# get departure point

# origin = target_stations.sample(1).geometry
date_time = datetime.datetime(2019, 2, 2, 10, 0)


stations_df = pd.DataFrame(columns=['station', 'depature', 'travel_time', 'x', 'y'])
outer_counter = 1
for ix, origin in target_stations.iterrows():
    print(outer_counter, 'OUTER RUN')
    travel_times_dict = request_travel_times(target_stations, origin, date_time)

    travel_times_list = [pd.Series(v.get('travel_times')).mean().astype('int') for k, v in travel_times_dict.items()]
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



stations_df.to_csv('pt_travel_time_test_result.csv')
stations_df = pd.read_csv('pt_travel_time_test_result.csv')
stations_df['travel_time'] = stations_df['travel_time'].astype(int)


mean_accessibility = stations_df.groupby('station').mean()
from shapely.geometry import Point
from geopandas import GeoDataFrame
mean_accessibility_gpd = mean_accessibility[['travel_time', 'x', 'y']]
geometry = [Point(xy) for xy in zip(mean_accessibility_gpd.x, mean_accessibility_gpd.y)]
mean_accessibility_gpd['geometry'] = geometry
mean_accessibility_gpd = GeoDataFrame(mean_accessibility_gpd, geometry='geometry')
mean_accessibility_gpd.crs = {'init': 'epsg:4326'}

mean_accessibility_gpd.to_file('data/accessiblity_sample.shp')

