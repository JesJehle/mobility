
import geocoder
import geopandas as gpd
import osmnx as ox
from shapely.geometry import Polygon
from numpy import ceil
from shapely.ops import nearest_points
from numpy import round
from math import sqrt
from functools import lru_cache
def get_coords_from_address(address):
    response = geocoder.osm(address)
    response_json = response.json
    lat = response_json['lat']
    lng = response_json['lng']

    return [lat, lng]

#@lru_cache(maxsize=10000)
def get_keys(json, key, keyList):
    if isinstance(json, dict):
        for keys in json:
            if keys == key:
                return(keyList.append(json[keys]))
            get_keys(json[keys], key, keyList)
    if isinstance(json, list):
        for elements in json:
            get_keys(elements, key, keyList)
    return keyList


def get_keys_from_json(json, key):
    key_list = []
    found_keys = get_keys(json, key, key_list)
    return found_keys


class SearchGrid():
    def __init__(self, city_name, width, height):
        self.city_name = city_name
        self.get_buildings()
        self.create_grid(width, height)
        self.crop_grid()
        #self._grid = self.create_grid(width, height)

    def get_buildings(self):
        """
        Arguments:
            city_name = string ('Loerrach, Baden-Wuerttemberg, Germany')
        Downloads the footprint of the city buildings form osm database.
        Returns a GeoDataFrame gdf.
        """
        # download city boundary
        city_boundary = ox.gdf_from_place(self.city_name)
        self.city_boundary = city_boundary
        # download buildings inside the boundary
        buildings = ox.buildings.create_buildings_gdf(city_boundary.geometry.iloc[0])
        self.buildings = buildings

    def crop_grid(self):
        intersections = gpd.sjoin(self.grid,
                                  self.buildings,
                                  how="left",
                                  op='intersects')
        grid_clean = intersections[['geometry', 'index_right']].dropna()
        grid_grouped = grid_clean.groupby(level=0)
        grid_unique = grid_grouped.first()
        self.grid = gpd.GeoDataFrame(grid_unique, geometry='geometry')
        self.grid.crs = {'init': 'epsg:4326'}

    def create_grid(self, width, height):
        """ creates a regular grid of polygons with given
        height and width in meters. Takes a gdf with crs wgs"""

        self.width = width
        self.height = height
        gdf_utm = self.buildings.to_crs({'init': 'epsg:25832'})
        xmin, ymin, xmax, ymax = gdf_utm.total_bounds
        rows = int(ceil((ymax - ymin) / height))
        cols = int(ceil((xmax - xmin) / width))
        x_left_origin = xmin
        x_right_origin = xmin + width
        y_top_origin = ymax
        y_bottomo_origin = ymax - height
        polygons = []
        for i in range(cols):
            y_top = y_top_origin
            y_bottom = y_bottomo_origin
            for j in range(rows):
                polygons.append(Polygon([
                    (x_left_origin, y_top),
                    (x_right_origin, y_top),
                    (x_right_origin, y_bottom),
                    (x_left_origin, y_bottom)]))
                y_top = y_top - height
                y_bottom = y_bottom - height
            x_left_origin = x_left_origin + width
            x_right_origin = x_right_origin + width

        grid = gpd.GeoDataFrame({'geometry': polygons})
        grid.crs = {'init': 'epsg:25832'}
        self.grid = grid.to_crs({'init': 'epsg:4326'})

    def get_nearest_point(self):
        """
        Find nearest point from grid centroid
        to next building centroid and add to grid gdf.
        :type grid: object
        """
        buildings_centroid = self.buildings.centroid.geometry.unary_union
        self.grid['centroids'] = self.grid.centroid
        p_list = []
        for index, row in self.grid.iterrows():
            nearest_p = nearest_points(row['centroids'], buildings_centroid)[1]
            p_list.append(nearest_p)
        self.nearest_p = gpd.GeoDataFrame({'geometry': p_list})
        self.nearest_p.crs = {'init': 'epsg:4326'}

    def get_radius(self):
        self.radius = round(sqrt(self.width ** 2 + self.height ** 2))
