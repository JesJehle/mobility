from api_keys import google_api_key
import googlemaps
from sumo import SearchGrid
from shapely.geometry import Point
import pandas as pd
import geopandas as gpd
import geoplot
import geoplot.crs as gcrs
from matplotlib.pyplot import savefig
import osmnx as ox
from sumo_tools import request_travel_time_google, create_origin_destination_df, aggregate_travel_time, extract_info
import datetime
import googlemaps as gmaps
%load_ext autoreload
%autoreload

# helper functions


def get_streets(city_name, street_type='drive_service'):
    city_boundary = ox.gdf_from_place(city_name).geometry.iloc[0]
    drive_net = ox.graph_from_polygon(city_boundary, network_type=street_type)
    drive_gpd = ox.graph_to_gdfs(drive_net, nodes=False)
    return drive_gpd


def get_type(city_class, type,):

    gmaps = googlemaps.Client(key=google_api_key)
    radius = city_class.radius
    type = type
    l_x = []
    l_y = []
    l_names = []

    for cell in city_class.grid.centroid:
        x = cell.x
        y = cell.y
        location = [y, x]
        places = gmaps.places_nearby(location=location, radius=radius, type=type)

        for result in places['results']:
            l_names.append(result['name'])
            l_x.append(result['geometry']['location']['lng'])
            l_y.append(result['geometry']['location']['lat'])

    df = pd.DataFrame(
        {'name': l_names,
         'x': l_x,
         'y': l_y})

    df['Coordinates'] = list(zip(df.x, df.y))
    df['Coordinates'] = df['Coordinates'].apply(Point)
    gdf = gpd.GeoDataFrame(df, geometry='Coordinates')
    gdf.crs = {'init': 'epsg:4326'}
    return gdf


name = 'Loerrach, Baden-Wuerttemberg, Germany'

loerrach = SearchGrid(name)
loerrach.get_buildings()


## plot building #####################
b = geoplot.polyplot(loerrach.buildings,  linewidth=0.5)
geoplot.polyplot(loerrach.city_boundary,  ax=b, linewidth=0.5)
savefig('buildings.png', dpi=200)

# plot streets
service_streets = get_streets(name, street_type='drive_service')
b = geoplot.polyplot(loerrach.buildings, linewidth=0.5)
service_streets.plot(ax=b, color='grey', linewidth=0.5)
geoplot.polyplot(loerrach.city_boundary,  ax=b, linewidth=0.5)
savefig('service_streets.png', dpi=200)

# plot bike streets
service_streets = get_streets(name, street_type='bike')
b = geoplot.polyplot(loerrach.buildings, linewidth=0.5)
service_streets.plot(ax=b, color='grey', linewidth=0.5)
geoplot.polyplot(loerrach.city_boundary,  ax=b, linewidth=0.5)
savefig('bike_streets.png', dpi=200)

# plot bike streets
service_streets = get_streets(name, street_type='walk')
b = geoplot.polyplot(loerrach.buildings, linewidth=0.5)
service_streets.plot(ax=b, color='grey', linewidth=0.5)
geoplot.polyplot(loerrach.city_boundary,  ax=b, linewidth=0.5)
savefig('walk_streets.png', dpi=200)

# plot bike streets
service_streets = get_streets(name, street_type='all_private')
b = geoplot.polyplot(loerrach.buildings, linewidth=0.5)
service_streets.plot(ax=b, color='grey', linewidth=0.5)
geoplot.polyplot(loerrach.city_boundary,  ax=b, linewidth=0.5)
savefig('all_private_streets.png', dpi=200)


# plot transport stations
loerrach.create_grid(1000, 1000)
loerrach.crop_grid()
loerrach.get_radius()

# plot bus stations
stations = get_type(loerrach, 'bus_station')
states_l = gpd.sjoin(stations, loerrach.city_boundary, how='left')

stations_l = states_l.dropna(subset=['index_right'], how='all')

service_streets = get_streets(name, street_type='drive_service')

b = geoplot.polyplot(loerrach.buildings, linewidth=0.5)
service_streets.plot(ax=b, color='grey', linewidth=0.5)
stations_l.plot(ax=b, color='blue', linewidth=5, markersize=5)
geoplot.polyplot(loerrach.city_boundary,  ax=b, linewidth=0.5)
savefig('bus_stations.png', dpi=200)

# plot parking places
parking_all = get_type(loerrach, 'parking')
parking_all_join = gpd.sjoin(parking_all, loerrach.city_boundary, how='left')

parking = parking_all_join.dropna(subset=['index_right'], how='all')
service_streets = get_streets(name, street_type='drive_service')
b = geoplot.polyplot(loerrach.buildings, linewidth=0.5)
service_streets.plot(ax=b, color='grey', linewidth=0.5)
parking.plot(ax=b, color='blue', linewidth=5, markersize=5)
geoplot.polyplot(loerrach.city_boundary,  ax=b, linewidth=0.5)
savefig('parking.png', dpi=200)

# plot stores
stores = get_type(loerrach, 'store')
stores_l = gpd.sjoin(stores, loerrach.city_boundary, how='left')

stores_l_final = stores_l.dropna(subset=['index_right'], how='all')

b = geoplot.polyplot(loerrach.buildings, linewidth=0.5)
service_streets.plot(ax=b, color='grey', linewidth=0.5)
stores_l_final.plot(ax=b, color='blue', linewidth=5, markersize=5)
geoplot.polyplot(loerrach.city_boundary,  ax=b, linewidth=0.5)
savefig('stores.png', dpi=200)

# plot schools
school_res = get_type(loerrach, 'school')
school_l = gpd.sjoin(school_res, loerrach.city_boundary, how='left')

school = school_l.dropna(subset=['index_right'], how='all')

b = geoplot.polyplot(loerrach.buildings, linewidth=0.5)
service_streets.plot(ax=b, color='grey', linewidth=0.5)
school.plot(ax=b, color='blue', linewidth=5, markersize=5)
geoplot.polyplot(loerrach.city_boundary,  ax=b, linewidth=0.5)
savefig('schools.png', dpi=200)


# plot schools
school_res = get_type(loerrach, 'school')
school_l = gpd.sjoin(school_res, loerrach.city_boundary, how='left')

school = school_l.dropna(subset=['index_right'], how='all')

b = geoplot.polyplot(loerrach.buildings, linewidth=0.5)
service_streets.plot(ax=b, color='grey', linewidth=0.5)
school.plot(ax=b, color='blue', linewidth=5, markersize=5)
geoplot.polyplot(loerrach.city_boundary,  ax=b, linewidth=0.5)
savefig('schools.png', dpi=200)

# plot grid
b = geoplot.polyplot(loerrach.buildings, linewidth=0.5)
service_streets.plot(ax=b, color='grey', linewidth=0.5)
geoplot.polyplot(loerrach.grid,  ax=b, linewidth=0.5)
loerrach.nearest_p.plot(ax=b, color='red', linewidth=5)
savefig('grid.png', dpi=200)


# plot mean travel time car
loerrach.get_nearest_point()
# distanc_matrix_df = create_origin_destination_df(loerrach.nearest_p.geometry)
# travel_time_car_df = request_travel_time_google(distanc_matrix_df, mode='driving')
# travel_time_car_df.to_csv('travel_time_car_google.csv')
travel_time_car_df = pd.read_csv('travel_time_car_google.csv')
travel_time_car_aggregated = aggregate_travel_time(travel_time_car_df)
loerrach.nearest_p['duration'] = travel_time_car_aggregated.duration

b = geoplot.polyplot(loerrach.buildings, linewidth=0.5)
service_streets.plot(ax=b, color='grey', linewidth=0.5)
loerrach.nearest_p.plot(ax=b, column='duration', cmap='plasma', legend=True, markersize=100)
geoplot.polyplot(loerrach.city_boundary,  ax=b, linewidth=0.5)
savefig('car_travel_time.png', dpi=200)

# plot mean puplic transport travel time
travel_time_transit_df = pd.read_csv('data/travel_time_t_df_loerrach.csv')
travel_time_transit_aggregated = aggregate_travel_time(travel_time_transit_df)
loerrach.nearest_p['duration_t'] = travel_time_transit_aggregated.duration

b = geoplot.polyplot(loerrach.buildings, linewidth=0.5)
service_streets.plot(ax=b, color='grey', linewidth=0.5)
loerrach.nearest_p.plot(ax=b, column='duration_t', cmap='plasma', legend=True, markersize=100)
geoplot.polyplot(loerrach.city_boundary,  ax=b, linewidth=0.5)
savefig('transit_travel_time.png', dpi=200)

# plot mean bike travel time
#distanc_matrix_df = create_origin_destination_df(loerrach.nearest_p.geometry)
#travel_time_car_df = request_travel_time_google(distanc_matrix_df, mode='bicycling')
# travel_time_car_df.to_csv('bike_travel_time_google.csv')
travel_time_bike_df = pd.read_csv('bike_travel_time_google.csv')
travel_time_bike_aggregated = aggregate_travel_time(travel_time_bike_df)
loerrach.nearest_p['duration_b'] = travel_time_bike_aggregated.duration

b = geoplot.polyplot(loerrach.buildings, linewidth=0.5)
service_streets.plot(ax=b, color='grey', linewidth=0.5)
loerrach.nearest_p.plot(ax=b, column='duration_b', cmap='plasma', legend=True, markersize=100)
geoplot.polyplot(loerrach.city_boundary,  ax=b, linewidth=0.5)
savefig('bike_travel_time.png', dpi=200)


# time line congestion
selection = loerrach.nearest_p.geometry.iloc[[1, 3, 6, 15, 20, 30]]
destination_maxtrix_selection = create_origin_destination_df(selection)


times = list(range(1, 25))
mean_time = []

for t in times:
    time = datetime.datetime(2018, 11, 26, 9)
    travel_time_car_9 = request_travel_time_google(
        destination_maxtrix_selection, departure_time=time, mode='driving')
    travel_time_car_9.duration.mean()
    mean_time.append(travel_time_car.duration.mean())


basel = (47.563392, 7.580051)
freiburg = (47.991322, 7.752478)

traffic_model = 'pessimistic'
gmaps = googlemaps.Client(key=google_api_key)

times = list(range(1, 24))
b_f_duration = []

for t in times:
    time = datetime.datetime(2018, 11, 27, t)
    response = gmaps.distance_matrix(basel, freiburg, mode='driving',
                                     departure_time=time, traffic_model=traffic_model)
    duration_sec = response['rows'][0]['elements'][0]['duration_in_traffic']['value']
    b_f_duration.append(round(duration_sec / 60))


df = pd.DataFrame({'time': times, 'mean_car_travel_time_basel_freiburg': b_f_duration})
df = df.set_index('time')
df.plot()
savefig('mean_car_travel_time_basel_freiburg.png', dpi=200)


b = geoplot.polyplot(loerrach.buildings, linewidth=0.5)
selection.plot(ax=b)

gmaps = googlemaps.Client(key=google_api_key)

radius = loerrach.radius
radius = 10000
types = 'bus_station'

x = loerrach.grid.centroid.x.iloc[0]
y = loerrach.grid.centroid.y.iloc[0]

location = [y, x]
places = gmaps.places_nearby(location=location, radius=radius, type=types)


stores = get_type(loerrach, '')
