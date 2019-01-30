import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import numpy as np
import geoplot as gp

path = "../data/kfz-counting-stations-bw.csv"
cols = ['DZ_Name', 'Str_Kl', 'Str_Nr', 'Fernziel_Ri1', 'Fernziel_Ri2',
        'vT_MobisSo', 'DTV_Kfz_MobisSo_Q', 'DTV_Kfz_MobisSo_Ri1',
        'DTV_Kfz_MobisSo_Ri2', 'Koor_UTM32_E', 'Koor_UTM32_N']

# read only selected columns, use encoding for german umlaute, read coords as strings to avoid strange . in number afterwards
c_raw = pd.read_csv(path, usecols=cols, sep=';', encoding='ISO-8859-1',
                    dtype={'Koor_UTM32_N': str, 'Koor_UTM32_E': str})
# replace dots
c_raw['Koor_UTM32_E'] = c_raw['Koor_UTM32_E'].str.replace('.', '')
c_raw['Koor_UTM32_N'] = c_raw['Koor_UTM32_N'].str.replace('.', '')
# convert to ints
c_raw['Koor_UTM32_E'] = c_raw['Koor_UTM32_E'].astype('int64')
c_raw['Koor_UTM32_N'] = c_raw['Koor_UTM32_N'].astype('int64')
# convert to shaply coordinates
c_raw['coords'] = list(zip(c_raw['Koor_UTM32_E'], c_raw['Koor_UTM32_N']))
c_raw['coords'] = c_raw['coords'].apply(Point)

gdf = gpd.GeoDataFrame(c_raw, geometry='coords')

gdf.crs = {'init': 'epsg:32632'}
# gdf = gdf.to_crs(epsg='4326')

gdf = gdf.fillna(0)

gdf.plot(column='DTV_Kfz_MobisSo_Q', cmap='OrRd', legend=True)
gdf.plot(column='DTV_Kfz_MobisSo_Ri1', cmap='OrRd', legend=True)
gdf.plot(column='DTV_Kfz_MobisSo_Ri2', cmap='OrRd', legend=True)


path_kreise = '../data/vg250-ew_3112.utm32s.shape.ebenen/vg250-ew_ebenen/VG250_KRS.shp'
kreise = gpd.read_file(path_kreise)
kreise.plot()

kreise.head(1)
bw = kreise[kreise.RS.str.startswith('08')]
bw.crs = {'init': 'epsg:32632'}

back = bw.plot()
gdf.plot(ax=back, column='DTV_Kfz_MobisSo_Q', cmap='OrRd', legend=True)

kreise.columns

kreise[kreise.GF]
