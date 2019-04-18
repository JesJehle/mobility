
import sys
sys.path.append('/home/jesjehle/Documents/Mobility/sumo')

import geopandas as gpd
from tools.traffic_data import TrafficData
import pandas as pd
import os
from datetime import datetime


city_filepath = '/home/jesjehle/Documents/Mobility/data/Poster/poi_shapes.shp'
boundary_filepath = '/home/jesjehle/Documents/Mobility/data/Poster/upper_rhine_shape.shp'
wdir = '/home/jesjehle/Documents/Mobility/data/Poster/traffic_data'

number_of_files = len(os.listdir(wdir))
time = datetime.now().strftime("%d-%m_%H:%M")
filename =  str(number_of_files) + '_traffic_' + str(time) + '.geojson'

traffic_filepath = os.path.join(wdir,filename)


def main():

    proj_cities = gpd.read_file(city_filepath)
    proj_boundary = gpd.read_file(boundary_filepath)

    # set projection
    etrs89 = {'init': 'epsg:4258'}
    proj_cities.crs = etrs89
    proj_boundary.crs = etrs89
    # convert to wgs 84
    proj_cities_wgs = proj_cities.to_crs(epsg=4326)
    proj_boundary_wgs = proj_boundary.to_crs(epsg=4326)

    # use two origins for request to cover entire area
    city_selection = proj_cities_wgs[proj_cities_wgs['NAME_left'].isin(['Karlsruhe', 'Freiburg im Breisgau'])]
    x = city_selection.centroid.x
    y = city_selection.centroid.y

    gdf = gpd.GeoDataFrame()

    for x_, y_ in zip(x,y):
        traffic = TrafficData(cityCoords=[y_, x_])
        traffic.request_data(100000)
        traffic.to_gdf()
        gdf = pd.concat([gdf, traffic.traffic_gdf])

    gdf.crs = {'init': 'epsg:4326'}
    gdf_in_boundary = gpd.sjoin(gdf, proj_boundary_wgs, op='within')

    df_unique = gdf_in_boundary.drop(columns='geometry').drop_duplicates()
    gdf_in_boundary_unique = gdf_in_boundary.loc[df_unique.index.drop_duplicates()]

    gdf_in_boundary_unique.crs = {'init': 'epsg:4326'}

    gdf_in_boundary_unique.to_file(traffic_filepath, driver='GeoJSON')

    return


if __name__ == '__main__':
    main()



