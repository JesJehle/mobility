import datetime


def get_time_difference(stringDep, StringArr):

    dep_time = datetime.datetime.strptime(stringDep.split('T')[1], '%H:%M:%S').time()
    dep_time_delta = datetime.timedelta(
        hours=dep_time.hour, minutes=dep_time.minute, seconds=dep_time.second)

    arr_time = datetime.datetime.strptime(StringArr.split('T')[1], '%H:%M:%S').time()
    arr_time_delta = datetime.timedelta(
        hours=arr_time.hour, minutes=arr_time.minute, seconds=arr_time.second)

    difference = arr_time_delta - dep_time_delta
    return int(difference.total_seconds()/60)



def add_to_dict(times_dict, new_times, new_stations):
    for i in range(len(new_times)):
        try:
            times_dict[new_stations[i]].append(new_times[i])
        except KeyError:
            times_dict.update(
            {new_stations[i]: [new_times[i]]})

    return times_dict



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