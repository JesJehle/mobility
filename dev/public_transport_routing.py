
import requests
from tools.utiles import get_coords_from_address
from tools.api_keys import here_app_code, here_app_id

start = get_coords_from_address('Reutebachgasse, Freiburg, Germany')
end = get_coords_from_address('VAG Zentrum, Freiburg, Germany')

# make own request to have additional information
transit_routing_url = 'https://transit.api.here.com/v3/route.json'
params = {}
params['app_id'] = here_app_id
params['app_code'] = here_app_code
params['dep'] = ','.join(list(map(str, start)))
params['arr'] = ','.join(list(map(str, end)))
params['time'] = '2019-04-10T10:40:00'
params['routingMode'] = 'realtime'



response = requests.get(transit_routing_url, params=params)
response.json()
