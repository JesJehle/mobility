import geopandas as gpd

main_cities_path = '../../data/project_region/ChefsLieux_Hauptorte.shp'
file_path =  '../../data/project_region/CRS_ORK_ETRS89_2019.shp'

regions = gpd.read_file(file_path, encoding = 'ascii')
poi = gpd.read_file(main_cities_path, encoding = 'ascii')


regions_in_poi = gpd.sjoin(regions, poi)
regions_in_poi[['NAME_left', 'geometry'].plot()
regions_in_poi[['NAME_left', 'geometry']].to_file('../../data/project_region/poi_shapes.shp')

## 2. verison

import geopandas as gpd
import pandas as pd

proj_city_filepath = '../../data/project_region/poi_shapes.shp'
proj_regions_filepath = '../../data/project_region/CRS_ORK_ETRS89_2019.shp'

etrs89 = {'init':'epsg:4258'}



proj_shape = gpd.read_file(proj_shape_filepath)
proj_regions = gpd.read_file(proj_regions_filepath)
proj_shape.crs = etrs89
proj_regions.crs = etrs89
proj_regions.columns
proj_countrys = proj_regions.dissolve(by='NUTS0')
proj_countrys.crs = etrs89
proj_countrys.to_file('../../data/Poster/upper_rhine_shape_country.shp')

regions_dessolved_poly = proj_regions.unary_union

upper_rhine_df = pd.DataFrame(
    {'name': 'Upper Rhine',
     'geometry': regions_dessolved_poly},
index=[0])


upper_rhine_gdf = gpd.GeoDataFrame(upper_rhine_df, geometry='geometry')


upper_rhine_gdf.plot()



world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

world.plot()
world.columns
world['continent'].unique()
world_filtered = world[~world['continent'].isin(['Antarctica'])]

world_filtered.plot()
world_filtered.crs = {'init': 'epsg:4326'}
world_filtered.to_file('../../data/Poster/world.shp')
world_filtered.
upper_rhine_gdf.to_file('../../data/Poster/upper_rhine_shape.shp')

