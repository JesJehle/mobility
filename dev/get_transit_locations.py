
import json
from datetime import datetime
from herepy import PublicTransitRoutingType
import requests
from tools.api_keys import here_app_code, here_app_id
import geopandas as gpd
import pandas as pd
from geopandas import GeoDataFrame
from shapely.geometry import Point
from tools.utiles import get_coords_from_address
# find stations in a radius
find_stations_url = 'https://transit.api.here.com/v3/stations/by_geocoord.json'

# response = requests.get(find_stations_url, params=params)
# res = response.json()

test_loaction = get_coords_from_address('Freiburg, Germany')

from tools.travel_time_pt import PubTransRouter

pt_routter = PubTransRouter(here_app_id, here_app_code)

stations = pt_routter.find_station(test_loaction)



# by id test !!!!
# only possible for busses
station = 'db_808280'
params = {}
params['app_id'] = here_app_id
params['app_code'] = here_app_code
params['stnId'] = station
#params['center'] = ','.join(list(map(str, location)))
params['time'] = '2019-06-24T07:30:00'
params['max'] = 100

info_by_id_url = 'https://transit.api.here.com/v3/board.json'

response = requests.get(info_by_id_url, params=params)
response.json()



# next departure test
test_loaction = get_coords_from_address('Ebringen, Germany')

params = {}
params['app_id'] = here_app_id
params['app_code'] = here_app_code
params['center'] = ','.join(list(map(str, test_loaction)))
#params['center'] = ','.join(list(map(str, location)))
params['time'] = '2019-06-24T10:30:00'
params['max'] = 100
params['maxStn'] = 40
params['radius'] = 10000

iso_url = 'https://transit.api.here.com/v3/multiboard/by_geocoord.json'

response = requests.get(iso_url, params=params)
res = response.json()


for i in res['Res']['MultiNextDepartures']['MultiNextDeparture']:
    print(i)



for i in res['Res']['MultiNextDepartures']['MultiNextDeparture'][0]['NextDepartures']['Dep'][0]['Transport']['dir']:
    print(i)









y_coord = []
x_coord = []
station_name = []
station_id = []
has_board = []
mode = []
line = []
direction = []

y = grid['geometry'].centroid.y.tolist()
x = grid['geometry'].centroid.x.tolist()


for item in range(len(x)):
    y_ = y[item]
    x_ = x[item]
    params['center'] = str(y_) + ',' + str(x_)
    response = requests.get(find_stations_url, params=params)
    response_jsom = response.json()
    try:
        for station in response_jsom['Res']['Stations']['Stn']:
            station_name.append(station['name'])
            station_id.append(station['id'])
            has_board.append(station['has_board'])
            line.append([i['name'] for i in station['Transports']['Transport']])
            mode.append([i['mode'] for i in station['Transports']['Transport']])
            direction.append([i['dir'] for i in station['Transports']['Transport']])
            y_coord.append(station['y'])
            x_coord.append(station['x'])
    except Exception as e:
        pass


df = pd.DataFrame(
    {
        'y': y_coord,
        'x': x_coord,
        'station_name': station_name,
        'station_id': station_id,
        'has_board': has_board,
        'lines': line,
        'mode': mode,
        'direction': direction
    }
)

df_unique = df.drop_duplicates('station_id')

geometry = [Point(xy) for xy in zip(df_unique.x, df_unique.y)]

# get intervals of a station

crs = {'init': 'epsg:4326'}
gdf = GeoDataFrame(df_unique, crs=crs, geometry=geometry)


gdf[['station_id', 'station_name', 'geometry']].to_file('./data/freiburg/stations.shp')

modes_list = gdf['mode'].tolist()
flat_list = [item for sublist in mode_list for item in sublist]
set(flat_list)

gdf.dtypes

line_list = gdf['lines'].tolist()
flat_list = [item for sublist in line_list for item in sublist]
set(flat_list)


mode_list.f
geo = gdf['geometry'].to_json()
m = folium.Map(location=location)
m.choropleth(
    geo_data=geo,
    name='choropleth',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='grid'
)

m.save('transit_stations.html')


#
#
# station_info_url = 'https://transit.api.here.com/v3/multiboard/by_geocoord.json'
# params = {}
# params['app_id'] = here_app_id
# params['app_code'] = here_app_code
# params['center'] = ','.join(list(map(str, location)))
# params['time'] = '2019-11-19T07:30:00'
# params['maxStn'] = 1
# params['max'] = 50
# params['radius'] = 500
#
#
# response_info = requests.get(station_info_url, params=params)
# res_info = response_info.json()
