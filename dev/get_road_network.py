import osmnx as ox
import geopandas as gpd

boundary_filepath = '/home/jesjehle/Documents/Mobility/data/Poster/upper_rhine_shape.shp'

boundary = gpd.read_file(boundary_filepath)

boundary_shape = boundary.geometry.iloc[0]
G = ox.graph_from_polygon(boundary.unary_union, network_type='drive')
ox.plot_graph(G)

