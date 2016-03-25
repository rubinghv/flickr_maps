import sys
from time import sleep
from datetime import datetime, timedelta

from flickr_fetch import initialize_save_file, get_place_id, get_photos_from_place, save_to_file, load_from_file, get_all_photo_locations
#from visualization import create_map, plot_on_map, show_map

#
#	Get all the photos taken at a certain place over the 
#	last days_back (from now to now - days_back)
#
def get_photos(place, start_day=0, days_back=30):
	photos_dict = load_from_file(place)

	place_id, latitude, longitude = get_place_id(place)
	photos_dict = get_photos_from_place(place_id, latitude, longitude, photos_dict, start_day=start_day, days_back=days_back)

	#print("total photos in db = " + str(len(photos_dict)))
	save_to_file(place, photos_dict)



#
#	Load photo information from the database and add the location
#	to photos that are missing that data
#
def get_photos_location(place, limit=1000):
	photos_dict = load_from_file(place)

	with_location = 0
	for key, photo_dict in photos_dict.items():
	    if 'latitude' in photo_dict: 
	        with_location += 1 


	print("before: total photos (with location) = " + str(len(photos_dict)) + " (" + str(with_location) + ")")
	photos_dict = get_all_photo_locations(photos_dict, place, limit=limit)

	with_location = 0
	for key, photo_dict in photos_dict.items():
	    if 'latitude' in photo_dict: 
	        with_location += 1 
	print("after: total photos (with location) = " + str(len(photos_dict)) + " (" + str(with_location) + ")")

	save_to_file(place, photos_dict)
	
	if len(photos_dict) - with_location < 1:
		print("Got all locations")
		return True
	else:
		return False

#
#	Export it so it can be printed here: http://www.darrinward.com/lat-long/
#
def get_location_data(place):
	photos_dict = load_from_file(place)

	return_tuple_list = []
	for key, photo_dict in photos_dict.items():
		if 'latitude' in photo_dict: 
			return_tuple_list.append((float(photo_dict['latitude']), 
									  float(photo_dict['longitude'])))

	return return_tuple_list




#
#
#
def get_city_data(city_name):


	# first get the picture data for the past year
	get_photos(city_name, start_day=0, days_back=360)

	first_loop = True
	minutes_to_sleep = 60

	while True:
		if first_loop: 
			limit = 2000
		else:
			limit = 3200


		if get_photos_location(city_name, limit=limit):
			print("Photo info and locations complete, exiting.")
			return

		print("going to sleep for " + str(minutes_to_sleep) + " minutes at " + str(datetime.now()))
		sleep(minutes_to_sleep * 60)
		print("resuming after sleep")

		first_loop = False


if (len(sys.argv) > 1):
	city_name = sys.argv[1]
	get_city_data(city_name)
else:
	print("Error: no command line argument received, please add city name")



# location_data = get_location_data("sydney")
# #print(str(location_data))
# bmap = create_map()
# for lat, lon in location_data:
# 	#print(str(lat) + "," + str(lon))
# 	plot_on_map(bmap, float(lat), float(lon))
# show_map()
