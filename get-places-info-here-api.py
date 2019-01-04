
import requests

from api_keys import here_app_id, here_app_code

url = 'https://cle.api.here.com/2/search/proximity.json'

payload = {}
payload['app_id'] = here_app_id
payload['app_code'] = here_app_code
payload['proximity'] = '52.5079549, 13.5472861, 5000'
payload['layer_ids'] = '30'
# request to api


response = requests.get(url, params=payload)

response.request.path_url

respnse_json = response.json()
summary = respnse_json['response']['route'][0]['summary']
distance.append(summary['distance'])
traffic_time.append(summary['trafficTime'])
base_time.append(summary['baseTime'])
travel_time.append(summary['travelTime'])


https: // cle.api.here.com/2/search/proximity.json?app_id = {YOUR_APP_ID} & app_code = {YOUR_APP_CODE} & proximity = 50.113905, 8.677608, 500 & layer_ids = 30
