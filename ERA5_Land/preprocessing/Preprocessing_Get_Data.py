import numpy as np
import pandas as pd
import xarray as xr

def Get_Data(Var):

	"""
	Get data by xarray and convert to numpy array
	==================================================
	Input:
		Var: variable name
	Output:
		Data: numpy array of data
		Time: numpy array of time
		Lat: numpy array of latitude
		Lon: numpy array of longitude
	"""

	# Get data
	Data = xr.open_dataset('../src/ERA5-Land/ERA5-Land.{Var}.nc'.format(Var=Var))[Var].values

	# Get time, latitude and longitude
	Time = xr.open_dataset('../src/ERA5-Land/ERA5-Land.{Var}.nc'.format(Var=Var))['time'].values
	Lat  = xr.open_dataset('../src/ERA5-Land/ERA5-Land.{Var}.nc'.format(Var=Var))['latitude'].values
	Lon  = xr.open_dataset('../src/ERA5-Land/ERA5-Land.{Var}.nc'.format(Var=Var))['longitude'].values

	# Convert to numpy array
	Data = np.array(Data)

	# Mask fill values to nan
	Data = np.ma.masked_where(Data == 1e+20, Data)

	# Convert units
	if (Var == 'tp'):

		# Convert m/month to mm/day (considergin the number of days in each month)
		# Get the number of days in each month
		Num_Days = np.array([pd.to_datetime(t).daysinmonth for t in Time])
		
		# Convert units
		Data = Data * 1000 / Num_Days[:, None, None]
	
	return Data, Time, Lat, Lon

if (__name__ == '__main__'):

	# Get data
	Data, Time, Lat, Lon = Get_Data('tp')