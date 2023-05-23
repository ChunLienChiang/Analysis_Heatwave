"""
Plot_Linechart.SeasonalCycle.py
===============================
Plot climatological seasonal cycles and 2022 anomalies of:
1. precipitation
2. Skin reservoir content
3. Volumetric soil waters
4. 2m temperature
5. Skin temperature
6. Evaporation
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
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

def Get_Var_Unit(Var):

	# Set unit
	if (Var == 'tp'):

		Var_Unit = 'mm/day'

	elif (Var in ['src', 'e']):

		Var_Unit = 'm of water equivalent'

	elif (Var in ['swvl1', 'swvl2', 'swvl3', 'swvl4']):

		Var_Unit = 'm3/m3'

	elif (Var in ['t2m', 'skt']):

		Var_Unit = 'K'

	else:

		raise None

	return Var_Unit

if (__name__ == '__main__'):
	
	VarName_File_List   = ['t2m', 'skt', 'e', 'tp', 'src', 'swvl1', 'swvl2', 'swvl3', 'swvl4']

	for i_Var in VarName_File_List:

		# Print message
		print('Plotting {Var}...'.format(Var=i_Var))

		# Get data
		Data, Time, Lat, Lon = PrepGD.Get_Data(i_Var)

		# Calculate spatial average
		Data = Prep.Calc_SpatialAverage(Data, Lat, Lon, 'SouthChina_Analysis')
		
		# Convert Time to YYYY-MM-DD format and convert to pandas datetime
		Time = np.array([pd.to_datetime(str(i_Time)[0:10]) for i_Time in Time])
		
		# ==================================================
		# Get climatological seasonal cycle
		Data_SeasonalCycle = Data.reshape(-1, 12)

		# Extract 2022 data by selecting the Time with year 2022
		Data_2022 = Data[np.array([i_Time.year == 2022 for i_Time in Time]), ...]

		# ==================================================
		# Plot climatological seasonal cycle
		Plot_Data = {\
			'Data_Mean': np.nanmean(Data_SeasonalCycle, axis=0), \
			'Data_CI'  : [\
				np.nanmean(Data_SeasonalCycle, axis=0) - 1.96 * np.nanstd(Data_SeasonalCycle, axis=0) / np.sqrt(Data_SeasonalCycle.shape[0]), \
				np.nanmean(Data_SeasonalCycle, axis=0) + 1.96 * np.nanstd(Data_SeasonalCycle, axis=0) / np.sqrt(Data_SeasonalCycle.shape[0]), \
			], \
			'Data_2022': Data_2022, \
		}

		Plot_Config = {\
			'Var': i_Var, \
			'Var_Unit': Get_Var_Unit(i_Var), \
		}

		Plot_Linechart(Plot_Data, Plot_Config)