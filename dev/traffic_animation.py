


from natsort import natsorted

import numpy as np
import geopandas as gpd
import pandas as pd
from matplotlib import pyplot as plt
import cartopy.crs as ccrs
import cartopy.io.img_tiles as cimgt
import contextily as ctx
from shapely.geometry import Point
import os
import re
#
#
# def add_basemap(ax, zoom, url='http://tile.stamen.com/terrain/tileZ/tileX/tileY.png'):
#     xmin, xmax, ymin, ymax = ax.axis()
#     basemap, extent = ctx.bounds2img(xmin, ymin, xmax, ymax, zoom=zoom, url=url)
#     ax.imshow(basemap, extent=extent, interpolation='bilinear')
#     # restore original x/y limits
#     ax.axis((xmin, xmax, ymin, ymax))
#     ax.set_axis_off()
#     # ax.set_title(title)
#
#
# def make_figure(traffic_filepath, figure_path, time):
#
#     traffic = gpd.read_file(traffic_filepath)
#     # convert
#     traffic_sel = traffic[(traffic['fc'] < 5) & (traffic['jf'] > 4) & (traffic['cn'] > 0.5)]
#
#     traffic_proj_sel = traffic_sel.to_crs(epsg=3857)
#
#     # get alpha for jf
#     traffic_len = len(traffic_proj_sel)
#     traffic_proj_sel['alpha'] = (traffic_proj_sel['jf'] / 10) - 0.4
#     traffic_proj_sel['alpha'] = traffic_proj_sel['alpha'].round(1)
#     alphas = traffic_proj_sel['alpha'].tolist()
#     rgba_colors = np.zeros((traffic_len, 4))
#     rgba_colors[:, 0] = 1.0
#     # the fourth column needs to be your alphas
#     rgba_colors[:, 3] = alphas
#
#     traffic_length_df = pd.read_csv('../../data/Poster/traffic_figures/traffic_length2.csv')
#
#
#     boundary_filepath = '/home/jesjehle/Documents/Mobility/data/Poster/upper_rhine_shape.shp'
#     boundary = gpd.read_file(boundary_filepath)
#     boundary.crs = {'init': 'epsg:4258'}
#     boundary_wgs = boundary.to_crs(epsg=4326)
#     boundary_proj = boundary.to_crs(epsg=3857)
#
#     fig = plt.figure()
#
#     # Divide the figure into a 1x2 grid, and give me the first section
#     ax1 = fig.add_subplot(121)
#     ax2 = fig.add_subplot(224)
#     ax3 = fig.add_subplot(222)
#     from matplotlib import rcParams
#
#     rcParams['font.family'] = 'sans-serif'
#     rcParams['font.sans-serif'] = ['Tahoma']
#
#
#     traffic_proj_sel.plot(ax=ax1, figsize=(19.2, 10.8), color=rgba_colors, column='jf', linewidth=2, legend=True)
#     boundary_proj.plot(ax=ax1, facecolor="none", edgecolor='black', lw=0.7, alpha=0.4)
#     add_basemap(ax1, zoom=9, url=ctx.sources.OSM_C)
#     traffic_length_df = traffic_length_df.set_index(pd.date_range('2019-03-15', periods=95, freq='15min'))
#
#     # plt.style.use('seaborn-darkgrid')
#     traffic_length_df['traffic_length'].plot(ax=ax2, style='-', color='black', alpha = 0.7 )
#
#     # traffic_length_df['traffic_length'].plot(, style='-', color='black')
#
#     traffic_length_df[traffic_length_df['time'] == time]['traffic_length'].plot(ax=ax2, style='ro', alpha = 0.7)
#     # ax2.set_xticks(traffic_length_df.index)
#     # ax2.set_xticklabels(traffic_length_df.time, rotation=60)
#     ax2.set_title('Roads with high traffic volume [km]')
#     ax3.axis('off')
#     ax3.text(0.5, 0.5, "Upper Rhine Traffic\n at: " + time, size=16, ha="center")
#     plt.savefig(figure_path, bbox_inches='tight', facecolor='w', dpi=200)
#



def add_basemap(ax, zoom, url='http://tile.stamen.com/terrain/tileZ/tileX/tileY.png'):
    xmin, xmax, ymin, ymax = ax.axis()
    basemap, extent = ctx.bounds2img(xmin, ymin, xmax, ymax, zoom=zoom, url=url)
    ax.imshow(basemap, extent=extent, interpolation='bilinear')
    # restore original x/y limits
    ax.axis((xmin, xmax, ymin, ymax))

    ax.set_axis_off()
    # ax.set_title(title)


def make_figure(traffic_filepath, figure_path, time):

    traffic = gpd.read_file(traffic_filepath)
    # converttraffic_filepath
    traffic_sel = traffic[(traffic['fc'] < 5) & (traffic['jf'] > 4) & (traffic['cn'] > 0.5)]

    traffic_proj_sel = traffic_sel.to_crs(epsg=3857)

    traffic_backround_proj = gpd.read_file('/home/jesjehle/Documents/Mobility/data/Poster/roads_upperrhine.geojson')
    traffic_backround_proj = traffic_backround_proj[(traffic_backround_proj['fc'] < 4)]

    traffic_length_df = pd.read_csv('../../data/Poster/traffic_figures/traffic_length2.csv')
    boundary_filepath = '/home/jesjehle/Documents/Mobility/data/Poster/upper_rhine_shape.shp'
    boundary = gpd.read_file(boundary_filepath)

    boundary.crs = {'init': 'epsg:4258'}
    # boundary_wgs = boundary.to_crs(epsg=4326)
    boundary_proj = boundary.to_crs(epsg=3857)


    # extract points ##############

    traffic_proj_sel['points'] = list(zip(traffic_proj_sel['geometry'].bounds['minx'], traffic_proj_sel['geometry'].bounds['miny']))

    traffic_proj_sel['points'] = traffic_proj_sel['points'].apply(Point)

    ###################

    # traffic_backround = traffic[(traffic['fc'] < 5)]
    # traffic_backround_proj = traffic_backround.to_crs(epsg=3857)


    # traffic_backround_proj.to_file('/home/jesjehle/Documents/Mobility/data/Poster/roads_upperrhine.geojson', driver='GeoJSON')
    # traffic_backround_proj.plot()

    # get alpha for jf
    traffic_len = len(traffic_proj_sel)
    traffic_proj_sel['alpha'] = (traffic_proj_sel['jf'] / 10) - 0.4
    traffic_proj_sel['alpha'] = traffic_proj_sel['alpha'].round(1)
    alphas = traffic_proj_sel['alpha'].tolist()
    rgba_colors = np.zeros((traffic_len, 4))
    rgba_colors[:, 0] = 1.0
    # the fourth column needs to be your alphas
    rgba_colors[:, 3] = alphas





    fig = plt.figure()
    plt.style.use('seaborn-darkgrid')

    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(224)
    ax3 = fig.add_subplot(222)
    #plt.rcParams["axes.edgecolor"] = "black"
    #plt.rcParams["axes.linewidth"] = 1
    import geoplot
    # from matplotlib import rcParams
    #
    # rcParams['font.family'] = 'sans-serif'
    # rcParams['font.sans-serif'] = ['Tahoma']
    traffic_backround_proj.plot(ax=ax1, color='black', linewidth=0.1, alpha = 0.3)
    traffic_proj_sel.set_geometry('points').plot(ax=ax1, column = 'jf',color=rgba_colors,  markersize=traffic_proj_sel['jf'] * 3)

    # traffic_proj_sel.plot(ax=ax1, color=rgba_colors, column='jf', linewidth=3)
    boundary_proj.plot(ax=ax1, facecolor="none", edgecolor='black', lw=1, alpha=0.6)
    add_basemap(ax1, zoom=8, url=ctx.sources.OSM_A)

    # ax1.set_title('Roads with high traffic volume', size = 12, color = 'w')
    # ax1.spines['bottom'].set_color('0.5')
    # ax1.spines['top'].set_color('0.5')
    # ax1.spines['right'].set_color('0.5')
    # ax1.spines['left'].set_color('0.5')

    traffic_length_df = traffic_length_df.set_index(pd.date_range('2019-03-15', periods=95, freq='15min'))
    # plt.style.use('seaborn-darkgrid')
    traffic_length_df['traffic_length'].plot(ax=ax2, style='-', color='black', alpha = 0.7, figsize=(10, 7))
    # ax2.tick_params(axis='x', rotation=45)


    # ax2.set_xticklabels(traffic_length_df.index, rotation=20, horizontalalignment='right')
    # ax2.tick_params(labelsize=6)
    # traffic_length_df['traffic_length'].plot(, style='-', color='black')

    traffic_length_df[traffic_length_df['time'] == time]['traffic_length'].plot(ax=ax2, style='ro', alpha = 0.7)
    traffic_length_df[traffic_length_df['time'] == time]['traffic_length'].plot(ax=ax2, style='.', alpha = 0.7)

    # ax2.set_xticks(traffic_length_df.index)
    #ax2.set_xticklabels(traffic_length_df.index, )
    ax2.set_title('Congested Roads', fontsize=12)
    ax2.set_ylabel('Total lengths [km]', size = 12)
    #ax2.tick_params(axis='x', colors='w')
    #ax2.tick_params(axis='y', colors='w')

    ax3.axis('off')

    ax3.text(0.5, 0.6, "Upper Rhine Traffic Flow", size=30, ha="center", color = 'w')
    ax3.text(0.5, 0.45, "Friday, March 15th", size=20, ha="center", color = 'w')

    ax3.text(0.5, 0.1, time, size=45, ha="center", fontname="monospace", color = 'w')

    plt.savefig(figure_path, bbox_inches='tight', facecolor='lightgrey', dpi=200)
#

def main():

    root_dir = '../../data/Poster/traffic_data/'
    figure_path = '../../data/Poster/traffic_figure2/'


    files = natsorted(os.listdir('../../data/Poster/traffic_data/'))

    # test #####
    # file_sel = files[27:35]

    #
    # time = re.search('\d{2}:\d{2}', file_sel).group(0)
    #
    # traffic_filepath = root_dir + file_sel
    # figure_path = figure_path + time
    # make_figure(traffic_filepath, figure_path, time=time)

    ####
    counter = 1
    for file in files:

        time = re.search('\d{2}:\d{2}', file).group(0)
        if counter < 10:
            name = 'image-' + '0' + str(counter)
        else:
            name = 'image-' + str(counter)

        traffic_filepath = root_dir + file
        figure_path_ = figure_path + name
        make_figure(traffic_filepath, figure_path_, time=time)
        counter = counter + 1



if __name__ == '__main__':
    main()




# # test
#
#
# from natsort import natsorted
#
# import numpy as np
# import geopandas as gpd
# import pandas as pd
# from matplotlib import pyplot as plt
# import cartopy.crs as ccrs
# import cartopy.io.img_tiles as cimgt
# import contextily as ctx
# import os
# import re
#
#
# boundary_filepath = '/home/jesjehle/Documents/Mobility/data/Poster/upper_rhine_shape.shp'
# boundary = gpd.read_file(boundary_filepath)
# boundary.crs = {'init': 'epsg:4258'}
# boundary_wgs = boundary.to_crs(epsg=4326)
# boundary_proj = boundary.to_crs(epsg=3857)
#
#
#
# root_dir = '../../data/Poster/traffic_data/'
# figure_path = '../../data/Poster/traffic_figures/'
#
# files = os.listdir('../../data/Poster/traffic_data/')
# file = files[0]
# time = re.search('\d{2}:\d{2}', file).group(0)
# title = time
#
# traffic_filepath = root_dir + file
#
# traffic = gpd.read_file(traffic_filepath)
#
# # convert
# traffic_sel = traffic[(traffic['fc'] < 5) & (traffic['jf'] > 4) & (traffic['cn'] > 0.5)]
#
# traffic_proj_sel = traffic_sel.to_crs(epsg=3857)
#
# # get alpha for jf
# traffic_len = len(traffic_proj_sel)
# traffic_proj_sel['alpha'] = (traffic_proj_sel['jf'] / 10) - 0.4
# traffic_proj_sel['alpha'] = traffic_proj_sel['alpha'].round(1)
# alphas = traffic_proj_sel['alpha'].tolist()
# rgba_colors = np.zeros((traffic_len, 4))
# rgba_colors[:, 0] = 1.0
# # the fourth column needs to be your alphas
# rgba_colors[:, 3] = alphas
#
#
# traffic_length_df = pd.read_csv('../../data/Poster/traffic_figures/traffic_length.csv')
#
# fig = plt.figure()
#
# # Divide the figure into a 1x2 grid, and give me the first section
# ax1 = fig.add_subplot(121)
# ax2 = fig.add_subplot(224)
# ax3 = fig.add_subplot(222)
#
#
# traffic_proj_sel.plot(ax=ax1, figsize=(19.2, 10.8), color=rgba_colors, column='jf', linewidth=2, legend=True)
# boundary_proj.plot(ax=ax1, facecolor="none", edgecolor='black', lw=0.7, alpha=0.4)
# add_basemap(ax1, zoom=9, url=ctx.sources.OSM_C, title='Congestion Hotspots')
# traffic_length_df['traffic_length'].plot(ax=ax2, style='-', color='black')
# traffic_length_df[traffic_length_df['time'] == time]['traffic_length'].plot(ax=ax2, style='ro')
# ax2.set_xticks(traffic_length_df.index)
# ax2.set_xticklabels(traffic_length_df.time, rotation=60)
# ax2.set_title('Roads with traffic jams [km]')
# ax3.axis('off')
# ax3.text(0.5,0.5, "Upper Rhine Traffic\n at: " + time, size=16, ha="center")
# plt.savefig(figure_path + time, bbox_inches='tight', facecolor='w', dpi = 200)
#
#
#
#
#
#
# fig = plt.figure()
#
# # Divide the figure into a 1x2 grid, and give me the first section
# ax1 = fig.add_subplot(2, 2, (1,2))
#
# # Divide the figure into a 1x2 grid, and give me the second section
# ax2 = fig.add_subplot(224)
#
# df.groupby('country').plot(x='year', y='unemployment', ax=ax1, legend=False)
# df.groupby('country')['unemployment'].mean().sort_values().plot(kind='barh', ax=ax2)
#


#
# traffic_filepath = '../../data/Poster/traffic_data/4_traffic_08-03_10:55.geojson'
#
# make_figure(traffic_filepath, figure_path)


#
# # plotting
# boundary = proj_boundary_wgs.plot( alpha=0.7)
# traffic_data.plot(ax=boundary, column='jf', cmap='viridis', linewidth=0.8, legend=True)
# proj_cities_wgs.plot(color='black',  alpha=0.7, ax=boundary)
# # for idx, row in proj_cities_wgs.iterrows():
# #     plt.annotate(s=row['NAME_left'], xy=[row['geometry'].centroid.x, row['geometry'].centroid.y], alpha=0.5)
# boundary.axis('off')
#
#
#
#
# import matplotlib.pyplot as plt
#
# gdf_in_boundary_big['diff'].hist()
# gdf_in_boundary_big['diff'] = gdf_in_boundary_big['ff'] - gdf_in_boundary_big['su']
#
#
#
#
# boundary = proj_boundary_wgs.plot()
# traffic_frei.traffic_gdf.plot(ax=boundary, column='diff')
#
# gdf.drop_duplicates()
# boundary = proj_boundary_wgs.plot()
# gdf.plot(ax=boundary, column='jf')
# proj_boundary_wgs.crs
# traffic_frei.traffic_gdf.crs = proj_boundary_wgs.crs
#
#
# gdf_in_boundary = gpd.sjoin(traffic_frei.traffic_gdf, proj_boundary_wgs, op='within')
# boundary = proj_boundary_wgs.plot()
# gdf_in_boundary.plot(ax=boundary, column='jf')
#
# gdf_in_boundary.plot()
# df_unique = gdf.drop(columns='geometry').drop_duplicates()
#
# len(gdf.loc[df_unique.index])
# len(gdf)
#
#
#
# # inspect
# gdf_in_boundary_big = gdf_in_boundary_unique[gdf_in_boundary_unique['fc'] < 4]
#
# boundary = proj_boundary_wgs.plot()
# gdf_in_boundary_unique[gdf_in_boundary_unique['jf'] > 2].plot(ax=boundary, column='jf', cmap='Reds')
#
# gdf_in_boundary_unique['jf'].hist()
#
#
#
#
# traffic_data = get_traffic_data()
#
# traffic_data.crs = {'init':'epsg:4326'}
#
# #traffic_data = traffic_data.to_crs(epsg=3857)
# #traffic_data = traffic_data.to_crs(epsg=4326)
#
#
#
# gdf.plot()
# pd.DataFrame(gdf)
#
#
#




# traffic_frei.traffic_gdf.to_file('../data/freiburg/traffic_big.geojson', driver='GeoJSON')

