# subroutine waterexchange

# ~ ~ ~ PURPOSE ~ ~ ~
# this subroutine reads the information about water exchange between different 
# sea zones from the corresponding csv file (water_exchange.csv) and reshape 
# them into time series

# ~ ~ ~ INCOMING VARIABLES ~ ~ ~
# name        |units         |definition
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# exchange_in |NA            |original data from csv file (water_exchange.csv)
# years       |none          |years of the model
# time_step   |min           |time step the model used
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

# ~ ~ ~ LOCAL DEFINITIONS ~ ~ ~
# name                   |units         |definition
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# edges                  |none          |contain edges for different zones
# water_exchange_matrix  |none          |water exchange matrix for each hour
# water_exchange_matrix_t|none          |water exchange matrix for 
#                                       |each time step
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ 

# ~ ~ ~ SUBROUTINES/FUNCTIONS CALLED ~ ~ ~
import numpy as np
import readcsv as rd
# ~ ~ ~ END SPECIFICATIONS ~ ~ ~

'''
Define edges between differnt zones
'''
edges = {'Edge1': ('Area1', 'Area2'),
         'Edge2': ('Area1', 'Area3'),
         'Edge3': ('Area1', 'Area4'),
         'Edge4': ('Area2', 'Area3'),
         'Edge5': ('Area3', 'Area4'),
         'Edge6': ('Area4', 'Area5'), 
         'Edge7': ('Area5', 'OuterSea'),
         'Edge8': ('Area2', 'Area1'),
         'Edge9': ('Area3', 'Area1'),
         'Edge10': ('Area4', 'Area1'),
         'Edge11': ('Area3', 'Area2'),
         'Edge12': ('Area4', 'Area3'),
         'Edge13': ('Area5', 'Area4'),
         'Edge14': ('OuterSea', 'Area5')}

'''
Calculate the water exchange matrix
'''
num_time_points = len(rd.exchange_in)  # set time series
water_exchange_matrix = np.zeros((len(rd.sea_areas), len(rd.sea_areas),\
                                num_time_points)) 

water_exchange_values = {
    'Edge1': rd.exchange_in['Edge 1'],
    'Edge2': rd.exchange_in['Edge 2'],
    'Edge3': rd.exchange_in['Edge 3'],
    'Edge4': rd.exchange_in['Edge 4'],
    'Edge5': rd.exchange_in['Edge 5'],
    'Edge6': rd.exchange_in['Edge 6'],
    'Edge7': rd.exchange_in['Edge 7'],
    'Edge8': rd.exchange_in['Edge 8'],
    'Edge9': rd.exchange_in['Edge 9'],
    'Edge10': rd.exchange_in['Edge 10'],
    'Edge11': rd.exchange_in['Edge 11'],
    'Edge12': rd.exchange_in['Edge 12'],
    'Edge13': rd.exchange_in['Edge 13'],
    'Edge14': rd.exchange_in['Edge 14'],
}

for edge, (area1, area2) in edges.items():
    index1 = rd.sea_areas.index(area1)
    index2 = rd.sea_areas.index(area2)
    water_exchange_matrix[index1, index2, :] =\
    np.array(water_exchange_values[edge])

# calculate the data on the diagonal
for t in range(num_time_points):
    for i in range(6):
        water_exchange_matrix[i, i, t] =\
        np.sum(water_exchange_matrix[i, :, t])*-1      

# considering time step needed for the model
num_steps = int((num_time_points-1)/2)
water_exchange_matrix_t = np.zeros((len(rd.sea_areas), len(rd.sea_areas),\
                                  num_steps))

for i in range(num_steps):
    start_idx = int(i * (rd.time_step / 120))
    end_idx = int((i + 1) * (rd.time_step / 120))
    water_exchange_matrix_t[:, :, i] =\
    np.sum(water_exchange_matrix[:, :, start_idx:end_idx], axis=2)

'''
Get water exchange matrix for a given time
'''
def func_water_exchange(t):
    if t%rd.time_step == 0:
        matrix = water_exchange_matrix_t[:,:,int(t/rd.time_step)]
        return matrix
    else:
        print ('Error: wrong time input')
        return None
