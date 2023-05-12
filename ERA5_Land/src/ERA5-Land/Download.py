import cdsapi
import os

c = cdsapi.Client()

Var_FullName_List = [\
	'total_precipitation', \
	'skin_reservoir_content', \
	'volumetric_soil_water_layer_1', \
	'volumetric_soil_water_layer_2', \
	'volumetric_soil_water_layer_3', \
	'volumetric_soil_water_layer_4', \
	'2m_temperature', \
	'skin_temperature', \
	'total_evaporation', \
]
Var_List = [\
	'tp', \
	'src', \
	'swvl1', \
	'swvl2', \
	'swvl3', \
	'swvl4', \
	'2t', \
	'skt', \
	'e', \
]

for i_Var_FullName, i_Var in zip(Var_FullName_List, Var_List):

	# Print message
	print('Download {Var}'.format(Var=i_Var))

	# Skip if file exists
	if (os.path.exists('ERA5-Land.{Var}.nc'.format(Var=i_Var))): continue

	c.retrieve(
		'reanalysis-era5-land-monthly-means',
		{
			'product_type': 'monthly_averaged_reanalysis',
			'variable': [i_Var_FullName],
			'year': [
				'1992', '1993', '1994',
				'1995', '1996', '1997',
				'1998', '1999', '2000',
				'2001', '2002', '2003',
				'2004', '2005', '2006',
				'2007', '2008', '2009',
				'2010', '2011', '2012',
				'2013', '2014', '2015',
				'2016', '2017', '2018',
				'2019', '2020', '2021',
				'2022'
			],
			'month': [
				'01', '02', '03',
				'04', '05', '06',
				'07', '08', '09',
				'10', '11', '12',
			],
			'time': '00:00',
			'format': 'netcdf',
		},
		'ERA5-Land.{Var}.nc'.format(Var=i_Var))