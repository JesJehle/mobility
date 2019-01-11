
# from shapely.geometry import Point, LineString
# import re
from shapely.geometry import Point, LineString, MultiLineString
import re
import json

from request_data import TrafficData, Helper
#import folium
%load_ext autoreload
%autoreload


l = TrafficData('Lörrach, Germany')

l.request_data(radius=100000, minJamFactor=9, maxFuncClass=3)
l.to_gdf()
l.traffic_gdf.plot(column="cn", legend=True)


df_json = l.traffic_gdf.to_json()

traffic = folium.features.GeoJson(df_json)

coordsf = Helper.get_coords_from_address('Freiburg, Germany')
m = folium.Map(coordsf)
m.add_children(traffic)
m.save('freiburg.html')
