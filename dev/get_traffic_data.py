

from tools.traffic_data import TrafficData
from tools.utiles import get_keys_from_json

traffic_frei = TrafficData(cityName='Freiburg, Germany')

traffic_frei.request_data(10000)
traffic_frei.extract()

traffic_frei.to_gdf()
traffic_frei.traffic_gdf.plot(column='jf')

traffic_frei.traffic_gdf.to_file('../data/freiburg/traffic_big.geojson', driver='GeoJSON')


