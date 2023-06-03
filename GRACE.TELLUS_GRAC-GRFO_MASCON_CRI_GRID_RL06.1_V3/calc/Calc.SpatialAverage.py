"""
Calc.SpatialAverage.py
===============================
Calculate spatial average of GRACE data and write to nc file
"""

import numpy as np
import pandas as pd
import xarray as xr
import os
import sys
sys.path.append('../')
import preprocessing.Preprocessing_Get_Data as PrepGD
import preprocessing.Preprocessing as Prep

if (__name__ == '__main__'):

	# Set the region to calculate spatial average
	Region = 'Taiwan_Analysis'

	# Get data
	Data, Time, Lat, Lon = PrepGD.Get_Data()
	
	# Calculate spatial average
	Data = Prep.Calc_SpatialAverage(Data, Lat, Lon, Region).squeeze()
	
	# Convert Time to YYYY-MM-DD format and convert to pandas datetime
	Time = np.array([pd.to_datetime(str(i_Time)[0:10]) for i_Time in Time])
	
	# ==================================================
	# Write spatial average to nc file by xarray
	Output_Path = '../output/Output_Data/SptAvg/'
	Output_File = 'SptAvg.lwe_thickness.{}.nc'.format(Region)
	if not os.path.exists(Output_Path): os.makedirs(Output_Path)

	# Create xarray dataset
	Data_SptAvg = xr.Dataset(\
		{\
			'lwe_thickness': (['time'], Data), \
		}, \
		coords = {\
			'time': (Time), \
		}, \
	)
	
	# Write to nc file
	Data_SptAvg.to_netcdf(Output_Path + Output_File)