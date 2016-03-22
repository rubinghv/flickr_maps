from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np

#
#	Create a Basemap and return it
#
def create_map():
	lower_left_lat = -34.126127
	lower_left_lon = 150.951113
	upper_right_lat = -33.751265
	upper_right_lon = 151.425672

	# map = Basemap(projection='merc', lat_0 = 57, lon_0 = -135,
	#     resolution = 'h', area_thresh = 0.1,
	#     llcrnrlon=-136.25, llcrnrlat=56.0,
	#     urcrnrlon=-134.25, urcrnrlat=57.75)

	map = Basemap(projection='merc',
				  llcrnrlat=lower_left_lat,
				  urcrnrlat=upper_right_lat,
	              llcrnrlon=lower_left_lon,
	              urcrnrlon=upper_right_lon,
	              resolution='f')

	map.drawcoastlines()
	map.drawcountries()
	map.fillcontinents(lake_color='aqua')
	map.drawmapboundary()

	return map

#
#	Plot coordinates lat, lon on the Basemap map
#
def plot_on_map(map, lat, lon):
	x,y = map(lon, lat)
	map.plot(x, y, 'bo', markersize=3)

def show_map():
	plt.show()

# map = create_map()
# plot_on_map(map, -33.902407, 151.228862)
# show_map()