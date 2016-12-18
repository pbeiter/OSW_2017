import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import pandas as pd
import matplotlib.colors as mcolors # color map
import numpy as np
#plt.ion() # to show figures automatically

### colormaputil.py for truncating scale

years = [2013, 2020, 2025]

'''
students = [
    ("John", ["CompSci", "Physics"]),
    ("Vusi", ["Maths", "CompSci", "Stats"]),
    ("Jess", ["CompSci", "Accounting", "Economics", "Management"]),


regions = ['pacific': ([(-125,32),(-116.5,49),(-120,35)]),
		   'atlantic': ([(-81,25),(-65,45),(-75,38)]),
           'gulf': ([(-98,25),(-83,31),(-90,28)]),
		   'greatlakes': ([(-92,41),(-75,49),(-85,45)]),
		   'hawaii': ([(-161,18),(-154,24.5),(-157,20)]),]

for region, year in zip(regions, years):
'''

regions = {'pacific': 	{'lllon': -125,
						   'lllat': 32,
						   'urlon': -116.5,
						   'urlat': 49,
						   'lon_cen': -120,
						   'lat_cen': 35},
		   'atlantic': 	{'lllon': -81,
						   'lllat': 25,
						   'urlon': -65,
						   'urlat': 45,
						   'lon_cen': -75,
						   'lat_cen': 35},
		   'gulf': 		{'lllon': -98,
							'lllat': 25,
							'urlon': -83,
							'urlat': 31,
							'lon_cen': -90,
							'lat_cen': 28},
		   'greatlakes':{'lllon': -92,
							'lllat': 41,
							'urlon': -75,
							'urlat': 49,
							'lon_cen': -85,
							'lat_cen': 45},
		   'hawaii': 	{'lllon': -161,
						    'lllat': 18,
							'urlon': -154,
							'urlat': 24.5,
							'lon_cen': -157,
							'lat_cen': 20}}

#for region, year in zip(regions, years):
#for region, year in enumerate(regions, years):
for region in regions:

	for year in years:
		print ("Processing: {} - {}...".format(region, year))

		dat = pd.read_csv("Results/Analysis_Results_{}.csv".format(year))

		fignum = 100
		fig = plt.figure(figsize=[10, 12]) #6,10
		#fig.clf()
		ax = plt.gca() # get current axis (e.g., if there's not one present such as after fig.clf)
		ax.set_axis_bgcolor('azure')

		map = Basemap(llcrnrlon=regions[region]['lllon'], llcrnrlat=regions[region]['lllat'], # latitude, longitude (e.g. Google Earth)
		              urcrnrlon=regions[region]['urlon'], urcrnrlat=regions[region]['urlat'],
		              projection='lcc', # projection options: cea, tmerc, cyl
		              lon_0=regions[region]['lon_cen'], lat_0=regions[region]['lat_cen'], # in middle/center where you're working
		              resolution='i') # resolution, e.g. "f" for full; i for intermediate
						  
		#cmap = plt.get_cmap('viridis_r')
	
		#colors = np.vstack((plt.cm.cool(np.linspace(0., 1, 128)), # chose e.g. 12 and 6 ("discrete color maps")
		#                    plt.cm.autumn(np.linspace(0., 1, 128))))[::-1] #RGBA color scheme
			

		#cmap = mcolors.LinearSegmentedColormap.from_list('split', colors)
		#cmap = plt.get_cmap('coolwarm_r') #"_r" reverses color map
		#cmap = plt.get_cmap('brg_r')
		cmap = plt.get_cmap('summer', 10) # for green color (YlGn) map (disrete, 11) ---


		#map.fillcontinents(color='0.4', lake_color='azure',)
		map.drawlsmask(ocean_color='#EFFBFB')
		#map.bluemarble()
		#map.shadedrelief() # basemap drawing on map (e.g. blue marble, shaeded relief, Etopos, e.g. map.fillcontinents(color='0.9', lake_color='b')))
		map.drawstates()
		map.drawcountries()
		#map.drawcounties()
		#map.drawmapboundary(fill_color='c')

		scat = map.scatter(dat.Longitude.values, dat.Latitude.values, 12, # x, y points, size, color (in this case numbers)
		                   c=dat.LCOE, edgecolors='none', latlon=True,
		                   cmap=cmap, vmin=-0, vmax=200) # cmap assigns color map to data points, vmin and vmax are borders of scale

		cbar = plt.colorbar(scat, format='%.0f')
		cbar.set_label('LCOE ($/MWh)', size=20)
		cbar.ax.tick_params(labelsize=12) 
		cbar.set_ticks(np.linspace(0,200,11))
		cbar.set_clim([0, 200])

		fig.savefig('Figures/Hmap_LCOE_{}_{}.png'.format(region, year,dpi=1000))
		fig.clf()

