
import requests
import re
from pandas import DataFrame
from geopandas import GeoDataFrame
from shapely.geometry import Point, LineString, MultiLineString
import osmnx as ox
from utiles import get_coords_from_address, get_keys_from_json
from api_keys import here_app_id, here_app_code


class TrafficData():
    """Includes methods to download, clean and converts and exports traffic data"""

    def __init__(self, cityName):
        self.city_name = cityName
        self.city_coords = get_coords_from_address(cityName)

    def __str__(self):
        return 'TrafficData class for: \nCity: {} \nCoordinates: {}'.format(self.city_name, self.city_coords[0])

    def request_data(self, radius=1000, maxFuncClass=5, minJamFactor=0.1):
        """Request traffic flow data from the Here traffic api
        Args:
            radius: (int) Radius in m for the data request from the city center
            maxFuncClass: (int 1-5) Maximum functional street class included in the response
            minJamFactor: (float 0-10) Minimum Jam Factor included in the response
            """

        search_coords = str(self.city_coords[0]) + ',' + \
            str(self.city_coords[1]) + ',' + str(radius)
        here_traffic_url = "https://traffic.api.here.com/traffic/6.1/flow.json"

        params = {}
        params['app_id'] = here_app_id
        params['app_code'] = here_app_code
        params['prox'] = search_coords
        params['responseattributes'] = 'sh,fc'
        params['maxfunctionalclass'] = maxFuncClass
        params['minjamfactor'] = minJamFactor

        response = requests.get(here_traffic_url, params=params)
        self.radius = radius
        self.response = response.json()

    def request_data_bbox(self):
        """Alternative to request_data, tried to excess more data - failed!!!"""

        city_b = ox.gdf_from_place(self.city_name)
        bbox = [city_b.bbox_north[0], city_b.bbox_east[0],
                city_b.bbox_south[0], city_b.bbox_west[0]]
        bbox = list(map(str, bbox))
        bbox = bbox[0] + ',' + bbox[1] + ';' + bbox[2] + ',' + bbox[3]

        here_traffic_url = "https://traffic.api.here.com/traffic/6.1/flow.json"

        params = {}
        params['app_id'] = here_app_id
        params['app_code'] = here_app_code
        params['responseattributes'] = 'sh,fc'
        #params['locationreferences'] = 'shp,tmc'
        params['bbox'] = bbox
        params['maxfunctionalclass'] = 5
        params['minjamfactor'] = 0.1

        response = requests.get(here_traffic_url, params=params)
        self.response = response.json()

    def extract_geom(self):
        """extract geometry from response"""

        geom_list = []
        shp = get_keys_from_json(self.response, 'SHP')
        for geom in shp:
            nested_geom_list = get_keys_from_json(geom, 'value')
            flat_geom_list = [item for sublist in nested_geom_list for item in sublist]
            geom_list.append(flat_geom_list)

        return geom_list

    def extract_fc(self):
        """extract functional street classes from response"""

        fc_list = []
        shp = get_keys_from_json(self.response, 'SHP')
        for geom in shp:
            flat_fc_list = get_keys_from_json(geom, 'FC')
            fc_list.append(flat_fc_list)
        fc_unique = [list(set(i))[0] for i in fc_list]
        return fc_unique

    def extract(self):
        """Extract traffic information from the json response
        Args:
            CN: float range(0.0, 1.0) The Confidence attribute, indicating the
                percentage of real time data included in the speed calculation.
            JF: float range(0.0, 10.0) Jam Factor, which represents the expected
                quality of travel. When there is a road closure,
                the Jam Factor is 10.
            FF: ??? Free Flow ???
            SP: float Average Speed for the road segment.
            SU: float Average Speed Uncut for the road segment.

        """
        cf = get_keys_from_json(self.response, 'CF')
        self.sp_list = [items[0].get('SP') for items in cf]
        self.cn_list = [items[0].get('CN') for items in cf]
        self.jf_list = [items[0].get('JF') for items in cf]
        self.su_list = [items[0].get('SU') for items in cf]
        self.ff_list = [items[0].get('FF') for items in cf]

        self.fc_list = self.extract_fc()
        self.geom_list = self.extract_geom()

        # test
        list_all = [self.sp_list, self.cn_list, self.jf_list,
                    self.su_list, self.ff_list, self.fc_list, self.geom_list]
        len_test = set(map(len, list_all))

        if not len(len_test) == 1:
            raise RuntimeError(
                f'Elements have no the same number: {len_test}')

    def convert_geom(self):
        geometry = []
        for shp in self.geom_list:
            lines_list = []
            for lines in shp:
                string_list = re.sub(' ', ',', "".join(lines).strip())
                float_list = [float(i) for i in string_list.split(',')]
                xy_pairs = [float_list[i:i+2] for i in range(0, len(float_list), 2)]
                lines_list.append(LineString([Point(p[1], p[0]) for p in xy_pairs]))

            geometry.append(MultiLineString(lines_list))

        self.geometry = geometry

    def to_gdf(self):
        self.extract()
        self.convert_geom()

        geo_df = DataFrame.from_dict(
            {'fc': self.fc_list,
             'sp': self.sp_list,
             'cn': self.cn_list,
             'jf': self.jf_list,
             'su': self.su_list,
             'ff': self.ff_list,
             'geometry': self.geometry})

        self.traffic_gdf = GeoDataFrame(geo_df, geometry='geometry')
