import flickrapi
import json
import pickle

save_file = "photos_db.p"

api_key = u'736c046ac91ed5f2fe5330642e4b2db1'
api_secret = u'cc5f4efa2cfb491e'

flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')

def initialize_save_file():
    pickle_dictionary = {"enabled" : True}
    with open(save_file, "wb") as f:
        pickle.dump(pickle_dictionary, f)

#
#   Save a list of photo data to the save_file
#   Items in the list are tuples of the form (id, owner)
#
def save_to_file(city, photo_list):
    pickle_dictionary = None
    with open(save_file, "rb") as f:
        pickle_dictionary = pickle.load(f)

    with open(save_file, "wb") as f:
        pickle_dictionary[city] = photo_list
        pickle.dump(pickle_dictionary, f)


#
#   Load and return a list of photo data from the save_file
#   Items in the list are tuples of the form (id, owner)
#
def load_from_file(city):
    pickle_dictionary = None
    with open(save_file, "rb") as f:
        pickle_dictionary = pickle.load(f)

    if pickle_dictionary is not None:
        if city in pickle_dictionary:
            return pickle_dictionary[city]

    print("Error: could not load city from file")
    return None

#
#   Get the place id for any given query
#   Returns the first result in list from Flickr
#
#   Also returns latitude and longitude in following format:
#   (place_id, lat, lon)
#
def place_id(query):
    json_item = flickr.places.find(query=query)
    if "places" in json_item:
        json_item = json_item['places']
        if "place" in json_item:
            place_list = json_item['place']
            if len(place_list) > 0:
                place = place_list[0]
                return (place['place_id'], place['latitude'], place['longitude'])
        else:
            print("Error: no results for place_id query")
    else:
        print("Error: could not resolve place_id JSON")

    return (None, None, None)




#
#   Get all photos from a certain place_id, latitude, and longitude
#
def get_photos_from_place(place_id, latitude, longitude, debug=True):
    json_item = flickr.photos.search(lat=latitude,lon=longitude, place_id=place_id,
                                     accuracy=12, 
                                     per_page=500)

    # first check total number of results
    if "photos" in json_item:
        json_item = json_item['photos']
        if int(json_item['total']) > int(json_item['perpage']):
            total_pages = json_item['pages']
            print("multiple pages (" + str(total_pages) + ")")
            return get_photos_from_place_page(place_id, latitude, longitude)
        else:
            print("Error: only one page returned, need more to create map")
        if debug: print ("perpage = " + str(json_item['perpage']))

    else:
        print("Error: could not resolve JSON")

    return None


def get_photos_from_place_page(place_id, latitude, longitude, page=1, debug=True):  
    json_item = flickr.photos.search(lat=latitude,lon=longitude, place_id=place_id,
                                     accuracy=12, 
                                     per_page=500,
                                     page=page)    
    photo_list = []

    if "photos" in json_item:
        photos = json_item['photos']
        for photo in photos['photo']:
            photo_list.append((photo['id'], photo['owner']))
        #print(str(photo_list))
        return photo_list
    else:
        print("Error: could not resolve JSON")
        return None


def print_json(json_item):
    print(json.dumps(json_item, indent=4))


#first get place id
#place_id, latitude, longitude = place_id("sydney")
#print("place = " + str(place_id) + ", (lat, lon) = (" + str(latitude) + ", " + str(longitude) + ")")
#photo_list = get_photos_from_place(place_id, latitude, longitude)

#save_to_file("sydney", photo_list)
photo_list = load_from_file("sydney")
print("photo_list = " + str(photo_list))


