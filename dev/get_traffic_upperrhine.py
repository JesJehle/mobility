
import geopandas as gpd
from tools.traffic_data import TrafficData
import pandas as pd


def get_traffic_data():

    proj_city_filepath = '../../data/project_region/poi_shapes.shp'
    proj_boundary_filepath = '../../data/Poster/upper_rhine_shape.shp'

    proj_cities = gpd.read_file(proj_city_filepath)
    proj_boundary = gpd.read_file(proj_boundary_filepath)

    etrs89 = {'init': 'epsg:4258'}
    proj_cities.crs = etrs89
    proj_boundary.crs = etrs89

    proj_cities_wgs = proj_cities.to_crs(epsg=4326)
    proj_boundary_wgs = proj_boundary.to_crs(epsg=4326)
    # plot files
    ax = proj_boundary_wgs.plot()
    proj_cities_wgs.plot(ax=ax, color='black')


    city_selection = proj_cities[proj_cities['NAME_left'].isin(['Karlsruhe', 'Freiburg im Breisgau'])]


    x = city_selection.centroid.x
    y = city_selection.centroid.y

    gdf = gpd.GeoDataFrame()

    for x_, y_ in zip(x,y):
        traffic_frei = TrafficData(cityCoords=[y_, x_])
        traffic_frei.request_data(100000)
        traffic_frei.to_gdf()
        gdf = pd.concat([gdf, traffic_frei.traffic_gdf])


    gdf_in_boundary = gpd.sjoin(gdf, proj_boundary_wgs, op='within')


    df_unique = gdf_in_boundary.drop(columns='geometry').drop_duplicates()
    gdf_in_boundary_unique = gdf_in_boundary.loc[df_unique.index.drop_duplicates()]
    gdf_in_boundary_big = gdf_in_boundary_unique[gdf_in_boundary_unique['fc'] < 4]

    return gdf_in_boundary_big



traffic_data = get_traffic_data()

traffic_data.crs = {'init':'epsg:4326'}
#traffic_data = traffic_data.to_crs(epsg=3857)
#traffic_data = traffic_data.to_crs(epsg=4326)



# plotting
boundary = proj_boundary_wgs.plot( alpha=0.7)
traffic_data.plot(ax=boundary, column='jf', cmap='viridis', linewidth=0.8, legend=True)
proj_cities_wgs.plot(color='black',  alpha=0.7, ax=boundary)
# for idx, row in proj_cities_wgs.iterrows():
#     plt.annotate(s=row['NAME_left'], xy=[row['geometry'].centroid.x, row['geometry'].centroid.y], alpha=0.5)
boundary.axis('off')




import matplotlib.pyplot as plt

gdf_in_boundary_big['diff'].hist()
gdf_in_boundary_big['diff'] = gdf_in_boundary_big['ff'] - gdf_in_boundary_big['su']




boundary = proj_boundary_wgs.plot()
traffic_frei.traffic_gdf.plot(ax=boundary, column='diff')

gdf.drop_duplicates()
boundary = proj_boundary_wgs.plot()
gdf.plot(ax=boundary, column='jf')
proj_boundary_wgs.crs
traffic_frei.traffic_gdf.crs = proj_boundary_wgs.crs


gdf_in_boundary = gpd.sjoin(traffic_frei.traffic_gdf, proj_boundary_wgs, op='within')
boundary = proj_boundary_wgs.plot()
gdf_in_boundary.plot(ax=boundary, column='jf')

gdf_in_boundary.plot()
df_unique = gdf.drop(columns='geometry').drop_duplicates()

len(gdf.loc[df_unique.index])
len(gdf)

gdf.plot()
pd.DataFrame(gdf)







traffic_frei.traffic_gdf.to_file('../data/freiburg/traffic_big.geojson', driver='GeoJSON')




