from shapely.geometry import Point
import geopandas as gpd
from numpy import nan
import pandas as pd
from api_keys import google_api_key
import googlemaps
import osmnx as ox
from utiles import SearchGrid, get_coords_from_address
import sys
sys.path.append('/home/jesjehle/Documents/Mobility/sumo/tools')


# grid_freiburg = SearchGrid('Lörrach, Germany', 1000, 1000)
#
# one_grid = grid_freiburg.grid.iloc[0:1]
#
#
# location = [one_grid.centroid.y, one_grid.centroid.x]
# radius = 1000
# type = 'store'
# places = gmaps.places_nearby(location=location, radius=radius, type=type)
#

# class PlacesData:
#     def __init__(self, city_name):

def get_type(grid, radius, type):

    gmaps = googlemaps.Client(key=google_api_key)
    l_x = []
    l_y = []
    l_place_id = []
    l_rating = []
    l_user_rating = []
    l_types = []
    l_names = []

    for cell in grid.centroid:
        x = cell.x
        y = cell.y
        location = [y, x]
        places = gmaps.places_nearby(location=location, radius=radius, type=type)

        for result in places['results']:
            l_names.append(result['name'])
            l_place_id.append(result['place_id'])
            try:
                l_rating.append(result['rating'])
            except KeyError:
                l_rating.append(nan)
            try:
                l_user_rating.append(result['user_ratings_total'])
            except KeyError:
                l_user_rating.append(nan)
            l_types.append(result['types'])
            l_x.append(result['geometry']['location']['lng'])
            l_y.append(result['geometry']['location']['lat'])

    df = pd.DataFrame(
        {'name': l_names,
         'rating': l_rating,
         'user_rating': l_user_rating,
         'place_id': l_place_id,
         'types': l_types,
         'x': l_x,
         'y': l_y})

    df['Coordinates'] = list(zip(df.x, df.y))
    df['Coordinates'] = df['Coordinates'].apply(Point)
    gdf = gpd.GeoDataFrame(df, geometry='Coordinates')
    gdf.crs = {'init': 'epsg:4326'}

    gdf_unique = gdf.drop_duplicates('place_id')
    return gdf_unique

    def get_unique_values_of_column(column):
        col_list = column.tolist()
        flat_list = [item for sublist in col_list for item in sublist]
        return set(flat_list)

'./data/freiburg/grid_1km_fr.shp'
grid = gpd.read_file('../data/freiburg/grid_1km_fr.shp')
len(grid)

# get supermarkets --------------------------------------------------
supermarkets_fr = get_type(grid, type='supermarket', radius=1000)
supermarkets_fr_clean = supermarkets_fr.drop_duplicates(
    'place_id')[['name', 'rating', 'user_rating', 'place_id', 'Coordinates']]
supermarkets_fr_clean.to_file('data/freiburg/supermarkets.shp')
supermarkets_fr_clean.sort_values('rating')
get_unique_values_of_column(supermarkets_fr['types'])

# get parks ---------------------------------------------------
parks = get_type(grid, type='park', radius=1000)
parks_unique = parks.drop_duplicates('place_id')
parks_unique[['name', 'rating', 'user_rating', 'place_id',
              'Coordinates']].to_file('data/freiburg/parks.shp')
get_unique_values_of_column(parks_unique['types'])

# get shopping facilities ----------------------------------------

store = get_type(grid, type='store', radius=1000)
store[['name', 'rating', 'user_rating', 'place_id',
       'Coordinates']].to_file('data/freiburg/stores.shp')
get_unique_values_of_column(store['types'])

# get cafes --------------------------------------------------
cafes = get_type(grid, type='cafe', radius=1000)
cafes[['name', 'rating', 'user_rating', 'place_id',
       'Coordinates']].to_file('data/freiburg/cafes.shp')
get_unique_values_of_column(cafes['types'])

# get bars ------------------------------------------------
bars = get_type(grid, type='bar', radius=1000)
bars[['name', 'rating', 'user_rating', 'place_id', 'Coordinates']].to_file('data/freiburg/bars.shp')
get_unique_values_of_column(bars['types'])

# get restaurants -------------------------------------------
restaurants = get_type(grid, type='restaurant', radius=1000)
restaurants[['name', 'rating', 'user_rating', 'place_id',
             'Coordinates']].to_file('data/freiburg/restaurants.shp')
get_unique_values_of_column(restaurants['types'])

# get doctors -----------------------------------------
doctor = get_type(grid, type='doctor', radius=1000)
doctor[['name', 'rating', 'user_rating', 'place_id',
        'Coordinates']].to_file('data/freiburg/doctor.shp')
get_unique_values_of_column(doctor['types'])

# get hospital ---------------------------------------
hospital = get_type(grid, type='hospital', radius=1000)
hospital[['name', 'rating', 'user_rating', 'place_id',
          'Coordinates']].to_file('data/freiburg/hospital.shp')
get_unique_values_of_column(hospital['types'])

# get parking ---------------------------------------
parking = get_type(grid, type='parking', radius=1000)
parking[['name', 'rating', 'user_rating', 'place_id',
         'Coordinates']].to_file('data/freiburg/parking.shp')
get_unique_values_of_column(parking['types'])

# get schools ----------------------------------------
school = get_type(grid, type='school', radius=1000)
school[['name', 'rating', 'user_rating', 'place_id',
        'Coordinates']].to_file('data/freiburg/schools_all.shp')

# clean and devide schools ----------------------------------------------------
school_type_list = school['types'].tolist()
no_store = []
for l in school_type_list:
    sub_list = []
    for item in l:
        if item == "store":
            sub_list.append(True)
    if len(sub_list) == 1:
        no_store.append(False)
    else:
        no_store.append(True)

school_no_stores = school[no_store]

kindergarten = school_no_stores[school_no_stores['name'].str.contains('kinder|kita', case=False)]
kindergarten[['name', 'rating', 'user_rating', 'place_id',
              'Coordinates']].to_file('data/freiburg/kindergarten.shp')
schools = school_no_stores[school_no_stores['name'].str.contains(
    'waldorf|real|grund|haupt|gesamt|gymna', case=False)]
schools[['name', 'rating', 'user_rating', 'place_id',
         'Coordinates']].to_file('data/freiburg/schools_general.shp')
schools_rest = school_no_stores[~school_no_stores['name'].str.contains(
    'waldorf|kinder|kita|real|grund|haupt|gesamt|gymna', case=False)]
schools_rest[['name', 'rating', 'user_rating', 'place_id',
              'Coordinates']].to_file('data/freiburg/schools_rest.shp')
school_selection.name

school[['name', 'rating', 'user_rating', 'place_id',
        'Coordinates']].to_file('data/freiburg/school.shp')
get_unique_values_of_column(parking['types'])


# test sample of stores

grid_sample = grid.sample(30)
grid_sample.plot()
store_test = get_type(grid_sample, type='store', radius=1500)
len(store.drop_duplicates('place_id'))
len(store_test)
store[['name', 'rating', 'user_rating', 'place_id',
       'Coordinates']].to_file('data/freiburg/stores.shp')
get_unique_values_of_column(store['types'])
