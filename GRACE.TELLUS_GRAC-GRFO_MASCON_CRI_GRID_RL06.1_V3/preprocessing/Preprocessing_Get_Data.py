import numpy as np
import pandas as pd
import xarray as xr
import os

def Get_Data(Var='lwe_thickness'):

	"""
	Get data by xarray and convert to numpy array
	==================================================
	Input:
		Var: variable name. Default: 'lwe_thickness'
	Output:
		Data: numpy array of data
		Time: numpy array of time
		Lat: numpy array of latitude
		Lon: numpy array of longitude
	"""

	# Set data path
	Data_Path = '/work5/TELLUS_GRAC-GRFO_MASCON_CRI_GRID_RL06.1_V3/'
	Data_File = 'GRCTellus.JPL.200204_202303.GLO.RL06.1M.MSCNv03CRI.nc'

	# Get data and time from all nc files
	Data = xr.open_dataset(Data_Path + Data_File)[Var].values
	Lat  = xr.open_dataset(Data_Path + Data_File)['lat'].values
	Lon  = xr.open_dataset(Data_Path + Data_File)['lon'].values
	Time = xr.open_dataset(Data_Path + Data_File)['time'].values

	# Mask fill values to nan
	Data = np.ma.masked_where(Data == -99999., Data)

	return Data, Time, Lat, Lon