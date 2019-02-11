

def test_format_time_for_request():
    from tools.travel_time_pt import format_time_for_request
    import datetime
    time_input = datetime.datetime(2019, 2, 2, 10, 0)
    time_output = '2019-02-02T10:00:00'
    assert format_time_for_request(time_input) == time_output


def test_request_route():
    import datetime
    from tools.travel_time_pt import PubTransRouter
    from tools.api_keys import here_app_code, here_app_id

    date_time = datetime.datetime(2019, 2, 2, 10, 0)
    origin = [48.022917, 7.85832]
    destination = [48.007457, 7.855260]
    router = PubTransRouter(here_app_id, here_app_code)

    response = router.request_route(date_time, origin, destination, False)
    assert isinstance(response['Res'], dict)



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
    found_stations = find_reached_stations(stations_df, target_stations, 50)
    assert isinstance(found_stations, list)



def test_create_travel_time_df():

    import geopandas as gpd
    from tools.travel_time_pt import create_travel_time_df
    from pandas import DataFrame
    import datetime

    target_stations = gpd.read_file('data/test_sample_target_stations.shp')
    target_stations.crs = {'init': 'epsg:4326'}
    target_stations = target_stations[['station_id', 'geometry']]
    # origin = target_stations.sample(1).geometry
    date_time = datetime.datetime(2019, 2, 2, 10, 0)
    travel_time_test = create_travel_time_df(target_stations.sample(2), date_time)

    assert isinstance(travel_time_test, DataFrame)



def test_get_accessibility_gdf():
    import pandas as pd
    from geopandas import GeoDataFrame
    from tools.travel_time_pt import get_accessibility_gdf
    stations_df = pd.read_csv('pt_travel_time_test_result.csv')
    test = get_accessibility_gdf(stations_df)
    assert isinstance(test,GeoDataFrame )




from tools.travel_time_pt import get_iso_lines

import geopandas as gpd

target_stations = gpd.read_file('../data/freiburg/pt_accessibility.shp')
target_stations.crs = {'init': 'epsg:4326'}

target_stations_iso = get_iso_lines(target_stations)

points_gdf = target_stations

#
# travel_time_counts = travel_time_test.groupby('station').count()
# station_index = travel_time_counts[travel_time_counts['travel_time'] > 150].index
#
# mean_station = travel_time_test.groupby('station').mean()
# connectivity
# import pandas as pd
# from geopandas import GeoDataFrame
# from shapely.geometry import Point
# from tools.travel_time_pt import get_accessibility_gdf
# stations_df = pd.read_csv('pt_travel_time_test_result.csv')
#
# mean_connectivity = stations_df[['depature', 'travel_time']].groupby('depature').mean()
#
# mean_coords_id = stations_df.groupby('station').mean()
#
# pd.merge(mean_connectivity, mean_coords_id[['x', 'y']], on='station')
# mean_connectivity.index.names = ['station']
#
# .join(, on='station')
# mean_connectivity_gpd = mean_connectivity[['travel_time', 'x', 'y']]
# geometry = [Point(xy) for xy in zip(mean_connectivity_gpd.x, mean_connectivity_gpd.y)]
# mean_connectivity_gpd['geometry'] = geometry
# mean_connectivity_gpd = GeoDataFrame(mean_connectivity_gpd, geometry='geometry')
# mean_connectivity_gpd.crs = {'init': 'epsg:4326'}
# assert isinstance(test,GeoDataFrame )
# mean_connectivity_gpd.to_file('data/connectivity_sample.shp')
#
