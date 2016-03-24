from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import math
import pyproj

#
#	Create a Basemap and return it
#
def create_map():
	lower_left_lat = -34.126127
	lower_left_lon = 150.951113
	upper_right_lat = -33.751265
	upper_right_lon = 151.425672


	bmap = Basemap(#projection='merc',
				  llcrnrlat=lower_left_lat,
				  urcrnrlat=upper_right_lat,
	              llcrnrlon=lower_left_lon,
	              urcrnrlon=upper_right_lon,
	              resolution='f')#,
	             # epsg=3857)

	bmap.drawcoastlines()
	bmap.drawcountries()
	bmap.fillcontinents(lake_color='aqua')
	bmap.drawmapboundary()

	return bmap

#
#	Plot coordinates lat, lon on the Basemap map
#
def plot_on_map(bmap, lat, lon):
	#gda94 = pyproj.Proj(init='epsg:4283')
	#mgaz56 = pyproj.Proj(init='epsg:4326')
	#x, y = pyproj.transform(gda94, mgaz56, lon, lat)

	x,y = bmap(lon, lat)
	bmap.plot(x, y, 'bo', markersize=1)

def show_map():
	plt.show()

#mgi = -34.00314109942555, 151.2523551179208

# map = create_map()
# plot_on_map(map, -34.002055, 151.248885)
# show_map()



