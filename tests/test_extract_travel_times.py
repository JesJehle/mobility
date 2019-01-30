import json
import sys
sys.path.append('/home/jesjehle/Documents/Mobility/sumo/tools')
# load the test response data
from travel_time_pt import extract_travel_times
import os
print(os.getcwd())
with open("data/transit-routing.json", 'r') as f:
	response = json.load(f)


time, ids, stops_x, stops_y, names = extract_travel_times(response)

assert len(time) == len(ids)