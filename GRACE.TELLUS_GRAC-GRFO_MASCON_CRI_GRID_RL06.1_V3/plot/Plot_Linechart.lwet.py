"""
Plot_Linechart.lwet.py
=============================
Plot the line chart of the liquid water equivalent thickness data.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import xarray as xr
import os

def Plot_Linechart(Plot_Data, Plot_Config):

	# Create figure
	fig, ax = plt.subplots(figsize=(12, 6), dpi=300)

	# Plot data
	ax.plot(Plot_Data['Time'], Plot_Data['Data'], color='black', linewidth=1.5, label='Data')
	ax.plot(Plot_Data['Time'], Plot_Data['Running_Mean'], color='red', linewidth=3, label='12 months RM')

	# Plot configuration
	ax.set_xlabel('Time')
	ax.set_xticks(['{}-01-31'.format(i) for i in range(2002, 2024, 3)])
	ax.set_xticklabels(['Jan {}'.format(i) for i in range(2002, 2024, 3)])
	ax.set_ylabel('Liquid Water Equivalent Thickness (cm)')
	ax.set_ylim([-8, 8])
	ax.grid()
	ax.legend(loc='upper left')

	# Save figure
	Output_Path = '../output/Output_Figure/Plot_Linechart.lwet/'
	Output_File = 'Plot_Linechart.lwet.{}.png'.format(Plot_Config['Region'])
	if not os.path.exists(Output_Path): os.makedirs(Output_Path)
	plt.savefig(Output_Path + Output_File, bbox_inches='tight')
	plt.close()

	return

def Get_Data(Region):

	ncFile = xr.open_dataset('../output/Output_Data/SptAvg/SptAvg.lwe_thickness.{}.nc'.format(Region))
	Data   = ncFile['lwe_thickness'].values
	Time   = ncFile['time'].values
	Time   = np.array([pd.to_datetime(str(i)[:10]) for i in Time])

	return pd.DataFrame({'Time': Time, 'Data': Data})

def DataPrep(df_LWET):

	# Set all days of Time to 01
	df_LWET['Time'] = df_LWET['Time'].apply(lambda x: x.replace(day=1))

	# Resample to monthly data
	df_LWET = df_LWET.set_index('Time').resample('M').mean().reset_index()

	# Add new column "Running_Mean": the running mean of the last 12 months based on datetime
	df_LWET['Running_Mean'] = df_LWET['Data'].rolling(12).mean()

	return df_LWET

if (__name__ == '__main__'):

	# Set region to plot
	Region = 'Taiwan_Analysis'

	# Get data
	df_LWET = Get_Data(Region)

	# Data preprocessing
	df_LWET = DataPrep(df_LWET)

	# Plot
	Plot_Data = {\
		'Time': df_LWET['Time'], \
		'Data': df_LWET['Data'], \
		'Running_Mean': df_LWET['Running_Mean'], \
	}

	Plot_Config = {\
		'Region': Region\
	}

	Plot_Linechart(Plot_Data, Plot_Config)