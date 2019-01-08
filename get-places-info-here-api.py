
import herepy
import requests
import geopandas as gpd
from shapely.geometry import Point
from api_keys import here_app_id, here_app_code
import pandas as pd
import matplotlib as plt
import cartopy.crs as ccrs
url = 'https://cle.api.here.com/2/search/proximity.json'
url = 'https://pde.api.here.com/1/tile.json'

# request stuff i dont unserstand

url = "https://reverse.geocoder.api.here.com/6.2/reversegeocode.json"
header = {}
params = {}
params['app_id'] = here_app_id
params['app_code'] = here_app_code
params['prox'] = "47.6120896, 7.6607218, 10000"
params['mode'] = "retrieveAddresses"
params['locationAttributes'] = "linkInfo"
params['gen'] = 100
response = requests.get(url, params=params)
respnse_json = response.json()

for items in respnse_json['Response']['View'][0]['Result']:
    print(items['Location']['LinkInfo']['SpeedCategory'])

respnse_json['Response']['View'][0]['Result'][0]

['MapReference']

lat = []
lng = []
SpeedCategory = []

for results in respnse_json['Response']['View'][0]['Result']:
    lat.append(results['Location']['DisplayPosition']['Latitude'])
    lng.append(results['Location']['DisplayPosition']['Longitude'])
    SpeedCategory.append(results['Location']['LinkInfo']['SpeedCategory'])


df = pd.DataFrame(
    {'SpeedCategory': SpeedCategory,
     'x': lng,
     'y': lat})

df['Coordinates'] = list(zip(df.x, df.y))
df['Coordinates'] = df['Coordinates'].apply(Point)
gdf = gpd.GeoDataFrame(df, geometry='Coordinates')
gdf.crs = {'init': 'epsg:4326'}

extent = (gdf['Coordinates'].x.min(), gdf['Coordinates'].x.max(),
          gdf['Coordinates'].y.min(), gdf['Coordinates'].y.max())
ax = plt.axes([0, 0, 1, 1],
              projection=ccrs.LambertCylindrical())
ax.set_extent(extent, ccrs.LambertCylindrical())


map = gdf.plot(vmin=47.612, vmax=47.61)

map.set_

# try to get speed limit directly

url = 'https://route.api.here.com/routing/7.2/calculateroute.json'
header = {}
params = {}
params['app_id'] = here_app_id
params['app_code'] = here_app_code
params['mode'] = 'fastest;car;traffic:disabled'
params['waypoint0'] = 'geo!52.4999825,13.3999652'
params['waypoint1'] = 'geo!52.4979866,13.4476519'


response = requests.get(url, params=params)
respnse_json = response.json()


routingApi = herepy.RoutingApi(here_app_id, here_app_code)
response = routingApi.car_route([52.4999825, 13.3999652], [52.4979866, 13.4476519], [
                                herepy.RouteMode.car, herepy.RouteMode.fastest])


response.as_dict()


params['layer'] = 'SPEED_LIMITS_FC'
params['level'] = 9
params['tilex'] = 537
params['tiley'] = 399


#params['proximity'] = [52.5079549, 13.5472861]
#params['layer_ids'] = 30

# request to api


response = requests.get(url, headers=header, params=params)

response.text
response.request.path_url

respnse_json = response.json()
summary = respnse_json['response']['route'][0]['summary']
distance.append(summary['distance'])
traffic_time.append(summary['trafficTime'])
base_time.append(summary['baseTime'])
travel_time.append(summary['travelTime'])


https: // cle.api.here.com/2/search/proximity.json?app_id = {YOUR_APP_ID} & app_code = {YOUR_APP_CODE} & proximity = 50.113905, 8.677608, 500 & layer_ids = 30
