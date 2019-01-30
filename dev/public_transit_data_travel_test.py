import json
from datetime import datetime
from herepy import PublicTransitRoutingType
import requests
import herepy
from utiles import get_coords_from_address
from api_keys import here_app_code, here_app_id

start = get_coords_from_address('In den Weihermatten 19, Freiburg, Germany')
end = get_coords_from_address('Auf der Haid, Freiburg, Germany')

# coverage
publicTransitApi = herepy.PublicTransitApi(here_app_id, here_app_code)
coverage = publicTransitApi.coverage_nearby(center=start, details=1)
coverage.as_dict()

# station inforation
# stations = publicTransitApi.coverage_witin_a_city(city_name='Freiburg, Germany', political_view='FRE')
stations = publicTransitApi.find_stations_nearby(center=start, radius=5000, max_count=50)
stds = stations.as_dict()

for std in stds['Res']['Stations']['Stn']:
    print(std)

station_id = stds['Res']['Stations']['Stn'][0]['id']
station_info = publicTransitApi.find_stations_by_name(name='Freiburg-Zährungen', center=start)
station_info.as_dict()

station_info = publicTransitApi.find_stations_by_id('db_8002071', 'en')


# make own request to have additional information
transit_converage_url = 'https://transit.api.here.com/v3/coverage/search.json'
params = {}
params['app_id'] = here_app_id
params['app_code'] = here_app_code
params['name'] = 'Freiburg, Germany'
params['max'] = 10
params['details'] = 1
#params['politicalview'] = 0
response = requests.get(transit_converage_url, params=params)
response.json()


# routing
# look for timetable data
time = str(datetime.now())
time = '2019-01-15T12:30:54'
PublicTransitRoutingType.time_tabled
route = publicTransitApi.calculate_route(
    departure=start, time=time, arrival=end, routing_type=PublicTransitRoutingType.time_tabled)


transit_route_url = 'https://transit.api.here.com/v3/route.json'
params = {}
params['app_id'] = here_app_id
params['app_code'] = here_app_code
params['dep'] = str(start[0]) + ',' + str(start[1])
params['arr'] = str(end[0]) + ',' + str(end[1])
params['time'] = time
params['routing'] = 'tt'

response = requests.get(transit_route_url, params=params)
res_json = response.json()
with open('transit-routing.json', 'w') as fp:
    json.dump(res_json, fp)
