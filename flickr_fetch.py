import flickrapi
import json
import pickle
import datetime, calendar
from progress.bar import Bar

save_file = "photos_db.p"

api_key = u'736c046ac91ed5f2fe5330642e4b2db1'
api_secret = u'cc5f4efa2cfb491e'

flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')

def merge_two_dicts(original, added):
    return_dict = original.copy()
    #print("merge size before = " + str(len(return_dict)))
    for key, value in added.items():
        if key not in return_dict:
            return_dict[key] = value
    #print("merge size after = " + str(len(return_dict)))
    return return_dict

def initialize_save_file():
    pickle_dictionary = {"enabled" : True}
    with open(save_file, "wb") as f:
        pickle.dump(pickle_dictionary, f)

#
#   Save a dictionary of photo data to the save_file
#   Items in the dictionary use id as their key
#
def save_to_file(city_name, city_dict):
    pickle_dictionary = None
    with open(save_file, "rb") as f:
        pickle_dictionary = pickle.load(f)

    with open(save_file, "wb") as f:
        pickle_dictionary[city_name] = city_dict
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
def get_place_id(query):
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
#   However number of photos returned is limited to 1500, so limit time frame to constrain that
#
def get_photos_from_place(place_id, latitude, longitude, days_back=30, debug=True):
    photos_dict = {}

    day_interval = 1
    today_date = datetime.datetime.utcnow()
    start_date = today_date
    
    bar = Bar('Fetching photos info', suffix='%(percent)d%%  -  Time remaining: %(eta)ds', max=days_back)

    for day in range(1, days_back + 1):
        # update date and timestamps
        end_date = start_date
        start_date = start_date - datetime.timedelta(days=day_interval)

        end_timestamp = calendar.timegm(end_date.timetuple())
        start_timestamp = calendar.timegm(start_date.timetuple())

        json_item = flickr.photos.search(lat=latitude,lon=longitude, place_id=place_id,
                                         accuracy=12, 
                                         per_page=250,
                                         min_upload_date=start_timestamp,
                                         max_upload_date=end_timestamp)

        # first check total number of results
        if "photos" in json_item:
            json_item = json_item['photos']
            if int(json_item['total']) > 0:
                total_pages = json_item['pages']
                #print("total results for date (" + str(start_date) + ") = " + str(json_item['total']))
                #print("multiple pages (" + str(total_pages) + ")")
                #print ("perpage = " + str(json_item['perpage']))

                for page in range(1, total_pages + 1):
                    #if page % 10 == 0:
                    #    print("At page: " + str(page))
                    photo_dict = get_photos_from_place_page(place_id, latitude, longitude, start_timestamp, end_timestamp, page=page)
                    photos_dict = merge_two_dicts(photo_dict, photos_dict)
                    #print("after page " + str(page) + ", total size = " + str(len(photos_dict)))

            else:
                print("Error: no results found and returned")

        else:
            print("Error: could not resolve JSON")

        bar.next()

    bar.finish()
    return photos_dict

#
#   Get a given page's photos given search query
#   for place, longitude and latitude, and timestamps
#
def get_photos_from_place_page(place_id, latitude, longitude, start_timestamp, end_timestamp, page=1, debug=True):  
    json_item = flickr.photos.search(lat=latitude,lon=longitude, place_id=place_id,
                                     accuracy=12, 
                                     per_page=250,
                                     page=page,
                                     min_upload_date=start_timestamp,
                                     max_upload_date=end_timestamp)
    photos_dict = {}

    if "photos" in json_item:
        photos = json_item['photos']
        for photo in photos['photo']:
            if photo['id'] not in photos_dict:
                photo_dict = { 'photo id' : photo['id'], 
                               'owner' : photo['owner'] }
                photos_dict[photo['id']] = photo_dict

        return photos_dict
    else:
        print("Error: could not resolve JSON")
        return None


def print_json(json_item):
    print(json.dumps(json_item, indent=4))


#
#   For the given dictionary, attach location data by querying Flickr.
#   Only look for location data if it is not already present
#
def get_all_photo_locations(photos_dict, limit=1000):
    counter = 0
    bar = Bar('Fetching locations', suffix='%(percent)d%%  -  Time remaining: %(eta)ds', max=limit)

    for key, photo_dict in photos_dict.items():
        if counter >= limit:
            break

        if 'latitude' not in photo_dict:
            #print("getting location")
            get_photo_location(photo_dict)
            counter += 1
            bar.next()
            #if counter % 10 == 0:
                #print("Photo locations resolved = " + str(counter))
        #else:
        #    print("location already there")

    bar.finish()
    return photos_dict

#
#   Get the longitude and latitude given a photo_id
#
def get_photo_location(photo_dict):
    json_item = flickr.photos.geo.getLocation(photo_id=photo_dict['photo id'])

    if "photo" in json_item and json_item['stat'] == 'ok':
        json_item = json_item['photo']
        if 'location' in json_item:
            location = json_item['location']
            if 'longitude' in location and 'latitude' in location:
                photo_dict['latitude'] = location['latitude']
                photo_dict['longitude'] = location['longitude']
                photo_dict['accuracy'] = location['accuracy']
                #print_json(json_item)
                return photo_dict
                
            else:
                print("Error: no longitude and latitude returned by Flickr")
        else:
            print("Error: no location returned by Flickr")
    else:
        print("Error: could not resolve JSON")
    
    return None




