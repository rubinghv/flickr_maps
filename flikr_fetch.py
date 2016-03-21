import flickrapi
import json
api_key = u'736c046ac91ed5f2fe5330642e4b2db1'
api_secret = u'cc5f4efa2cfb491e'

flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')
#photos = flickr.photos.search(user_id='73509078@N00', per_page='10')
#sets = flickr.photosets.getList(user_id='73509078@N00')


#first get place id
#places = flickr.places.find(query="sydney")
#print("place id = " + str(places['places']['place'][0]))
photos_at_loc = flickr.photos.search(lat=33.8650,lon=151.2094, accuracy=11)


def parse_photos(json_item):
	if 

def print_json(json_item):
	print(json.dumps(json_item, indent=4))