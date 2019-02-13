

def test_format_time_for_request():
    from tools.travel_time_pt import format_time_for_request
    import datetime
    time_input = datetime.datetime(2019, 2, 2, 10, 0)
    time_output = '2019-02-02T10:00:00'
    assert format_time_for_request(time_input) == time_output


def test_request_route():
    import datetime
    from tools.travel_time_pt import PubTransRouter
    from tools.api_keys import here_app_code, here_app_id

    date_time = datetime.datetime(2019, 2, 2, 10, 0)
    origin = [48.022917, 7.85832]
    destination = [48.007457, 7.855260]
    router = PubTransRouter(here_app_id, here_app_code)

    response = router.request_route(date_time, origin, destination, False)
    assert isinstance(response['Res'], dict)



def test_extract_travel_times():
    import json
    from pandas import DataFrame
    from tools.travel_time_pt import extract_travel_times
    with open("data/test_pt_route_simple.json", 'r') as f:
        response = json.load(f)

    stations_df = extract_travel_times(response)

    assert isinstance(stations_df, DataFrame)


def test_find_reached_stations():
    from tools.travel_time_pt import find_reached_stations
    from geopandas import read_file
    import pandas as pd

    target_stations = read_file('data/test_sample_target_stations.shp')
    target_stations.crs = {'init': 'epsg:4326'}
    stations_df = pd.read_csv('data/test_station_df.csv')
    found_stations = find_reached_stations(stations_df, target_stations, 50)
    assert isinstance(found_stations, list)



def test_create_travel_time_df():

    import geopandas as gpd
    from tools.travel_time_pt import create_travel_time_df
    from pandas import DataFrame
    import datetime

    target_stations = gpd.read_file('data/test_sample_target_stations.shp')
    target_stations.crs = {'init': 'epsg:4326'}
    target_stations = target_stations[['station_id', 'geometry']]
    # origin = target_stations.sample(1).geometry
    date_time = datetime.datetime(2019, 2, 2, 10, 0)
    travel_time_test = create_travel_time_df(target_stations.sample(2), date_time)

    assert isinstance(travel_time_test, DataFrame)



def test_get_accessibility_gdf():
    import pandas as pd
    from geopandas import GeoDataFrame
    from tools.travel_time_pt import get_accessibility_gdf
    stations_df = pd.read_csv('pt_travel_time_test_result.csv')
    test = get_accessibility_gdf(stations_df)
    assert isinstance(test,GeoDataFrame )




from tools.travel_time_pt import get_iso_lines, clip_by_attribute
import pandas as pd
import matplotlib as plt
import geopandas as gpd

plt.interactive(True)
pd.set_option('display.max_columns', 500)


target_stations = gpd.read_file('../data/freiburg/pt_accessibility.shp')
target_stations.crs = {'init': 'epsg:4326'}

target_stations_iso = get_iso_lines(target_stations)
target_stations_iso.to_file('../data/freiburg/iso_all.shp')

iso_clipped = clip_by_attribute(target_stations_iso, 'iso_time')

sum(iso_clipped.geometry.is_empty)


iso_all_clean = iso_clipped.loc[~iso_clipped.geometry.is_empty]
iso_clipped.loc[~iso_clipped.geometry.is_empty].plot(column='iso_time', legend=True)


iso_all_clean

target_stations_iso.to_file('../data/freiburg/iso_all.shp')
broken_index = iso_all_clean.index.isin(broken_geometries)
iso_all_c = iso_all_clean.iloc[~broken_index]

iso_all_c['iso_distance'] = iso_all_c['iso_distance'].astype(int)
iso_all_c['iso_time'] = iso_all_c['iso_time'].astype(int)

iso_all_c.dtypes

iso_all_c.to_file('../data/freiburg/iso_all_clean.shp')

iso_all_clean[]

iso_all_clean.crs
broken_geometries = []


for i, row in iso_all_clean.iterrows():
    try:
        gpd.GeoSeries(row.geometry).is_simple
    except:
        broken_geometries.append(i)


iso_clipped.iloc[3:4].plot()

gdf = target_stations_iso
from shapely.geometry import Polygon
import pandas as pd
import matplotlib as plt
import geopandas as gpd






gdf_new.plot(column='iso_time')
iso_clipped[index:index+1].plot()

gdf_union = gpd.GeoDataFrame(gpd.GeoSeries(new_geom))
gdf_union_renamed = gdf_union.rename(columns={0: 'geometry'}).set_geometry('geometry')
gdf_union_renamed.plot()

#
#
#
# for i in ['1', '5', '10']:
#     target_stations_iso[['station', 'iso' + i +'travel_time', 'iso' + i +'geometry']].set_geometry('iso' + i +'geometry').to_file('../data/freiburg/iso_' + i +'_freiburg.shp')
#
#
# iso_1 = gpd.read_file('../data/freiburg/iso_1_freiburg.shp')
# iso_1.crs = {'init': 'epsg:4326'}
# iso_5 = gpd.read_file('../data/freiburg/iso_5_freiburg.shp')
# iso_1.crs = {'init': 'epsg:4326'}
# iso_10 = gpd.read_file('../data/freiburg/iso_10_freiburg.shp')
# iso_10.crs = {'init': 'epsg:4326'}
#
#
# pd.concat([iso_1,iso_5, iso_10])
#
#
# def create_union_gdf(gdf):
#     gdf_union = gpd.GeoDataFrame(gpd.GeoSeries(gdf.unary_union))
#     gdf_union_renamed = gdf_union.rename(columns={0:'geometry'}).set_geometry('geometry')
#     return gdf_union_renamed
#
#
#
#
#
# iso_1_5_diff = gpd.overlay(iso_5, create_union_gdf(iso_1), how='difference')
# iso_5_10_diff = gpd.overlay(iso_10, create_union_gdf(iso_5), how='difference')
#
# iso_5_10_diff.to_file('../data/freiburg/iso_diff.shp')
#
# continents = world.dissolve(by='continent', aggfunc='sum')
#
#
# iso_1_5.plot()
# iso_1_5.to_file('../data/freiburg/iso_diff.shp')
# world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
#
# world.plot()
# world = world[['continent', 'geometry', 'pop_est']]
# continents = world.dissolve(by='continent', aggfunc='sum')
# continents.plot()
#


# example

from shapely.geometry import Polygon
import pandas as pd
import matplotlib as plt
import geopandas as gpd

plt.interactive(True)
pd.set_option('display.max_columns', 500)


polys1 = gpd.GeoSeries([Polygon([(0,0), (2,0), (2,2), (0,2)]), Polygon([(1,1), (3,1), (3,3), (1,3)]), Polygon([(0.5, 0.5), (2.5,0.5), (2.5,2.5), (0.5,2.5)])])
# polys2 = gpd.GeoSeries([Polygon([(1,1), (3,1), (3,3), (1,3)])])

df1 = gpd.GeoDataFrame({'geometry': polys1, 'value':[1, 3, 5], 'in': [1,2,3]})
# df2 = gpd.GeoDataFrame({'geometry': polys2, 'df2':[1]})

df1.plot(column='value', legend=True)

test_1 = df1.iloc[0:1]
test_1.plot(column='value', legend=True)

test_2 = df1.iloc[2:3]
test_2.plot(column='value', legend=True)

test_2.intersects(test_1.geometry)


df_2.iloc[0:1].plot(column='value', legend=True)
df1.iloc[0:1].plot(column='value', legend=True)


df_2 = clip_by_attribute(df1, 'value')



def clip_by_attribute(gdf, attr):
    gdf_new = gdf.copy()

    for index, row in gdf_new.iterrows():
        # diff_index = df1.index.difference(index)
        index_in = gdf_new.index.isin([index])
        diff_gdf = gdf_new.iloc[~index_in]

        is_intersection = diff_gdf.intersects(row.geometry)

        gdf_intersection = diff_gdf.loc[is_intersection]

        highest_intersection = gdf_intersection.sort_values(attr, ascending=False).head(1).iloc[0]

        if highest_intersection[attr] > row[attr]:
            print(highest_intersection[attr], 'is bigger then', row[attr])
            new_geom = row.geometry.difference(highest_intersection.geometry)
            gdf_new.at[index, 'geometry'] = new_geom

    return gdf_new






    for i, r in gdf_intersection.iterrows():
        if r['value'] > row['value']:
            print(r['value'], 'is bigger then', row['value'])
            new_geom = row.geometry.difference(r.geometry)
            inx = r['in']
            df1.at[inx, 'in']
            gdf_union = gpd.GeoDataFrame(gpd.GeoSeries(new_geom))
            gdf_union_renamed = gdf_union.rename(columns={0: 'geometry'}).set_geometry('geometry')
            gdf_union_renamed.plot()


            df1[df1['in'] == r['in']]['geometry'] = new_geom

    #print(geom_diff)

df1.iloc[0:1].plot(column='value', legend=True)


r_gdf = gpd.GeoDataFrame(r.geometry.difference(row.geometry))
type(r_gdf)
r_gdf.plot()
gdf_union_renamed = r_gdf.rename(columns={0: 'geometry'}).set_geometry('geometry')
gdf_union_renamed.plot()
gdf_union = gpd.GeoDataFrame(gpd.GeoSeries(r.geometry.difference(row.geometry)))
gdf_union_renamed = gdf_union.rename(columns={0: 'geometry'}).set_geometry('geometry')
gdf_union_renamed.plot()

    #row.geometry.intersects(geom_1)

row = df1.iloc[0]



rest = df1.loc[diff_index]

geometry
geom_1 = df1.iloc[1].geometry

geom_0.intersects(geom_1)

geom_diff = geom_1.difference(geom_0)

gdf_union = gpd.GeoDataFrame(gpd.GeoSeries(geom_diff))
gdf_union_renamed = gdf_union.rename(columns={0:'geometry'}).set_geometry('geometry')
gdf_union_renamed.plot()

















# travel_time_counts = travel_time_test.groupby('station').count()
# station_index = travel_time_counts[travel_time_counts['travel_time'] > 150].index
#
# mean_station = travel_time_test.groupby('station').mean()
# connectivity
# import pandas as pd
# from geopandas import GeoDataFrame
# from shapely.geometry import Point
# from tools.travel_time_pt import get_accessibility_gdf
# stations_df = pd.read_csv('pt_travel_time_test_result.csv')
#
# mean_connectivity = stations_df[['depature', 'travel_time']].groupby('depature').mean()
#
# mean_coords_id = stations_df.groupby('station').mean()
#
# pd.merge(mean_connectivity, mean_coords_id[['x', 'y']], on='station')
# mean_connectivity.index.names = ['station']
#
# .join(, on='station')
# mean_connectivity_gpd = mean_connectivity[['travel_time', 'x', 'y']]
# geometry = [Point(xy) for xy in zip(mean_connectivity_gpd.x, mean_connectivity_gpd.y)]
# mean_connectivity_gpd['geometry'] = geometry
# mean_connectivity_gpd = GeoDataFrame(mean_connectivity_gpd, geometry='geometry')
# mean_connectivity_gpd.crs = {'init': 'epsg:4326'}
# assert isinstance(test,GeoDataFrame )
# mean_connectivity_gpd.to_file('data/connectivity_sample.shp')
#
