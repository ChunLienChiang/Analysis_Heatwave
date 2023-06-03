import numpy as np

def Get_Range(Range):

	if (Range == 'Global_Analysis'):

		return -90, 90, 0, 360
	
	elif (Range == 'CentralChina_Analysis'):

		return 28, 34, 106, 118
	
	elif (Range == 'SouthChina_Analysis'):

		return 20, 32, 106, 120
	
	elif (Range == 'EastAsia_Analysis'):

		return 17, 40, 90, 133
	
	elif (Range == 'EastAsia_Analysis_Extended'):

		return 14, 43, 87, 136
	
	elif (Range == 'Taiwan_Analysis'):

		return 21.8, 25.3, 119.8, 122.1
	
	else:

		raise ValueError('Error in Get_Range: wrong range name.')
	
def Crop_Range(Data, Lat, Lon, Range, Range_Original='Global_Analysis'):

	"""
	Crop data to the given range
	==================================================
	Input:
		Data: numpy array of data. The last two dimensions should be latitude and longitude, respectively
		Lat: numpy array of latitude
		Lon: numpy array of longitude
		Range: [lat_min, lat_max, lon_min, lon_max] or string of region name
	Output:
		Data_Crop: numpy array of cropped data
		Lat_Crop: numpy array of cropped latitude
		Lon_Crop: numpy array of cropped longitude
	"""

	if (Lat[0] > Lat[-1]):
		
		Lat = Lat[::-1]
		Data = Data[..., ::-1, :]
	
	# ==================================================
	# Get range boundaries if the range is a string
	if (isinstance(Range, str)): Range = Get_Range(Range)
	Lat_Min, Lat_Max, Lon_Min, Lon_Max = Range

	# ==================================================
	# Crop latitude and longitude
	Lat_Crop, Lon_Crop = Crop_Lat_Lon(Lat, Lon, Range)

	# Crop data
	if (tuple(Data.shape[-2:]) != tuple([Lat.shape[0], Lon.shape[0]])):

		raise ValueError('Error in Crop_Range: given array does not meet original range.')

	Arg_Lon_Min = np.argmin(np.abs(Lon-Lon_Min))
	Arg_Lon_Max = np.argmin(np.abs(Lon-Lon_Max)) + 1
	Arg_Lat_Min = np.argmin(np.abs(Lat-Lat_Min))
	Arg_Lat_Max = np.argmin(np.abs(Lat-Lat_Max)) + 1

	if (Range_Original != 'Global_Analysis'):

		Lon_Min_Original, Lon_Max_Original, Lat_Min_Original, Lat_Max_Original = Get_Range(Range_Original)
		Arg_Lon_Min_Original = np.argmin(np.abs(Lon-Lon_Min_Original))
		Arg_Lon_Max_Original = np.argmin(np.abs(Lon-Lon_Max_Original)) + 1
		Arg_Lat_Min_Original = np.argmin(np.abs(Lat-Lat_Min_Original))
		Arg_Lat_Max_Original = np.argmin(np.abs(Lat-Lat_Max_Original)) + 1

		Arg_Lon_Min          = Arg_Lon_Min - Arg_Lon_Min_Original
		Arg_Lon_Max          = Arg_Lon_Max - Arg_Lon_Max_Original
		Arg_Lat_Min          = Arg_Lat_Min - Arg_Lat_Min_Original
		Arg_Lat_Max          = Arg_Lat_Max - Arg_Lat_Max_Original
		
	if ((Arg_Lat_Max in Lat[[0, -1]]) and (Arg_Lon_Max in Lon[[0, -1]])):

		Data_Crop = Data[..., Arg_Lat_Min:, Arg_Lon_Min:]
	
	elif (Arg_Lat_Max in Lat[[0, -1]]) and ~(Arg_Lon_Max in Lon[[0, -1]]):

		Data_Crop = Data[..., Arg_Lat_Min:, Arg_Lon_Min:Arg_Lon_Max]
	
	elif ~(Arg_Lat_Max in Lat[[0, -1]]) and (Arg_Lon_Max in Lon[[0, -1]]):

		Data_Crop = Data[..., Arg_Lat_Min:Arg_Lat_Max, Arg_Lon_Min:]
	
	else:

		Data_Crop = Data[..., Arg_Lat_Min:Arg_Lat_Max, Arg_Lon_Min:Arg_Lon_Max]

	# ==================================================
	if (Lat[0] > Lat[-1]):
		
		Lat_Crop = Lat_Crop[::-1]
		Data_Crop = Data_Crop[..., ::-1, :]
	
	return Data_Crop, Lat_Crop, Lon_Crop

def Crop_Lat_Lon(Lat, Lon, Range):

	"""
	Crop the latitude and longitude data to fit the given range
	==========================
	Input:
		Lat: numpy array of latitude. The order should be from south to north
		Lon: numpy array of longitude
		Range: [lat_min, lat_max, lon_min, lon_max] or string of region name
	Output:
		Lat_Crop: numpy array of cropped latitude
		Lon_Crop: numpy array of cropped longitude
	==========================
	"""

	# ==================================================
	# Get range boundaries if the range is a string
	if (isinstance(Range, str)): Range = Get_Range(Range)
	Lat_Min, Lat_Max, Lon_Min, Lon_Max = Range

	# ==================================================
	Arg_Lon_Min = np.argmin(np.abs(Lon-Lon_Min))
	Arg_Lon_Max = np.argmin(np.abs(Lon-Lon_Max))
	Arg_Lat_Min = np.argmin(np.abs(Lat-Lat_Min))
	Arg_Lat_Max = np.argmin(np.abs(Lat-Lat_Max))

	Lat_Crop = Lat[Arg_Lat_Min:Arg_Lat_Max+1]
	Lon_Crop = Lon[Arg_Lon_Min:Arg_Lon_Max+1]

	return Lat_Crop, Lon_Crop

def Calc_SpatialAverage(Data, Lat, Lon, Range, Optimization=True):

	"""
	Calculate spatial average considering range and latitude weighting
	==================================================
	Input:
		Data: numpy array of data
		Lat: numpy array of latitude
		Lon: numpy array of longitude
		Range: [lat_min, lat_max, lon_min, lon_max] or string of region name
	Output:
		Data_Avg: numpy array of spatial average
	"""

	# ==================================================
	# Mask: range
	# Get range boundaries if the range is a string
	if (isinstance(Range, str)): Range = Get_Range(Range)

	# Create a numpy array and set the range inside the rectangle range to 1, and outside to 0
	Mask_Range = np.zeros((len(Lat), len(Lon)))
	Mask_Range[(Lat[:, None] >= Range[0]) & (Lat[:, None] <= Range[1]) & (Lon[None, :] >= Range[2]) & (Lon[None, :] <= Range[3])] = 1

	# Mask: latitude weighting
	# Create a numpy array and set the latitude weighting to the cosine of latitude and broadcast to the last two dimensions of data
	Mask_Lat = np.cos(np.deg2rad(Lat))
	Mask_Lat = np.broadcast_to(Mask_Lat[:, np.newaxis], (len(Lat), len(Lon)))

	# Mask: land region
	# Create a numpy array and set the values to 1 where the data is not nan, and 0 where the data is nan
	Mask_Land = np.where(np.isnan(Data), 0, 1)

	# ==================================================
	# Calculate overall mask (by multiplying all masks)
	Mask = Mask_Range * Mask_Lat * Mask_Land

	if (Optimization):

		Mask = Crop_Range(Mask, Lat, Lon, Range)[0]
		Data = Crop_Range(Data, Lat, Lon, Range)[0]

	# Calculate spatial average ignoring nan values
	Data_Avg = np.ma.average(np.ma.MaskedArray(Data, mask=np.isnan(Data)), weights=Mask, axis=(-2, -1))

	return Data_Avg