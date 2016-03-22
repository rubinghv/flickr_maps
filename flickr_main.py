from flickr_fetch import initialize_save_file, get_place_id, get_photos_from_place, save_to_file, load_from_file, get_all_photo_locations
from visualization import create_map, plot_on_map, show_map

#
#	Get all the photos taken at a certain place over the 
#	last days_back (from now to now - days_back)
#
def get_photos(place, days_back=30, reset_save_file=False):
	if reset_save_file: initialize_save_file()

	place_id, latitude, longitude = get_place_id(place)
	photo_dict = get_photos_from_place(place_id, latitude, longitude, days_back=days_back)

	save_to_file(place, photo_dict)


#
#	Load photo information from the database and add the location
#	to photos that are missing that data
#
def get_photos_location(place):
	photos_dict = load_from_file(place)
	print("photo list size = " + str(len(photos_dict)))
	with_location = 0
	for key, photo_dict in photos_dict.items():
	    if 'latitude' in photo_dict: 
	        with_location += 1 
	print("before with location = " + str(with_location))

	photos_dict = get_all_photo_locations(photos_dict, place)

	with_location = 0
	for key, photo_dict in photos_dict.items():
	    if 'latitude' in photo_dict: 
	        with_location += 1 
	print("after with location = " + str(with_location))

	save_to_file(place, photos_dict)



#
#	Export it so it can be printed here: http://www.darrinward.com/lat-long/
#
def get_location_data(place):
	photos_dict = load_from_file("sydney")

	return_tuple_list = []
	for key, photo_dict in photos_dict.items():
		if 'latitude' in photo_dict: 
			return_tuple_list.append((photo_dict['latitude'], photo_dict['longitude']))

	return return_tuple_list

#get_photos("sydney", 30, True)
#get_photos_location("sydney")

location_data = get_location_data("sydney")
#print(str(location_data))
map = create_map()
for lat, lon in location_data:
	plot_on_map(map, float(lat), float(lon))
show_map()
