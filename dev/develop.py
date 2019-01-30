
from api_keys import google_api_key
import googlemaps
from sumo import SearchGrid
from shapely.geometry import Point
import pandas as pd
import geopandas as gpd
import geoplot
import geoplot.crs as gcrs

%load_ext autoreload
%autoreload


name = 'Loerrach, Baden-Wuerttemberg, Germany'

loerrach = SearchGrid(name)
loerrach.get_buildings()
loerrach.create_grid(1000, 1000)
loerrach.crop_grid()
loerrach.get_radius()
################################################
# test
###############################################

x = loerrach.grid.centroid.x.iloc[0]
y = loerrach.grid.centroid.y.iloc[0]

location = [y, x]


def get_type(type):


gmaps = googlemaps.Client(key=google_api_key)

radius = loerrach.radius
type = 'store'

l_x = []
l_y = []
l_names = []

for cell in loerrach.grid.centroid:
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


b = geoplot.polyplot(loerrach.buildings, linewidth=0.5)
geoplot.pointplot(gdf, ax=b, linewidth=3)


test = loerrach.grid.head(1)
test.crs = {'init': 'epsg:4326'}
test_utm = test.to_crs({'init': 'epsg:32632'})
test_utm_buffer = test_utm.buffer(1400)

test_wgs_buffer = test_utm_buffer.to_crs({'init': 'epsg:4326'})

loerrach.grid.crs = {'init': 'epsg:4326'}

loerrach.grid.plot()
gdf.plot()
test_wgs_buffer.plot()
b = geoplot.polyplot(loerrach.grid.head(1), linewidth=5)
geoplot.pointplot(gdf, ax=b, linewidth=3)
geoplot.polyplot(test_wgs_buffer, ax=b, linewidth=0.5)


# visualize

b = geoplot.polyplot(loerrach.buildings, linewidth=0.5, projection=gcrs.AlbersEqualArea())
geoplot.polyplot(loerrach.grid, ax=b, linewidth=0.5)
geoplot.pointplot(gdf, ax=b, linewidth=3)
geoplot.pointplot(loerrach.grid.centroid.head(1).buffer(1400), ax=b, linewidth=10)
