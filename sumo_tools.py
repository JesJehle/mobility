# -*- coding: utf-8 -*-


import pandas as pd
import osmnx as ox
import geopandas as gpd
from shapely.geometry import Polygon
from shapely.ops import nearest_points
from shapely.wkt import loads
from shapely.geometry import Point
import numpy as np
import geocoder
import requests
import googlemaps


# import api keys
from api_keys import here_app_id, here_app_code, google_api_key


def get_buildings(city_name):
    """
    Arguments : city_name = string ('Loerrach, Baden-Wuerttemberg, Gernamy')
    Downloads the footprint of the city buildings form osm database.
    Returns a GeoDataFrame gdf.
    """
    # download city boundary
    city = ox.gdf_from_place(city_name).geometry.iloc[0]
    # download buildings inside the boundary
    buildings = ox.buildings.create_buildings_gdf(city)
    return buildings


def create_grid(gdf_wgs, width, height):
    """ creates a regular grid of polygons with given
    height and width in meters. Takes a gdf with crs wgs"""

    gdf_utm = gdf_wgs.to_crs({'init': 'epsg:32632'})
    xmin, ymin, xmax, ymax = gdf_utm.total_bounds
    rows = int(np.ceil((ymax - ymin) / height))
    cols = int(np.ceil((xmax - xmin) / width))
    x_left_origin = xmin
    x_right_origin = xmin + width
    y_top_origin = ymax
    y_bottomo_origin = ymax - height
    polygons = []
    for i in range(cols):
        y_top = y_top_origin
        y_bottom = y_bottomo_origin
        for j in range(rows):
            polygons.append(Polygon([(x_left_origin, y_top), (x_right_origin, y_top), (x_right_origin, y_bottom),
                                     (x_left_origin, y_bottom)]))
            y_top = y_top - height
            y_bottom = y_bottom - height
        x_left_origin = x_left_origin + width
        x_right_origin = x_right_origin + width

    grid = gpd.GeoDataFrame({'geometry': polygons})
    grid.crs = {'init': 'epsg:32632'}
    grid_wgs = grid.to_crs({'init': 'epsg:4326'})

    return grid_wgs


def crop_grid(buildings, grid):
    intersections = gpd.sjoin(grid, buildings, how="left", op='intersects')
    grid_clean = intersections[['geometry', 'index_right']].dropna()
    grid_grouped = grid_clean.groupby(level=0)
    grid_unique = grid_grouped.first()
    grid_gdf = gpd.GeoDataFrame(grid_unique, geometry='geometry')

    return grid_gdf


def add_nearest_point(buildings, grid):
    """
    Find nearest point from grid centroid to next building centroid and add to grid gdf.
    :type grid: object
    """

    buildings_centroid = buildings.centroid.geometry.unary_union
    grid['centroids'] = grid.centroid
    p_list = []
    for index, row in grid.iterrows():
        nearest_p = nearest_points(row['centroids'], buildings_centroid)[1]
        p_list.append(nearest_p)

    grid['nearest_point'] = p_list

    return grid


def create_origin_destination_df(points):
    """
    create a df ...
    """

    start_list_x = []
    start_list_y = []
    destination_list_x = []
    destination_list_y = []
#    id = 0

    for row in points:
        for col in points:
            start_list_x.append(row.x)
            start_list_y.append(row.y)
            destination_list_x.append(col.x)
            destination_list_y.append(col.y)

    dest_matrix_df = pd.DataFrame(
        {'start_x': start_list_x,
         'start_y': start_list_y,
         'destination_x': destination_list_x,
         'destination_y': destination_list_y}
    )
    return dest_matrix_df


def get_coords(address):
    response = geocoder.osm(address)
    response_json = response.json
    lat = response_json['lat']
    lng = response_json['lng']

    return ((lng, lat))


def get_address(point):
    response = geocoder.osm([point.y, point.x], method="reverse")
    origin_address = response.json['address']
    return (origin_address)


def request_car_travel_time_here(dest_matrix):
    url = 'https://route.api.here.com/routing/7.2/calculateroute.json'
    payload = {}
    payload['app_id'] = here_app_id
    payload['app_code'] = here_app_code
    payload['mode'] = 'fastest;car'

    distance = []
    traffic_time = []
    base_time = []
    travel_time = []
    # request to api
    for i, row in dest_matrix.iterrows():
        payload['waypoint0'] = 'geo!' + str(row.start_y) + ',' + str(row.start_x)
        payload['waypoint1'] = 'geo!' + str(row.destination_y) + ',' + str(row.destination_x)
        response = requests.post(url, params=payload)
        respnse_json = response.json()
        summary = respnse_json['response']['route'][0]['summary']
        distance.append(summary['distance'])
        traffic_time.append(summary['trafficTime'])
        base_time.append(summary['baseTime'])
        travel_time.append(summary['travelTime'])

    # clean response
    travel_time_m = [round(i / 60) for i in travel_time]
    base_time_m = [round(i / 60) for i in base_time]
    traffic_time_m = [round(i / 60) for i in traffic_time]
    # add to df
    dest_matrix['travel_time'] = travel_time_m
    dest_matrix['base_time'] = base_time_m
    dest_matrix['traffic_time'] = traffic_time_m
    dest_matrix['distance'] = distance

    return dest_matrix


def get_streets(city_name, street_type='drive_service'):
    city_boundary = ox.gdf_from_place(city_name).geometry.iloc[0]
    drive_net = ox.graph_from_polygon(city_boundary, network_type=street_type)
    drive_gpd = ox.graph_to_gdfs(drive_net, nodes=False)

    return drive_gpd


def extract_info(response_json):
    if response_json['rows'][0]['elements'][0]['status'] == 'ZERO_RESULTS':
        distance = None
        duration = None
    else:
        distance = response_json['rows'][0]['elements'][0]['distance']['value']
        duration = response_json['rows'][0]['elements'][0]['duration']['value']

    return distance, duration


def request_travel_time_google(d_matrix, departure_time, mode='driving', traffic_model='best_guess'):
    """ Request travel time with given mode.
            modes can be: transit, driving, bicycling, walking
    """
    distance_l = []
    duration_l = []

    gmaps = googlemaps.Client(key=google_api_key)
    # request to api
    for i, row in d_matrix.iterrows():
        origins = (row.start_y, row.start_x)
        destination = (row.destination_y, row.destination_x)

        response = gmaps.distance_matrix(
            origins, destination, mode=mode, departure_time=departure_time, traffic_model=traffic_model)
        distance, duration = extract_info(response)

        distance_l.append(distance)
        duration_l.append(duration)

    # clean response
    duration = [round(i / 60) if i != None else i for i in duration_l]

    # add to df
    d_matrix['distance'] = distance_l
    d_matrix['duration'] = duration

    return d_matrix


def create_wkt(df, wkt=True, col_y='destination_y', col_x='destination_x'):
    coords_list = list(zip(df[col_x], df[col_y]))
    coords_point = list(map(Point, coords_list))
    if wkt:
        coords_wkt = list(map(lambda g: g.to_wkt(), coords_point))
        return coords_wkt
    else:
        return coords_point


def aggregate_travel_time(travel_time_df):

    travel_time_df['wkt'] = create_wkt(travel_time_df)
    group = travel_time_df[['distance', 'duration', 'wkt']].groupby('wkt').mean().reset_index()
    group['geometry'] = group['wkt'].apply(lambda a: loads(a))
    geo_df = gpd.GeoDataFrame(group, geometry='geometry')
    geo_df_selection = geo_df.drop('wkt', 1)

    geo_df_selection.crs = {'init': 'epsg:4326'}
    return geo_df_selection
