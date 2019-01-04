from sumo_tools import get_coords
import googlemaps
import herepy


from api_keys import here_app_id, here_app_code, google_api_key

%load_ext autoreload
%autoreload


coords = get_coords('Lörrach, Germany')

coords = [47.6120896, 7.6607218]
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
