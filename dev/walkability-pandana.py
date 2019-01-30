from sumo_tools import get_streets, get_coords
import googlemaps
import osmnx as ox
from pandana.loaders import osm
import folium

from api_keys import here_app_id, here_app_code, google_api_key

%load_ext autoreload
%autoreload


streets_w = get_streets('Lörrach, Germany', 'walk')
city_name = 'Lörrach, Germany'
street_type = 'drive'
city_boundary = ox.gdf_from_place(city_name).geometry.iloc[0]
drive_net = ox.graph_from_polygon(city_boundary, network_type=street_type)

# plot strees on folium
graph_folium = ox.plot_graph_folium(drive_net, popup_attribute='highway')
graph_folium.save('map.html')


drive_gpd = ox.graph_to_gdfs(drive_net, nodes=True, edges=False,
                             fill_edge_geometry=False, node_geometry=True)
drive_gpd_sub = drive_gpd
roads_json = drive_gpd_sub.to_json()
points = folium.features.GeoJson(roads_json)
m = folium.Map([47.6120896, 7.6607218])
m.add_children(points)
m.save('map.html')

streets_w.plot()

streets_w.size
streets_w_drop_na = streets_w.dropna(subset=['geometry', 'maxspeed'])
streets_w_drop_na.size
streets_w_drop_na.plot()
is_list = streets_w_drop_na.maxspeed.apply(lambda x: isinstance(x, list))

streets_w_drop_na[is_list].plot()


def bigger(list):
    if list[0] > list[1]:
        return list[0]
    else:
        return list[1]


streets_w_drop_na['maxspeed_clean'] = streets_w_drop_na.maxspeed
streets_w_drop_na['maxspeed_clean'][is_list] = streets_w_drop_na.maxspeed[is_list].apply(bigger)
streets_w_drop_na['maxspeed_clean'] = streets_w_drop_na.maxspeed_clean.astype(int)
streets_w_drop_na.plot(column='maxspeed_clean', legend=True)

streets_w_drop_na['maxspeed_clean']

for i in streets_w_drop_na['maxspeed'].iloc[1]:
    print(i)


streets_w_drop_na['maxspeed'].iloc[1] isinstance([12, 3], list)

# download buildings inside the boundary
buildings = ox.buildings.create_buildings_gdf(city)


coords = get_coords('Lörrach, Germany')

type = 'store'
radius = 1000

# google
gmaps = googlemaps.Client(key=google_api_key)

places = gmaps.places_nearby(location=coords, radius=radius, type=type)
google_places = []

for result in places['results']:
    google_places.append(result['name'])


# here

here_places = herepy.PlacesApi(here_app_id, here_app_code)

response = here_places.onebox_search(coords, type)


here_places = []

for result in response.results['items']:
    here_places.append(result['title'])
