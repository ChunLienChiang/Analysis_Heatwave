"""
Plot_Map.Monthly_Anomaly.py
===========================
Plot monthly anomalies of:
1. precipitation
2. Skin reservoir content
3. Volumetric soil waters
4. 2m temperature
5. Skin temperature
6. Evaporation
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

def Get_Plot_vmin_vmax(Var):

	# Set vmin and vmax
	if (Var == 'tp'):

		Plot_pcolormesh_vmin = -0.4
		Plot_pcolormesh_vmax = 0.4

	elif (Var == 'src'):

		Plot_pcolormesh_vmin = -2e-4
		Plot_pcolormesh_vmax = 2e-4

	elif (Var in ['swvl1', 'swvl2', 'swvl3', 'swvl4']):

		Plot_pcolormesh_vmin = -0.2
		Plot_pcolormesh_vmax = 0.2

	elif (Var == 't2m'):

		Plot_pcolormesh_vmin = -4
		Plot_pcolormesh_vmax = 4

	elif (Var == 'skt'):

		Plot_pcolormesh_vmin = -4
		Plot_pcolormesh_vmax = 4

	elif (Var == 'e'):

		Plot_pcolormesh_vmin = -0.003
		Plot_pcolormesh_vmax = 0.003

	else:

		raise ValueError('Wrong variable name')

	return Plot_pcolormesh_vmin, Plot_pcolormesh_vmax

def Get_Plot_cmap(Var):

	if (Var == 'tp'):

		Plot_cmap = 'BrBG'

	elif (Var == 'src'):

		Plot_cmap = 'coolwarm'

	elif (Var in ['swvl1', 'swvl2', 'swvl3', 'swvl4']):

		Plot_cmap = 'BrBG'

	elif (Var == 't2m'):

		Plot_cmap = 'coolwarm'

	elif (Var == 'skt'):

		Plot_cmap = 'coolwarm'

	elif (Var == 'e'):

		Plot_cmap = 'BrBG'

	else:

		raise ValueError('Wrong variable name')

	return Plot_cmap

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

	VarName_File_List   = ['t2m', 'skt', 'e', 'tp', 'src', 'swvl1', 'swvl2', 'swvl3', 'swvl4']

	for i_Var in VarName_File_List:

		# Print message
		print('Plotting {Var}...'.format(Var=i_Var))

		# Get data
		Data, Time, Lat, Lon = PrepGD.Get_Data(i_Var)
		
		# Crop data
		Data, Lat, Lon = Prep.Crop_Range(Data, Lat, Lon, Range='EastAsia_Analysis_Extended')

		# Convert Time to YYYY-MM-DD format and convert to pandas datetime
		Time = pd.Series([pd.to_datetime(str(i_Time)[0:10]) for i_Time in Time])
		
		# ==================================================
		# Get climatological seasonal cycle
		Data_SeasonalCycle = Data.reshape(-1, 12, *Data.shape[-2:])

		# Extract 2022 data by selecting the Time with year 2022
		Data_2022 = Data[Time.dt.year == 2022, ...]

		# ==================================================
		# Plot anomaly for each month
		for ind_Month in np.arange(12):

			# Calculate the mean, standard deviation
			with warnings.catch_warnings():
				
				warnings.simplefilter('ignore', category=RuntimeWarning)
				Data_Clim_Mean = np.nanmean(Data_SeasonalCycle[:, ind_Month, ...], axis=0)
				Data_Clim_Std  = np.nanstd(Data_SeasonalCycle[:, ind_Month, ...], axis=0)

			Plot_Data = {\
				'Lon'                 : Lon, \
				'Lat'                 : Lat, \
				'Data_Anomaly'        : (Data_2022[ind_Month, ...] - Data_Clim_Mean), \
				'Data_Significance'   : (Data_2022[ind_Month, ...] - Data_Clim_Mean) / Data_Clim_Std, \
				'Rectangular_Range'   : 'SouthChina_Analysis', \
			}

			Plot_Config = {\
				'Plot_pcolormesh_vmin': Get_Plot_vmin_vmax(i_Var)[0], \
				'Plot_pcolormesh_vmax': Get_Plot_vmin_vmax(i_Var)[1], \
				'Plot_cmap'           : Get_Plot_cmap(i_Var), \
				'Var'                 : i_Var, \
				'Month'               : ind_Month + 1, \
			}

			# Plot map
			Plot_Map(Plot_Data, Plot_Config)