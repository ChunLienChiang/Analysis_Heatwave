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
	Data_Path = '/work5/TELLUS_GRFO_L3_CSR_RL06.1_LND_v04/'

	# Get data and time from all nc files
	Data = []
	Time = []

	File_List = [i for i in os.listdir(Data_Path) if i.endswith('.nc')]
	File_List = sorted(File_List, key=lambda x: int(x[6:12]))
	
	for i_File in File_List:
		
		Data.append(xr.open_dataset(Data_Path + i_File)[Var].values)
		Time.append(xr.open_dataset(Data_Path + i_File)['time'].values)

	Data = np.concatenate(Data, axis=0)
	Time = np.concatenate(Time, axis=0)

	# Get latitude and longitude from GRD-3_2022305-2022334_GRFO_UTCSR_BA01_0601_LND_v04.nc
	Lat  = xr.open_dataset(Data_Path + 'GRD-3_2022305-2022334_GRFO_UTCSR_BA01_0601_LND_v04.nc')['lat'].values
	Lon  = xr.open_dataset(Data_Path + 'GRD-3_2022305-2022334_GRFO_UTCSR_BA01_0601_LND_v04.nc')['lon'].values

	# Mask fill values to nan
	Data = np.ma.masked_where(Data == -99999., Data)

	return Data, Time, Lat, Lon

if (__name__ == '__main__'):

	# Get data
	Data, Time, Lat, Lon = Get_Data('lwe_thickness')