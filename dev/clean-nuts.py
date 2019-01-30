import pandas as pd
import geopandas as gpd


nuts_path = '../data/nuts/NUTS_RG_20M_2016_3035_LEVL_3.shp//'
region_path = '../data/project_region/region.shp'
kreise_path = '../data/vg250-ew_3112.utm32s.shape.ebenen/vg250-ew_ebenen/VG250_KRS.shp'

nuts = gpd.read_file(nuts_path)
region = gpd.read_file(region_path)
kreise = gpd.read_file(kreise_path)

kreise.crs

kreise = kreise.to_crs({'init': 'epsg:3035'})
region = region.to_crs({'init': 'epsg:3035'})

kreise_region = gpd.sjoin(kreise, region, how='left')
kreise_region = kreise_region.dropna()

kreise_region[kreise_region.GEN == 'Lörrach'].plot()

cities = kreise_region[kreise_region.BEZ != 'Landkreis']

cities.plot()


nuts_region = gpd.sjoin(nuts, region, how='left')
nuts_region.size
nuts_region = nuts_region.dropna()
nuts_region.size

nuts_region.head()

nuts_region['area'] = nuts_region.area

nuts_region.sort_values('area')

nuts_region.plot(column='area', legend=True)


dfg
