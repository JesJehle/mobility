import folium
import geopandas as gpd
import osmnx as ox

# load freiburg shape and grid of germany
city_b = ox.gdf_from_place('Freiburg, Germany')
grid = gpd.read_file('../data/gitter/1_km_grid/de_1km.shp')
# reproject city_b to fit grid
city_b_proj = city_b.to_crs(grid.crs)


inters = gpd.sjoin(grid, city_b_proj, how='left', op='intersects')
not_na = inters['index_right'].notna()
grid_fr = inters.loc[not_na]

grid_fr.plot()

pop_grid = gpd.read_file("data/freiburg/grid_pop_fr.shp")
pop_grid.plot()
# pop_grid.to_crs(epsg=4326).to_file('data/freiburg/grid_pop_fr_wgs.shp')
grid_fr_wgs = grid_fr.to_crs(epsg=4326)
pop_grid_wgs = pop_grid.to_crs(epsg=4326)

pop_grid_wgs.plot()

pop_grid_wgs[pop_grid_wgs.Einwohner > 100].plot()


intersect = gpd.sjoin(grid_fr_wgs[['CELLCODE', 'geometry']], pop_grid_wgs, how='left')
not_na = intersect['index_right'].notna()
km_grid_fr_clean = intersect.loc[not_na]

km_grid_fr_test = km_grid_fr_clean.drop_duplicates('CELLCODE')
km_grid_fr_test.plot()
km_grid_fr_test.to_file("data/freiburg/grid_1km_fr.shp")
km_grid_geo = km_grid_fr_test[['CELLCODE', 'geometry']].to_json()
coords = city_b.centroid

coords = [coords.y[0], coords.x[0]]
# Add the color for the chloropleth:
m = folium.Map(location=coords)
m.choropleth(
    geo_data=km_grid_geo,
    name='choropleth',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='grid'
)
m.save('Freiburg_einwohner.html')


km_grid_fr_test[['CELLCODE', 'geometry']].to_file('freiburg_1_km_grid.shp')
