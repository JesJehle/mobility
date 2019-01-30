
def test_format_time_for_request():
	from tools.travel_time_pt import format_time_for_request
	import datetime
	time_input = datetime.datetime(2019, 2, 2, 10, 0)
	time_output = '2019-02-02T10:00:00'
	assert format_time_for_request(time_input) == time_output



def test_request_pt_route():
	import datetime
	from tools.api_keys import here_app_code, here_app_id
	from tools.travel_time_pt import request_pt_route

	date_time = datetime.datetime(2019, 2, 2, 10, 0)
	start = [48.022917, 7.858326]
	end = [48.007457, 7.855260]

	route = request_pt_route(here_app_id, here_app_code, date_time, start, end)
	assert isinstance(route['Res'], dict)




with open("tests/data/pt_test_route_simple.json", 'r') as f:
	response = json.load(f)


def extract_travel_times(here_pt_response):
	time = []
	ids = []
	stops_x = []
	stops_y = []
	names = []
	for connection in here_pt_response['Res']['Connections']['Connection']:
		dep_time_ = connection['Dep']['time']
		for section in connection['Sections']['Sec']:
			for i in section['Journey'].get('Stop', '0'):
				if isinstance(i, dict):
					try:
						time_ = i['arr']
					except KeyError:
						time_ = i['dep']
					finally:
						time_diff_ = get_time_difference(dep_time_, time_)
						time.append(time_diff_)
						ids.append(i['Stn']['id'])
						stops_x.append(i['Stn']['x'])
						stops_y.append(i['Stn']['y'])
						names.append(i['Stn']['name'])

	return time, ids, stops_x, stops_y, names




assert len(time) == len(ids)
