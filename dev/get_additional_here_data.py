

#%%

import json
from datetime import datetime
import requests
from tools.api_keys import here_app_code, here_app_id
import geopandas as gpd
import pandas as pd
from geopandas import GeoDataFrame
from shapely.geometry import Point
from tools.utiles import get_coords_from_address
# find stations in a radius
#%%


def list_available_attributes(app_id, app_code):
    av_attr_url = 'https://pde.api.here.com/1/doc/attributes.json'
    params = {}
    params['app_id'] = here_app_id
    params['app_code'] = here_app_code

    response = requests.get(av_attr_url, params=params)
    res = response.json()
    return res



attributes = list_available_attributes(here_app_id, here_app_code)



for att in attributes:
    if 'walk' in str(att):
        print(att)



layer = 'lkjasdf'

layers = list_available_attributes(here_app_id, here_app_code)



# response = requests.get(find_stations_url, params=params)
# res = response.json()


start = get_coords_from_address('Reutebachgasse, Freiburg, Germany')

end = get_coords_from_address('Tennenbacher Str. 4,Freiburg im Breisgau, Germany')


# request route

url = 'https://route.api.here.com/routing/7.2/calculateroute.json'
payload = {}
payload['app_id'] = here_app_id
payload['app_code'] = here_app_code

# payload['mode'] = 'fastest;car'
payload['mode'] = 'fastest;bicycle'

payload['routeattributes'] = 'legs'
payload['legAttributes'] = 'links,shape'
payload['linkAttributes'] = 'dynamicSpeedInfo,functionalClass'
payload['returnelevation'] = 'true'

#payload['routeLinkAttributes'] = 'speedLimit'
#payload['routeLegAttributes'] = 'trafficTime'


    # request to api

payload['waypoint0'] = 'geo!' + str(start[0]) + ',' + str(start[1])
payload['waypoint1'] = 'geo!' + str(end[0]) + ',' + str(end[1])
response_ = requests.post(url, params=payload)
routing_res = response_.json()
# routing_res


for i in routing_res['response']['route'][0]['leg'][0]:
    print(i)


for i in routing_res['response']['route'][0]['waypoint']:
    print(i)


routing_res['response']['route'][0]['leg']

# by id test !!!!
# only possible for busses
#params['center'] = ','.join(list(map(str, location)))


for att in attributes:
    if 'LANE' in str(att):
        print(att)


def list_available_layers(app_id, app_code, layer=None):
    av_attr_url = 'https://pde.api.here.com/1/doc/layers.json'
    params = {}
    if not layer is None:
        params['layer'] = layer
    params['app_id'] = here_app_id
    params['app_code'] = here_app_code

    response = requests.get(av_attr_url, params=params)
    res = response.json()
    return res


def list_available_attributes(app_id, app_code):
    av_attr_url = 'https://pde.api.here.com/1/doc/attributes.json'
    params = {}
    params['app_id'] = here_app_id
    params['app_code'] = here_app_code

    response = requests.get(av_attr_url, params=params)
    res = response.json()
    return res



list_available_layers(here_app_id, here_app_code, layer='LINK_ATTRIBUTE_FC3')




tile_url = 'https://pde.api.here.com/1/tile.json'
layer = 'LANE_FC2'
level = 10

tileSizeDegree = 180.0 / (2 ** level)
from numpy import round
tiley = int((start[0] +  90.0) / tileSizeDegree)
tilex = int((start[1] + 180.0) / tileSizeDegree)

params = {}
params['app_id'] = here_app_id
params['app_code'] = here_app_code
params['layer'] = layer
params['level'] = level

params['tilex'] = tilex
params['tiley'] = tiley


response = requests.get(tile_url, params=params)
limits_res = response.json()


routing_link_list = [abs(int(i['linkId'])) for i in routing_res['response']['route'][0]['leg'][0]['link']]

limits_link_list = [abs(int(i['LINK_ID'])) for i in limits_res['Rows']]



for i in routing_link_list:
    if i in limits_link_list:
        print('found')









def get_layer_info(attribute):

    tile_url = 'https://pde.api.here.com/1/doc/layer.json'
    layer = attribute

    params['app_id'] = here_app_id
    params['app_code'] = here_app_code
    params['layer'] = layer

    response = requests.get(tile_url, params=params)
    res = response.json()
    return res







layers = list_available_layers(here_app_id, here_app_code)




prox_url = 'https://pde.api.here.com' + '/1/' + 'search/proximity.json'
layer_ids = 'TRAFFIC_SPEED_RECORD_FC1'
radius = 1000
key_attributes = 'SPEED_LIMITS_FC3'

params = {}
params['app_id'] = here_app_id
params['app_code'] = here_app_code
params['layer_ids'] = layer_ids
params['key_attributes'] = key_attributes

test_loaction_rev = test_loaction.copy()
test_loaction_rev.reverse()
params['proximity'] = ','.join(list(map(str, test_loaction_rev))) + ',' + str(radius)


response = requests.get(prox_url, params=params)
response.json()





#%%
