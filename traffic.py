
import re
import requests
from sumo_tools import get_coords
from api_keys import here_app_id, here_app_code
import pandas as pd
import numpy as np
from geopandas import GeoDataFrame
from shapely.geometry import Point, LineString
import json
import folium
# get coords Lörrach
coords_c = get_coords('Freiburg, Germany')
radius = 100000
search_coords = str(coords_c[0]) + ',' + str(coords_c[1]) + ',' + str(radius)

url = "https://traffic.api.here.com/traffic/6.1/flow.json"
header = {}
params = {}
params['app_id'] = here_app_id
params['app_code'] = here_app_code
params['prox'] = search_coords
params['responseattributes'] = 'sh,fc'

response = requests.get(url, params=params)
response_json = response.json()

with open('traffic-response2.json', 'w') as f:
    json.dump(response_json, f)

with open('traffic-response2.json') as f:
    response_json = json.load(f)


def get_key(json, key, key_list):
    if isinstance(json, dict):
        for keys in json:
            if keys == key:
                return(key_list.append(json[keys]))
            get_key(json[keys], key, key_list)
    if isinstance(json, list):
        for elements in json:
            get_key(elements, key, key_list)
    return key_list


coords_list = []
coords_list = get_key(response_json, 'value', coords_list)
len(coords_list)

fcat_list = []
key_list = get_key(response_json, 'FC', fcat_list)
len(fcat_list)

geometries = []

for coords in coords_list:
    string = re.sub(' ', ',', coords[0].strip())
    float_list = [float(i) for i in string.split(',')]
    xy = [float_list[i:i+2] for i in range(0, len(float_list), 2)]
    geometries.append(LineString([Point(p[1], p[0]) for p in xy]))


geo_df = pd.DataFrame.from_dict({'FC': fcat_list, 'geometry': geometries})

geo_df = GeoDataFrame(geo_df, geometry='geometry')

geo_df.plot(column='FC', legend=True)


df_json = geo_df.to_json()
traffic = folium.features.GeoJson(df_json)
m = folium.Map(coords_c)
m.add_children(traffic)
m.save('freiburg.html')


# for i in new_list:
#     coords_list.append(LineString([Point(xy[0], xy[1]) for xy in i]).wkt)
#
# xy = [i.split() for i in key_list[7]][0]
# xy
# xy_split = [i.split(',') for i in xy]
#
# xy_split
#
# xy_points =
#
# coords_list = []
# FC_list = []

# for item in respnse_json['RWS']:
#    for RW in item['RW']:
#        for FI in RW['FIS']:
#            for FI in FI['FI']:
#                for SHP in FI['SHP']:
#                    coords_list.append(SHP['value'])
#                    FC_list.append(SHP['FC'])


# new_list = []
# key_list[1]

# for i in coords_list:
#    list = i[0].split()
#    temp_list = []
#    for e in list:
#        temp_list.append([float(i) for i in list[0].split(',')])
#    new_list.append(temp_list)

#coords_list = []
# for i in new_list:
#    coords_list.append(LineString([Point(xy[0], xy[1]) for xy in i]).wkt)


#geo_df = GeoDataFrame(FC_list, geometry=coords_list)
