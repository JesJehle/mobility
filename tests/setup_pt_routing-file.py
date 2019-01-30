import datetime
import json
from tools.api_keys import here_app_code, here_app_id
from tools.travel_time_pt import request_pt_route

date_time = datetime.datetime(2019, 2, 2, 10, 0)

Reuterbachgasse = [48.022917, 7.858326]
Hauptstrasse = [48.007457, 7.855260]

response = request_pt_route(here_app_id, here_app_code,date_time, Reuterbachgasse, Hauptstrasse)

with open('pt_test_route_simple.json', 'w') as f:
    json.dump(response, f)

