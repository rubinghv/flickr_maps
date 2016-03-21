import flickrapi
import json
import pickle

api_key = u'736c046ac91ed5f2fe5330642e4b2db1'
api_secret = u'cc5f4efa2cfb491e'

flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')

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
            get_photos_from_place_page(place_id, latitude, longitude)
        else:
            print("single page")
        if debug: print ("perpage = " + str(json_item['perpage']))

    else:
        print("Error: could not resolve JSON")


def get_photos_from_place_page(place_id, latitude, longitude, page=1, debug=True):  
    json_item = flickr.photos.search(lat=latitude,lon=longitude, place_id=place_id,
                                     accuracy=12, 
                                     per_page=500)    
    photos_list = []

    if "photos" in json_item:
        photos = json_item['photos']
        print("I'm in")
        counter = 0
        for photo in photos['photo']:
            photos_list.append((photo['id'], photo['owner']))
        print(str(photos_list))
    else:
        print("Error: could not resolve JSON")


def print_json(json_item):
    print(json.dumps(json_item, indent=4))




#first get place id
place_id, latitude, longitude = place_id("sydney")
#print("place = " + str(place_id) + ", (lat, lon) = (" + str(latitude) + ", " + str(longitude) + ")")
get_photos_from_place(place_id, latitude, longitude)





