import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
# path_gitter = "../data/gitter/DE_Grid_ETRS89-LAEA_100m.csv"
# gitter_100 = pd.read_csv(path_gitter, nrows=20, sep=';')

# nutz regions for project
path_nuts = "../data/nuts/NUTS_RG_20M_2016_3035_LEVL_2.shp/NUTS_RG_20M_2016_3035_LEVL_2.shp"
nuts = gpd.read_file(path_nuts)
nuts_de_fr = nuts[(nuts.CNTR_CODE == "DE") | (nuts.CNTR_CODE == "FR")]
regions = ['Stuttgart', 'Karlsruhe', 'Freiburg', 'Alsace']
region = nuts_de_fr[nuts_de_fr.NUTS_NAME.isin(regions)]
region.plot(column='NUTS_NAME', legend=True)

region.to_file('region.shp')

polygon = region.unary_union
# read spatial grid data


def add_geom(df):
    x = df.x_mp_100m
    y = df.y_mp_100m
    df['geometry'] = list(zip(y, x))
    df['geometry'] = df['geometry'].apply(Point)
    gdf = gpd.GeoDataFrame(df, geometry='geometry')
    gdf.crs = {'init': 'epsg:3035'}
    return gdf


# read pop data
path_pop_100 = "../data/population-bw/pop_cleaned_shp/pop_100_in_p_region.shp"
# to initialize property

path_demo = "../data/population-bw/demography_raw/Bevoelkerung100M.csv"

# test
# test_index = demo.Gitter_ID_100m.head(10)


# index.append(test_index)
# test_index = pd.concat([test_index, index])
# demo[demo.Gitter_ID_100m.isin(test_index)]

demo = pd.read_csv(path_demo, sep=';', encoding='ISO-8859-1',  nrows=0)
pop_100_raw = gpd.read_file(path_pop_100)
# all ids are unique

# add demographie data
# read in data in chunks
i = 1
for chunk in pd.read_csv(path_demo, sep=';', encoding='ISO-8859-1', chunksize=10000000):
    new = chunk[chunk.Gitter_ID_100m.isin(index)]
    print(new.size, 'new rnows in the ', i, 'iteration')
    demo = pd.concat([demo, new])
    i += 1

# create new columns
pop_100_raw['1'] = None
pop_100_raw['2'] = None
pop_100_raw['3'] = None
pop_100_raw['4'] = None
pop_100_raw['5'] = None
# filter for ALTER_KURZ
demo_sub = demo[demo.Merkmal == 'ALTER_KURZ']
selection = ['Einwohner_', 'Gitter_ID_', 'x_mp_100m',
             'Einwohner', 'y_mp_100m', 'geometry', '1', '2', '3', '4', '5']

for i in range(1, 6):
    index = demo_sub.Auspraegung_Code == i
    demo_sub_merk = demo_sub[index]
    pop_100_raw = pd.merge(pop_100_raw, demo_sub_merk, how='left',
                           left_on='Gitter_ID_', right_on='Gitter_ID_100m')
    pop_100_raw[str(i)] = pop_100_raw['Anzahl']
    pop_100_raw = pop_100_raw[selection]

pop_100_raw.plot(column="Einwohner_", legend=True, cmap='OrRd', scheme='quantiles')

pop_100_raw.to_file('../data/population-bw/pop_demo.shp')

pop_100_raw.Einwohner_.describe()

demo.to_csv('../data/population-bw/demography_raw/demography_bw.csv')

all = pd.read_csv(path_pop_100, sep=';')
x = all.x_mp_100m
y = all.y_mp_100m
all['geometry'] = list(zip(y, x))
all['geometry'] = all['geometry'].apply(Point)
gdf = gpd.GeoDataFrame(df, geometry='geometry')
gdf.crs = {'init': 'epsg:3035'}
all

all_geom = add_geom(all)


within_region.sum()


gdf.plot(column='Einwohner')
pop_100_raw


path_gitter = "../data/gitter/100m-grid/"
grid_100 = gpd.read_file(path_nuts)
