"""
Plot_Map.Range.py
===============================
Plot rectangular range on map
"""

import matplotlib.pyplot as plt
import cartopy
import cartopy.crs as ccrs
import os
import sys
sys.path.append('../')
import preprocessing.Preprocessing as Prep

def Plot_Map(Plot_Data, Plot_Config):

	# Create figure with PlateCarree projection
	fig, ax = plt.subplots(figsize=(5, 3), dpi=300, subplot_kw={'projection': ccrs.PlateCarree()})

	# Plot: rectangular range
	ax.add_patch(plt.Rectangle(\
		(Plot_Data['Range'][2], Plot_Data['Range'][0]), \
		Plot_Data['Range'][3] - Plot_Data['Range'][2], \
		Plot_Data['Range'][1] - Plot_Data['Range'][0], \
		facecolor='Green', edgecolor='none', \
		alpha=0.5, \
		transform=ccrs.PlateCarree(), \
	))
	
	# Plot configuration
	ax.set_extent([Plot_Config['Plot_extend'][2], Plot_Config['Plot_extend'][3], Plot_Config['Plot_extend'][0], Plot_Config['Plot_extend'][1]], crs=ccrs.PlateCarree())
	ax.coastlines(resolution='10m', color='black', linewidth=0.5)
	ax.add_feature(cartopy.feature.BORDERS, linewidth=0.4, linestyle='-', alpha=.5)

	# Add topography
	ax.stock_img()
	ax.add_feature(cartopy.feature.LAND, edgecolor='grey', linewidth=0.5)
	ax.add_feature(cartopy.feature.OCEAN, edgecolor='grey', linewidth=0.5)
	ax.add_feature(cartopy.feature.LAKES, edgecolor='grey', linewidth=0.5)
	ax.add_feature(cartopy.feature.RIVERS, edgecolor='grey', linewidth=0.5)

	# Add gridlines
	gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True, linewidth=0.5, color='grey', alpha=0.5, linestyle='--')
	gl.top_labels = False
	gl.right_labels = False
	gl.xformatter = cartopy.mpl.gridliner.LONGITUDE_FORMATTER
	gl.yformatter = cartopy.mpl.gridliner.LATITUDE_FORMATTER
	gl.xlabel_style = {'size': 6, 'color': 'black'}
	gl.ylabel_style = {'size': 6, 'color': 'black'}

	# Save figure
	Output_Path = '../output/Output_Figure/Plot_Map.Range/'
	Output_File = 'Plot_Map.Range.{Range}.png'.format(Range=i_Range)
	if not os.path.exists(Output_Path): os.makedirs(Output_Path)
	plt.tight_layout()
	plt.savefig(Output_Path + Output_File)
	plt.close('all')

	return

if (__name__ == '__main__'):

	# Set plotting ranges list
	Range_List = ['CentralChina_Analysis', 'SouthChina_Analysis']

	for i_Range in Range_List:

		# Plot the rectangular range on East-Asia map
		Plot_Data = {\
			'Range'      : Prep.Get_Range(i_Range), \
		}

		Plot_Config = {\
			'Plot_extend': Prep.Get_Range('EastAsia_Analysis'), \
		}

		Plot_Map(Plot_Data, Plot_Config)