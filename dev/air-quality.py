
import requests
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import json
from pandas.io.json import json_normalize

endpoint = 'http://api.luftdaten.info/static/v2/data.24h.json'

response = requests.get(endpoint)
data = response.json()
data_str = json.load(data)


id = [i['id'] for i in data]
lat = [float(i['location']['latitude']) for i in data]
lon = [float(i['location']['longitude']) for i in data]
value = [float(i['sensordatavalues'][0]['value']) for i in data]
type = [i['sensordatavalues'][0]['value_type'] for i in data]

data_df = pd.DataFrame({
    'id': id,
    'lat': lat,
    'lon': lon,
    'value': value,
    'value_type': type
})

data_df['geometry'] = list(zip(data_df['lon'], data_df['lat']))
data_df['geometry'] = data_df['geometry'].apply(Point)
data_gdf = gpd.GeoDataFrame(data_df, geometry='geometry')
data_gdf.crs = {'init': 'epsg:4326'}
data_gdf = data_gdf.to_crs({'init': 'epsg:3035'})
data_gdf.size

# load project region
region_path = '../data/project_region/region.shp'
project_region = gpd.read_file(region_path)

in_proj = gpd.sjoin(data_gdf, project_region, how='left')
in_proj = in_proj.dropna()
in_proj.value_type.unique()

p1_values = in_proj[in_proj.value_type == 'P1']

p1_values.value[p1_values.value < 2000].plot()

p1_values[in_proj.value < 1000].plot(column='value', legend=True, scheme='quantiles')
