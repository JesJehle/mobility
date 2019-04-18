import pandas as pd
import geopandas as gpd


nuts_path = '../../data/project_region/CRS_ORK_ETRS89_2019.shp'
main_cities_path = '../../data/project_region/ChefsLieux_Hauptorte.shp'

nuts = gpd.read_file(nuts_path)
main_cities = gpd.read_file(main_cities_path)


project_cities = gpd.sjoin(nuts, main_cities)

project_cities['AREA_KM2'].sum()

project_cities.plot()