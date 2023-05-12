"""
Plot_Map.Monthly_Anomaly.py
===========================
Plot monthly anomalies of lwe_thickness
"""

import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import cartopy
import cartopy.crs as ccrs
import warnings
import os
import sys
sys.path.append('../')
import preprocessing.Preprocessing_Get_Data as PrepGD
import preprocessing.Preprocessing as Prep

def Plot_Map(Plot_Data, Plot_Config):

	# Create figure
	fig, ax = plt.subplots(figsize=(10, 6), dpi=150, subplot_kw={'projection': ccrs.PlateCarree()})

	# Plot: rectangular range
	Rectangular_Range = Prep.Get_Range(Plot_Data['Rectangular_Range'])
	ax.add_patch(plt.Rectangle(\
		(Rectangular_Range[2], Rectangular_Range[0]), \
		Rectangular_Range[3] - Rectangular_Range[2], \
		Rectangular_Range[1] - Rectangular_Range[0], \
		facecolor='none', edgecolor='Red', \
		alpha=0.6, \
		zorder=20, \
		transform=ccrs.PlateCarree(), \
	))
	
	# Plot: anomaly
	Data_pcolormesh = ax.pcolormesh(\
		Plot_Data['Lon'], Plot_Data['Lat'], \
		Plot_Data['Data_Anomaly'], \
		cmap=Plot_Config['Plot_cmap'], vmin=Plot_Config['Plot_pcolormesh_vmin'], vmax=Plot_Config['Plot_pcolormesh_vmax'], \
		transform=ccrs.PlateCarree(), \
	)

	# Plot: hatch for Data_Significance < -2 or > 2
	ax.contourf(\
		Plot_Data['Lon'], Plot_Data['Lat'], \
		np.where((~np.isnan(Plot_Data['Data_Anomaly'])), Plot_Data['Data_Significance'], np.nan), \
		colors='none', levels=[-999, -2, 2, 999], hatches=['////', '', '////'], zorder=9, \
		transform=ccrs.PlateCarree(), \
	)
	mpl.rcParams['hatch.linewidth'] = 0.5

	# Colorbar
	cbar = plt.colorbar(\
		Data_pcolormesh, \
		orientation='vertical', \
		extend='both', \
	)
	cbar.ax.tick_params(labelsize=12)

	# Plot configuration
	Lat_Min, Lat_Max, Lon_Min, Lon_Max = Prep.Get_Range('EastAsia_Analysis')
	ax.set_extent([Lon_Min, Lon_Max, Lat_Min, Lat_Max], crs=ccrs.PlateCarree())
	ax.coastlines(resolution='10m', color='black', linewidth=0.5)
	ax.add_feature(cartopy.feature.BORDERS, linewidth=0.4, linestyle='-', alpha=0.5)

	# Add gridlines
	gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True, linewidth=0.5, color='grey', alpha=0.5, linestyle='--')
	gl.top_labels = False
	gl.right_labels = False
	gl.xformatter = cartopy.mpl.gridliner.LONGITUDE_FORMATTER
	gl.yformatter = cartopy.mpl.gridliner.LATITUDE_FORMATTER
	gl.xlabel_style = {'size': 12, 'color': 'black'}
	gl.ylabel_style = {'size': 12, 'color': 'black'}

	# Save figure
	Output_Path = '../output/Output_Figure/Plot_Map.Monthly_Anomaly/{Var}/'.format(Var=Plot_Config['Var'])
	Output_File = 'Plot_Map.Monthly_Anomaly.{Var}.{Month}.png'.format(Var=Plot_Config['Var'], Month=Plot_Config['Month'])
	if not os.path.exists(Output_Path): os.makedirs(Output_Path)
	plt.tight_layout()
	plt.savefig(Output_Path + Output_File)
	plt.close('all')

	return

if (__name__ == '__main__'):

	# Get data
	Data, Time, Lat, Lon = PrepGD.Get_Data()
	
	# Crop data
	Data, Lat, Lon = Prep.Crop_Range(Data, Lat, Lon, Range='EastAsia_Analysis_Extended')

	# Convert Time to YYYY-MM-DD format and convert to pandas datetime
	Time = pd.Series([pd.to_datetime(str(i_Time)[0:10]) for i_Time in Time])
	
	# ==================================================
	# Plot anomaly for each month
	for ind_Month in np.arange(12):

		# Extract data for the month
		Data_Month = Data[Time.dt.month == (ind_Month + 1), ...]

		# Extract data for 2022 and the month
		Data_2022 = Data[(Time.dt.year == 2022)&(Time.dt.month == (ind_Month + 1)), ...].squeeze()

		# Skip if Data_2022 is empty
		if (Data_2022.size == 0): continue

		# Calculate the mean, standard deviation
		with warnings.catch_warnings():
			
			warnings.simplefilter('ignore', category=RuntimeWarning)
			
			Data_Clim_Mean = np.nanmean(Data_Month, axis=0)
			Data_Clim_Std  = np.nanstd(Data_Month, axis=0)

		Plot_Data = {\
			'Lon'                 : Lon, \
			'Lat'                 : Lat, \
			'Data_Anomaly'        : (Data_2022 - Data_Clim_Mean), \
			'Data_Significance'   : (Data_2022 - Data_Clim_Mean) / Data_Clim_Std, \
			'Rectangular_Range'   : 'SouthChina_Analysis', \
		}

		Plot_Config = {\
			'Plot_pcolormesh_vmin': -0.1, \
			'Plot_pcolormesh_vmax': 0.1, \
			'Plot_cmap'           : 'BrBG', \
			'Var'                 : 'Liquid_water_equivalent_thickness', \
			'Month'               : ind_Month + 1, \
		}

		# Plot map
		Plot_Map(Plot_Data, Plot_Config)