# subroutine readcsv

# ~ ~ ~ PURPOSE ~ ~ ~
# this subroutine reads the information from the csv files, does some 
# preliminary data processing and define some global variables for the model

# ~ ~ ~ OUTGOING VARIABLES ~ ~ ~
# name        |units         |definition
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# bio_data    |NA            |original data from csv file (bio_coe.csv)
# temp_data   |NA            |original data from csv file (envi_T_min.csv)
# river_in    |NA            |original data from csv file 
#                            |(box_source_river.csv)
# sea_in      |NA            |original data from csv file (sea.csv)
# exchange_in |NA            |original data from csv file (water_exchange.csv)
# in_num_agr  |NA            |reclassified data for fish, shellfish and seaweed
# seaweed_data|NA            |original data from csv file (box_seaweed.csv)
# radiation   |W/m^2         |original data from csv file (envi_radiation.csv)
# box_h       |m             |original data from csv file (box_h.csv)
# box_a       |m^2           |original data from csv file (box_infor.csv)
# box_v       |m^3           |original data from csv file (box_vol.csv)
# source_point|NA            |original data from csv file 
#                            |(box_source_points.csv)
# source_pond |NA            |original data from csv file 
#                            |(box_source_ponds.csv)
# start_n     |NA            |original data from csv file (box_nutrient.csv)
# d_to_min    |min/d         |number of minutes in a day
# years       |none          |years of the model
# sea_areas   |none          |5 different sea zones and the outer sea
# time_step   |min           |time step the model used
# time_start  |min           |the time the model starts (0)
# time_end    |min           |the time the model lasts
# num_step    |NA            |number of time steps 
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

# ~ ~ ~ LOCAL DEFINITIONS ~ ~ ~
# name        |units         |definition
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# agri_data   |NA            |original data from csv file 
#                            |(box_argriculture.csv)
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~  

# ~ ~ ~ SUBROUTINES/FUNCTIONS CALLED ~ ~ ~
import numpy as np
import pandas as pd
# ~ ~ ~ END SPECIFICATIONS ~ ~ ~

'''
Import infornation from csv files
'''
bio_data = np.genfromtxt(r'.\original_data\bio_coe.csv', delimiter=',',\
                         skip_header=True, usecols=(1,))
temp_data = np.genfromtxt(r'.\original_data\envi_T.csv', delimiter=',',\
                          skip_header=True, usecols=range(1,6))
river_in = np.genfromtxt(r'.\original_data\box_source_river.csv',\
                         delimiter=',', skip_header=True,\
                         usecols=range(2, 7))
sea_in = pd.read_csv(r'.\original_data\sea.csv')
exchange_in = pd.read_csv(r'.\original_data\water_exchange.csv',\
                               index_col=[0])
agri_data = pd.read_csv(r'.\original_data\box_argriculture.csv')
seaweed_data = pd.read_csv(r'.\original_data\box_seaweed.csv')
radiation = np.genfromtxt(r'.\original_data\envi_radiation.csv',\
                          delimiter=',', skip_header=True, usecols=(1,))
box_h = np.genfromtxt(r'.\original_data\box_h.csv', delimiter=',',\
                      skip_header=True, usecols=range(1, 6))
box_a = np.genfromtxt(r'.\original_data\box_infor.csv', delimiter=',',\
                      skip_header=True, usecols=range(2,))  
box_v = np.genfromtxt(r'.\original_data\box_vol.csv', delimiter=',',\
                      skip_header=True, usecols=range(1, 6))
source_point = pd.read_csv(r'.\original_data\box_source_points.csv',\
                           usecols=range(1,4)).T
source_pond = pd.read_csv(r'.\original_data\box_source_ponds.csv',\
                          usecols=range(1,4)).T
source_sgd = pd.read_csv(r'.\original_data\box_source_sgd.csv',\
                          usecols=range(1,4)).T
source_atmo = pd.read_csv(r'.\original_data\box_source_atmo.csv',\
                              usecols=range(1,4)).T
start_n = pd.read_csv(r'.\original_data\box_nutrient.csv',\
                          usecols=range(1,4)).T

'''
Define global variables
'''
d_to_min = 24*60
years = [2016, 2017, 2018, 2019, 2020] # year needed
sea_areas = ['Area1', 'Area2', 'Area3', 'Area4', 'Area5', 'OuterSea']
time_step = 240
time_start = 0
time_end = (365*3+366*2)*24*60-time_step
num_step = int(time_end/time_step)+1
# start and end time of shellfish, fish and seaweed
## form: [month, day, hour, minute, year] 
## year = 0 if start end at the same year, year = 1 if not
t_shellfish_start = [6, 30, 0, 0, 0] 
t_shellfish_end = [12, 31, 0, 0, 0]
t_fish_start = [6, 1, 0, 0, 0]
t_fish_end = [4, 30, 0, 0, 1]
t_seaweed_start = [1, 1, 0, 0, 0]
t_seaweed_end = [6, 30, 0, 0, 0]

'''
Transform the agriculture data into dictionary
'''
in_num_agr = {}
years = agri_data['Year'].unique()
areas = agri_data['num'].unique()

for col in agri_data.columns[1:4]:
    type_df = pd.DataFrame(index=years, columns=areas)  
    for year in years:
        for area in areas:
            quantity = agri_data[(agri_data['Year'] == year)\
                                & (agri_data['num'] == area)][col].values
            type_df.loc[year, area] = quantity[0] if len(quantity) > 0 else 0
    in_num_agr[col] = type_df
    
