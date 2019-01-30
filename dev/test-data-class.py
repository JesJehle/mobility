
# from shapely.geometry import Point, LineString
# import re
#from shapely.geometry import Point, LineString, MultiLineString
#import re
#import json

from api_keys import here_app_id, here_app_code
import osmnx as ox
from shapely.geometry import Point, LineString, MultiLineString
from geopandas import GeoDataFrame
from pandas import DataFrame
import re
import requests
import geocoder
import folium
from request_data import TrafficData, Helper
%load_ext autoreload
%autoreload


l = TrafficData('Lörrach, Germany')

l.request_data(radius=1000, minJamFactor=1, maxFuncClass=5)
l.to_gdf()
l.traffic_gdf.plot(column="sp", legend=True)

# make a map
df_json = l.traffic_gdf.to_json()
traffic = folium.features.GeoJson(df_json)

m = folium.Map(l.city_coords)
m.add_children(traffic)
m.save('lörrach.html')


city_b = ox.gdf_from_place(l.city_name)
bbox = [city_b.bbox_north[0], city_b.bbox_east[0], city_b.bbox_south[0], city_b.bbox_west[0]]
bbox = list(map(str, bbox))
bbox = ','.join(bbox)
bbox = bbox[0] + ',' + bbox[1] + ';' + bbox[2] + ',' + bbox[3]
search_coords = str(self.city_coords[0]) + ',' + \
    str(self.city_coords[1]) + ',' + str(radius)


here_traffic_availability_url = "https://traffic.api.here.com/traffic/6.0/flowavailability.json"
params = {}
params['app_id'] = here_app_id
params['app_code'] = here_app_code
#params['profile'] = 'NTdefault'
params['mapview'] = bbox
# params['zoom'] = 14

response = requests.get(here_traffic_availability_url, params=params)

response = response.json()

here_traffic_url = "https://traffic.api.here.com/traffic/6.1/flow.json"
params = {}
params['app_id'] = here_app_id
params['app_code'] = here_app_code
#params['profile'] = 'NTdefault'
params['bbox'] = bbox
params['responseattributes'] = 'sh,fc'

response = requests.get(here_traffic_url, params=params)

response = response.json()


%load_ext autoreload
%autoreload

l = TrafficData('Freiburg, Germany')

l.request_data(radius=10000)
l.to_gdf()
l.response
l.traffic_gdf.plot(column="jf", legend=True)

df_json = l.traffic_gdf.to_json()
traffic = folium.features.GeoJson(df_json)

m = folium.Map(l.city_coords)
m.add_children(traffic)
m.save('freiburg-bbox.html')
