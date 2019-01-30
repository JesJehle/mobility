import folium
import geoplot
from places_data import get_type
from utiles import SearchGrid, get_coords_from_address
#import osmnx as ox
# import googlemaps
# from api_keys import google_api_key
import pandas as pd
# from numpy import nan
# import geopandas as gpd
# from shapely.geometry import Point
%load_ext autoreload
%autoreload


grid_freiburg = SearchGrid('Lörrach, Germany', 2000, 2000)

one_grid = grid_freiburg.grid.iloc[0:1]


location = [one_grid.centroid.y, one_grid.centroid.x]
radius = 1000
type = 'store'
places = gmaps.places_nearby(location=location, radius=radius, type=type)


res = get_type(grid_freiburg.grid, 1000, 'bus_station')
res_unique = res.drop_duplicates(subset='place_id')

res_unique

df_json = res_unique.to_json()
bus_station = folium.features.GeoJson(df_json)
coords = get_coords_from_address('Lörrach, Germany')

m = folium.Map(coords)
m.add_children(bus_station)
m.save('bus_station.html')


res_unique.dropna().plot(column='rating', legend=True)
res_unique.dropna().plot(column='user_rating', legend=True)


res_unique.rating.describe()
b = geoplot.pointplot(res, hue='rating', linewidth=0.5, legend=True, cmap='Blues')
grid_freiburg.grid.iloc[0:2].plot(ax=b, color='grey', linewidth=0.5)

res_small = get_type(one_grid, 1000, 'store')
res_small.plot(column='rating', legend=True)
b = geoplot.pointplot(res_small, hue='rating', linewidth=0.5, legend=True, cmap='Blues')
grid_freiburg.grid.iloc[0:2].plot(ax=b, color='grey', linewidth=0.5)

geoplot.polyplot(grid_freiburg.buildings,  ax=b, linewidth=0.5)
#geoplot.polyplot(loerrach.city_boundary,  ax=b, linewidth=0.5)
#savefig('service_streets.png', dpi=200)
