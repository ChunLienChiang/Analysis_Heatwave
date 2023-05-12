"""
Plot_Linechart.SeasonalCycle.py
===============================
Plot climatological seasonal cycles and 2022 anomalies of lwe_thickness
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import xarray as xr
import os
import sys
sys.path.append('../')
import preprocessing.Preprocessing_Get_Data as PrepGD
import preprocessing.Preprocessing as Prep

def Plot_Linechart(Plot_Data, Plot_Config):

	# Create figure
	fig, ax = plt.subplots(figsize=(5, 5), dpi=300)

	# Plot: climatology and CI
	ax.plot(np.arange(1, 13), Plot_Data['Data_Mean'], color='k', linewidth=2.5, label='Climatology')
	ax.fill_between(np.arange(1, 13), Plot_Data['Data_CI'][0], Plot_Data['Data_CI'][1], color='k', alpha=0.2)

	# Plot: 2022
	ax.plot(np.arange(1, 13), Plot_Data['Data_2022'], color='r', linewidth=2.5, label='2022')

	# Plot configuration
	ax.set_xticks(np.arange(1, 13))
	ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct','Nov', 'Dec'])
	ax.set_xlabel('Month')
	ax.set_ylabel(r'{} (${}$)'.format(Plot_Config['Var'], Plot_Config['Var_Unit']))
	ax.legend()

	# Save figure
	Output_Path = '../output/Output_Figure/Plot_Linechart.SeasonalCycle/'
	Output_File = 'Plot_Linechart.SeasonalCycle.{Var}.png'.format(Var=Plot_Config['Var'])
	if not os.path.exists(Output_Path): os.makedirs(Output_Path)
	plt.tight_layout()
	plt.savefig(Output_Path + Output_File)
	plt.close('all')

	return

if (__name__ == '__main__'):

	# Get data
	Data, Time, Lat, Lon = PrepGD.Get_Data()
	
	# Calculate spatial average
	Data = Prep.Calc_SpatialAverage(Data, Lat, Lon, 'SouthChina_Analysis')
	
	# Convert Time to YYYY-MM-DD format and convert to pandas datetime
	Time = np.array([pd.to_datetime(str(i_Time)[0:10]) for i_Time in Time])
	
	# ==================================================
	# Get climatological seasonal cycle
	# Group the data with the same month and calculate the mean
	Data_SeasonalCycle = pd.DataFrame({'Data': Data, 'Time': Time}).set_index('Time')
	Data_SeasonalCycle = Data_SeasonalCycle.groupby(Data_SeasonalCycle.index.month)
	Data_Mean          = Data_SeasonalCycle.mean()['Data'].values
	Data_Std           = Data_SeasonalCycle.std()['Data'].values
	Data_n             = Data_SeasonalCycle.count()['Data'].values

	# Extract 2022 data by selecting the Time with year 2022
	Data_2022 = Data[np.array([i_Time.year == 2022 for i_Time in Time]), ...]

	# Because 2022-12 is not available, add a nan to the end of Data_2022
	Data_2022 = np.append(Data_2022, np.nan)

	# ==================================================
	# Plot climatological seasonal cycle
	Plot_Data = {\
		'Data_Mean': Data_Mean, \
		'Data_CI'  : [\
			Data_Mean - 1.96 * Data_Std / np.sqrt(Data_n), \
			Data_Mean + 1.96 * Data_Std / np.sqrt(Data_n), \
		], \
		'Data_2022': Data_2022, \
	}

	Plot_Config = {\
		'Var'     : 'Liquid water equivalent thickness', \
		'Var_Unit': 'm', \
	}

	Plot_Linechart(Plot_Data, Plot_Config)