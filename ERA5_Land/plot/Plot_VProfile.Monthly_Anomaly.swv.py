"""
Plot_VProfile.Monthly_Anomaly.swv.py
===========================
Plot monthly anomalies of volumetric soil waters in four different layers
The vertical axis is the depth of the soil layer
The horizontal axis is the time (2022-01 to 2022-12)
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import xarray as xr
import warnings
import os
import sys
sys.path.append('../')
import preprocessing.Preprocessing_Get_Data as PrepGD
import preprocessing.Preprocessing as Prep

def Plot_VProfile(Plot_Data, Plot_Config):
	
	# Create figure
	fig, ax = plt.subplots(nrows=4, sharex=True, figsize=(9, 9), dpi=300)

	# Plot contourf: lwet
	ax[0].plot(\
		np.arange(1, 13), \
		Plot_Data['Data_lwet_Anomaly'], \
		color='Black', \
		linewidth=2, \
	)
	ax[0].hlines(\
		0, 1, 12, \
		color='Black', \
		linewidth=1, \
	)
	ax[0].fill_between(\
		np.arange(1, 13), \
		Plot_Data['Data_lwet_CI'][0], Plot_Data['Data_lwet_CI'][1], \
		color='Black', \
		alpha=0.2, \
	)

	# Plot contourf: tp
	ax[1].plot(\
		np.arange(1, 13), \
		Plot_Data['Data_tp_Anomaly'], \
		color='Blue', \
		linewidth=2, \
	)
	ax[1].hlines(\
		0, 1, 12, \
		color='Black', \
		linewidth=1, \
	)
	ax[1].fill_between(\
		np.arange(1, 13), \
		Plot_Data['Data_tp_CI'][0], Plot_Data['Data_tp_CI'][1], \
		color='Blue', \
		alpha=0.2, \
	)

	# Plot contourf: t2m
	ax[2].plot(\
		np.arange(1, 13), \
		Plot_Data['Data_t2m_Anomaly'], \
		color='Red', \
		linewidth=2, \
	)
	ax[2].hlines(\
		0, 1, 12, \
		color='Black', \
		linewidth=1, \
	)
	ax[2].fill_between(\
		np.arange(1, 13), \
		Plot_Data['Data_t2m_CI'][0], Plot_Data['Data_t2m_CI'][1], \
		color='Red', \
		alpha=0.2, \
	)

	# Plot contourf: swvl
	Data_contourf = ax[3].contourf(\
		np.arange(1, 13), \
		[-3.5, -17.5, -64, -194.5], \
		Plot_Data['Data_swv_Anomaly'].T, \
		levels=np.linspace(Plot_Config['Plot_pcolormesh_vmin'], Plot_Config['Plot_pcolormesh_vmax'], 21), \
		cmap=Plot_Config['Plot_cmap'], \
		extend='both', \
	)

	# Plot red points for Data_Significance < -2 or > 2
	scatter_x, scatter_y = np.meshgrid(np.arange(1, 13), [-3.5, -17.5, -64, -194.5])
	ax[3].scatter(\
		scatter_x.ravel(), scatter_y.ravel(), \
		c=np.where(np.abs(Plot_Data['Data_swv_Significance'])>2, 1, np.nan).T.ravel(), \
		cmap='Reds', \
		vmin=0, vmax=1.5, \
		marker='o', s=15, \
		zorder=10, \
	)
	
	# Colorbar at the right side of the plot
	fig.subplots_adjust(right=0.8)
	cbar_ax = fig.add_axes([0.85, 0.15, 0.02, 0.7])
	cbar = fig.colorbar(Data_contourf, cax=cbar_ax)
	cbar.ax.tick_params(labelsize=12)
	cbar.set_label('Volumetric Soil Water Anomaly \n(cm$^3$/cm$^3$)', fontsize=12)

	# Set xticks
	ax[0].set_ylabel('LWE Thickness \n(m)', fontsize=12)
	ax[0].set_ylim([-0.1, 0.1])
	ax[0].set_yticks([-0.1, 0, 0.1])

	ax[1].set_ylabel('Precip. Anomaly \n(mm/day)', fontsize=12)
	ax[1].set_ylim([-0.2, 0.2])
	ax[1].set_yticks([-0.2, -0.1, 0, 0.1, 0.2])

	ax[2].set_ylabel('T2m Anomaly \n($^\circ$C)', fontsize=12)
	ax[2].set_ylim([-4, 4])
	ax[2].set_yticks([-4, -2, 0, 2, 4])

	ax[3].set_xticks(np.arange(1, 13))
	ax[3].set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], fontsize=12)
	ax[3].set_xlabel('Month of 2022', fontsize=12)
	ax[3].set_yticks([-3.5, -28, -100, -194.5])
	ax[3].set_ylabel('Depth (cm)', fontsize=12)
	ax[3].set_ylim([-194.5, -3.5])

	# Save figure
	Output_Path = '../output/Output_Figure/Plot_VProfile.Monthly_Anomaly.swv/'
	Output_File = 'Plot_VProfile.Monthly_Anomaly.swv.png'
	if not os.path.exists(Output_Path): os.makedirs(Output_Path)
	#plt.tight_layout()
	plt.savefig(Output_Path + Output_File)
	plt.close('all')


def Get_Data_swv():

	Data = []

	for i_Var in ['swvl1', 'swvl2', 'swvl3', 'swvl4']:

		# Read data
		Data_swv, Time, Lat, Lon = PrepGD.Get_Data(i_Var)
		
		# Calculate spatial average
		Data_swv = Prep.Calc_SpatialAverage(Data_swv, Lat, Lon, 'SouthChina_Analysis')
		
		Data.append(Data_swv[:, None])

	# Concatenate data
	Data = np.concatenate(Data, axis=1)

	# Convert Time to YYYY-MM-DD format and convert to pandas datetime
	Time = np.array([pd.to_datetime(str(i_Time)[0:10]) for i_Time in Time])
	
	return Data, Time

def Get_Data_tp():

	# Read data
	Data_tp, _, Lat, Lon = PrepGD.Get_Data('tp')

	# Calculate spatial average
	Data_tp = Prep.Calc_SpatialAverage(Data_tp, Lat, Lon, 'SouthChina_Analysis')

	return Data_tp

def Get_Data_t2m():

	# Read data
	Data_t2m, _, Lat, Lon = PrepGD.Get_Data('t2m')

	# Calculate spatial average
	Data_t2m = Prep.Calc_SpatialAverage(Data_t2m, Lat, Lon, 'SouthChina_Analysis')

	return Data_t2m

def Get_Data_lwet():

	# Read data
	ncfile   = xr.open_dataset('../../GRACE/output/Output_Data/SeasonalCycle/SeasonalCycle.lwe_thickness.nc')
	Data_lwe = ncfile['lwe_thickness'].values
	Time     = pd.Series(ncfile['time'].values)

	# Get climatological seasonal cycle
	# Group the data with the same month and calculate the mean
	Data_SeasonalCycle = pd.DataFrame({'Data': Data_lwe, 'Time': Time}).set_index('Time')
	Data_SeasonalCycle = Data_SeasonalCycle.groupby(Data_SeasonalCycle.index.month)
	Data_Mean          = Data_SeasonalCycle.mean()['Data'].values
	Data_Std           = Data_SeasonalCycle.std()['Data'].values
	Data_n             = Data_SeasonalCycle.count()['Data'].values
	Data_CI            = [-1.96 * Data_Std / np.sqrt(Data_n), 1.96 * Data_Std / np.sqrt(Data_n)]

	# Extract 2022 data by selecting the Time with year 2022
	Data_2022 = Data_lwe[np.array([i_Time.year == 2022 for i_Time in Time]), ...]
	Data_2022 = np.append(Data_2022, np.nan)
	Data_2022 = Data_2022 - Data_Mean

	return Data_2022, Data_CI

if (__name__ == '__main__'):

	# Get data: lwe_thickness
	Data_lwet_2022, Data_lwet_CI = Get_Data_lwet()

	# Get data: swvl1, swvl2, swvl3, swvl4
	Data_swv, Time = Get_Data_swv()

	# Get data: tp
	Data_tp        = Get_Data_tp()

	# Get data: t2m
	Data_t2m       = Get_Data_t2m()
	
	# ==================================================
	# Get climatological seasonal cycle
	Data_swv_SeasonalCycle = Data_swv.reshape(-1, 12, Data_swv.shape[-1])
	Data_tp_SeasonalCycle  = Data_tp.reshape(-1, 12)
	Data_t2m_SeasonalCycle = Data_t2m.reshape(-1, 12)

	# Calculate the mean, standard deviation
	with warnings.catch_warnings():
		
		warnings.simplefilter('ignore', category=RuntimeWarning)

		Data_swv_Clim_Mean	   = np.nanmean(Data_swv_SeasonalCycle, axis=0)
		Data_swv_Clim_Std	   = np.nanstd(Data_swv_SeasonalCycle, axis=0)
		
		Data_tp_Clim_Mean	   = np.nanmean(Data_tp_SeasonalCycle, axis=0)
		Data_tp_Clim_Std	   = np.nanstd(Data_tp_SeasonalCycle, axis=0)
		Data_tp_Clim_n         = np.sum(~np.isnan(Data_tp_SeasonalCycle), axis=0)

		Data_t2m_Clim_Mean	   = np.nanmean(Data_t2m_SeasonalCycle, axis=0)
		Data_t2m_Clim_Std	   = np.nanstd(Data_t2m_SeasonalCycle, axis=0)
		Data_t2m_Clim_n        = np.sum(~np.isnan(Data_t2m_SeasonalCycle), axis=0)

	# Extract 2022 data by selecting the Time with year 2022
	Data_swv_2022          = Data_swv[np.array([i_Time.year == 2022 for i_Time in Time]), ...]
	Data_tp_2022           = Data_tp[np.array([i_Time.year == 2022 for i_Time in Time]), ...]
	Data_t2m_2022          = Data_t2m[np.array([i_Time.year == 2022 for i_Time in Time]), ...]

	# ==================================================
	# Plot anomaly profile
	Plot_Data = {\
		'Data_swv_Anomaly'        : (Data_swv_2022 - Data_swv_Clim_Mean), \
		'Data_swv_Significance'   : (Data_swv_2022 - Data_swv_Clim_Mean) / Data_swv_Clim_Std, \
		'Data_lwet_Anomaly'       : Data_lwet_2022, \
		'Data_lwet_CI'            : Data_lwet_CI, \
		'Data_tp_Anomaly'         : (Data_tp_2022 - Data_tp_Clim_Mean), \
		'Data_tp_CI'              : [-1.96 * Data_tp_Clim_Std / np.sqrt(Data_tp_Clim_n), 1.96 * Data_tp_Clim_Std / np.sqrt(Data_tp_Clim_n)], \
		'Data_t2m_Anomaly'        : (Data_t2m_2022 - Data_t2m_Clim_Mean), \
		'Data_t2m_CI'             : [-1.96 * Data_t2m_Clim_Std / np.sqrt(Data_t2m_Clim_n), 1.96 * Data_t2m_Clim_Std / np.sqrt(Data_t2m_Clim_n)], \
	}

	Plot_Config = {\
		'Plot_pcolormesh_vmin'    : -0.1, \
		'Plot_pcolormesh_vmax'    : 0.1, \
		'Plot_cmap'               : 'BrBG', \
	}

	# Plot map
	Plot_VProfile(Plot_Data, Plot_Config)