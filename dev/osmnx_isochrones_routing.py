import osmnx as ox, networkx as nx, geopandas as gpd, matplotlib.pyplot as plt
from shapely.geometry import Point, LineString, Polygon
from descartes import PolygonPatch

ox.config(log_console=True, use_cache=True)

# configure the place, network type, trip times, and travel speed
place = 'Freiburg, Germany'
network_type = 'walk'
trip_times = [5, 10, 15, 20, 25] #in minutes
travel_speed = 4.5 #walking speed in km/hour

# download the street network
G = ox.graph_from_place(place, network_type=network_type)


# find the centermost node and then project the graph to UTM
gdf_nodes = ox.graph_to_gdfs(G, edges=False)
x, y = gdf_nodes['geometry'].unary_union.centroid.xy
center_node = ox.get_nearest_node(G, (y[0], x[0]))
G = ox.project_graph(G)



gdf_test = ox.graph_to_gdfs(G, edges=False)


# add an edge attribute for time in minutes required to traverse each edge
meters_per_minute = travel_speed * 1000 / 60 #km per hour to m per minute
for u, v, k, data in G.edges(data=True, keys=True):
    data['time'] = data['length'] / meters_per_minute


iso_colors = ox.get_colors(n=len(trip_times), cmap='Reds', start=0.3, return_hex=True)


# color the nodes according to isochrone then plot the street network
node_colors = {}
for trip_time, color in zip(sorted(trip_times, reverse=True), iso_colors):
    subgraph = nx.ego_graph(G, center_node, radius=trip_time, distance='time')
    for node in subgraph.nodes():
        node_colors[node] = color
nc = [node_colors[node] if node in node_colors else 'none' for node in G.nodes()]
ns = [20 if node in node_colors else 0 for node in G.nodes()]
fig, ax = ox.plot_graph(G, fig_height=8, node_color=nc, node_size=ns, node_alpha=0.8, node_zorder=2)


# make the isochrone polygons
isochrone_polys = []
for trip_time in sorted(trip_times, reverse=True):
    subgraph = nx.ego_graph(G, center_node, radius=trip_time, distance='time')
    node_points = [Point((data['x'], data['y'])) for node, data in subgraph.nodes(data=True)]
    bounding_poly = gpd.GeoSeries(node_points).unary_union.convex_hull
    isochrone_polys.append(bounding_poly)


# plot the network then add isochrones as colored descartes polygon patches
fig, ax = ox.plot_graph(G, fig_height=8, show=False, close=False, edge_color='k', edge_alpha=0.2, node_color='none')
for polygon, fc in zip(isochrone_polys, iso_colors):
    patch = PolygonPatch(polygon, fc=fc, ec='none', alpha=0.6, zorder=-1)
    ax.add_patch(patch)
plt.show()


def make_iso_polys(G, edge_buff=25, node_buff=50, infill=False):
    isochrone_polys = []
    for trip_time in sorted(trip_times, reverse=True):
        subgraph = nx.ego_graph(G, center_node, radius=trip_time, distance='time')

        node_points = [Point((data['x'], data['y'])) for node, data in subgraph.nodes(data=True)]
        nodes_gdf = gpd.GeoDataFrame({'id': subgraph.nodes()}, geometry=node_points)
        nodes_gdf = nodes_gdf.set_index('id')

        edge_lines = []
        for n_fr, n_to in subgraph.edges():
            f = nodes_gdf.loc[n_fr].geometry
            t = nodes_gdf.loc[n_to].geometry
            edge_lines.append(LineString([f, t]))

        n = nodes_gdf.buffer(node_buff).geometry
        e = gpd.GeoSeries(edge_lines).buffer(edge_buff).geometry
        all_gs = list(n) + list(e)
        new_iso = gpd.GeoSeries(all_gs).unary_union

        # try to fill in surrounded areas so shapes will appear solid and blocks without white space inside them
        if infill:
            new_iso = Polygon(new_iso.exterior)
        isochrone_polys.append(new_iso)
    return isochrone_polys


isochrone_polys = make_iso_polys(G, edge_buff=25, node_buff=0, infill=True)
fig, ax = ox.plot_graph(G, fig_height=8, show=False, close=False, edge_color='k', edge_alpha=0.2, node_color='none')
for polygon, fc in zip(isochrone_polys, iso_colors):
    patch = PolygonPatch(polygon, fc=fc, ec='none', alpha=0.6, zorder=-1)
    ax.add_patch(patch)
plt.show()


# compare with isochrone

# isochrone 10 min

from tools.travel_time_pt import get_iso_lines

import pandas as pd
import geopandas as gpd
import math

from shapely.geometry import Point, Polygon

center_point = gdf_nodes[gdf_nodes['osmid'] == center_node]

iso_df = get_iso_lines(center_point, point_id_column='osmid', times=[10])



df = pd.DataFrame(columns=['iso_times', 'geometry'])
trip_times.reverse()
df['iso_times'] = trip_times
df['geometry'] = isochrone_polys

osm_gdf = gpd.GeoDataFrame(df, geometry='geometry')

avg_longitude = center_point['geometry'].x
# calculate the UTM zone from this avg longitude and define the UTM
# CRS to project
utm_zone = int(math.floor((avg_longitude + 180) / 6.) + 1)
utm_crs = {'datum': 'WGS84',
           'ellps': 'WGS84',
           'proj': 'utm',
           'zone': utm_zone,
           'units': 'm'}

# project the GeoDataFrame to the UTM CRS
osm_gdf.crs = utm_crs
osm_gdf = osm_gdf.to_crs(4326)



ido_df_rev = iso_df.copy()
coords_revered = [[t[1], t[0]] for t in list(iso_df.iloc[0].geometry.exterior.coords)]

ido_df_rev['geometry'] = Polygon(coords_revered)




fig, ax = ox.plot_graph(G, fig_height=8, show=False, close=False, edge_color='k', edge_alpha=0.2, node_color='none')
osm_gdf[osm_gdf['iso_times'] == 10].plot(ax=ax)
ido_df_rev.plot( color='red')
