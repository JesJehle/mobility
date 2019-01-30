import pysal as ps
from pandas import DataFrame
import folium
from random import randint
from numpy import nan
import osmnx as ox
import geopandas as gpd
import json
#from datetime import datetime
import requests
from utiles import get_coords_from_address
from api_keys import here_app_code, here_app_id

start = get_coords_from_address('Reutebachgasse, Freiburg, Germany')

# make own request to have additional information
transit_isochrone_url = 'https://transit.api.here.com/v3/isochrone.json'
params = {}
params['app_id'] = here_app_id
params['app_code'] = here_app_code
params['maxDur'] = 20
params['center'] = ','.join(list(map(str, start)))
params['time'] = '2019-11-19T08:15:00'
params['timespan'] = 10
params['modes'] = 'bus'


response = requests.get(transit_isochrone_url, params=params)
response.json()


# population data freiburg
pop_bw = gpd.read_file("../data/population-bw/pop_demo.shp")
city_b = ox.gdf_from_place('Freiburg, Germany')

# city_b_proj = city_b.to_crs({'init': 'epsg:3035'})
# pop_bw_proj = pop_bw.to_crs({'init': 'epsg:3035'})

pop_bw.plot()
city_b.plot()
pop_bw.head(10).plot()

intersect = gpd.sjoin(pop_bw, city_b, how='left')

not_na = intersect['index_right'].notna()
pop_fr = intersect.loc[not_na]
cols_selection = ['Einwohner', '1', '2', '3', '4', '5', 'geometry']
pop_fr_selection = pop_fr[cols_selection]
for col in cols_selection[0:6]:
    pop_fr_selection[col] = pop_fr_selection[col].fillna(0)
    pop_fr_selection[col] = pop_fr_selection[col].astype('int')
    # pop_fr_selection[col]= pop_fr_selection[col].replace('-1', nan)


pop_fr_selection.plot(column='1', legend=True)


grid = gpd.read_file("../data/gitter/100_m_grid/100kmN27E41_DE_Grid_ETRS89-LAEA_100m.shp")
len(grid)

sample_index = [randint(0, 479081) for i in range(10000)]
grid_sample = grid.iloc[sample_index]

ax = grid_sample.plot()
city_b_proj.plot(ax=ax)


grid_sample.plot()
grid_proj = grid_sample.to_crs(epsg=4326)
ax = grid_proj.plot()
pop_fr_selection.plot(ax=ax)

grid_proj = grid.to_crs(epsg=4326)
grid.crs
pop_fr_selection_proj = pop_fr_selection.to_crs(grid.crs)


city_b_proj = city_b.to_crs(grid.crs)

inters = gpd.sjoin(grid, city_b_proj, how='left', op='within')
not_na = inters['index_right'].notna()
grid_fr = inters.loc[not_na]

grid_fr_clean = grid_fr[['id', 'geometry']]

inters_pop_grid = gpd.sjoin(grid_fr_clean, pop_fr_selection_proj, how='left')
not_na = inters_pop_grid['index_right'].notna()
grid_pop_fr = inters_pop_grid.loc[not_na]


grid_pop_fr.plot(column='Einwohner', legend=True)
grid_pop_fr.to_file('grid_pop_fr.shp')

# interactive ploting

grid_pop_fr = gpd.read_file('grid_pop_fr.shp')

grid_pop_fr_wgs = grid_pop_fr.to_crs(epsg=4326)


grid_pop_fr_wgs.plot(column='Einwohner', legend=True)

# plot with folium
coords_fr = get_coords_from_address('Freiburg, Germany')

data = DataFrame(grid_pop_fr_wgs)
geo = grid_pop_fr_wgs[['id', 'geometry']].to_json()

type(geo)

with open('test.geojson', 'w') as f:
    f.write(geo)

with open('geo_folium_test.json', 'w') as file:
    json.dump(geo, file)

data['Einwohner'].plot()
threshold_scale = threshold_scale = ps.esda.mapclassify.Quantiles(
    data['Einwohner'], k=6).bins.tolist()
threshold_scale = [1, 40, 80, ]
# Add the color for the chloropleth:
m = folium.Map(location=coords_fr)
m.choropleth(
    geo_data=geo,
    name='choropleth',
    data=data,
    columns=['id', 'Einwohner'],
    key_on='feature.properties.id',
    fill_color='YlGn',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Einwohner'
    threshold_scale=threshold_scale
)
# folium.LayerControl().add_to(m)
# 'feature.id'
# Save to html
m.save('Freiburg_einwohner.html')

# old people

threshold_scale = threshold_scale = ps.esda.mapclassify.Quantiles(data['5'], k=6).bins.tolist()

m = folium.Map(location=coords_fr)
m.choropleth(
    geo_data=geo,
    name='choropleth',
    data=data,
    columns=['id', '5'],
    key_on='feature.properties.id',
    fill_color='YlGn',
    fill_opacity=0.7,
    line_opacity=0.1,
    legend_name='Old people',
    # popup='Einwohner',
    threshold_scale=threshold_scale,
    highlight=True
)
# folium.LayerControl().add_to(m)
# 'feature.id'
# Save to html
m.save('Freiburg_old.html')
