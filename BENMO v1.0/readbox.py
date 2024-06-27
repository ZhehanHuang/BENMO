# subroutine readbox

# ~ ~ ~ PURPOSE ~ ~ ~
# this subroutine reads the phycical information about different zones from 
# the corresponding csv files (box_h.csv, box_infor.csv and box_vol.csv) and 
# reshape them into time series

# ~ ~ ~ INCOMING VARIABLES ~ ~ ~
# name        |units         |definition
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# box_h       |m             |original data from csv file (box_h.csv)
# box_a       |m^2           |original data from csv file (box_infor.csv)
# box_v       |m^3           |original data from csv file (box_vol.csv)
# years       |none          |years of the model
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

# ~ ~ ~ OUTGOING VARIABLES ~ ~ ~
# name        |units         |definition
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# area        |m^2           |area size of different zones
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

# ~ ~ ~ LOCAL DEFINITIONS ~ ~ ~
# name        |units         |definition
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# height      |m             |height of different zones
# volume      |m^3           |volume of different zones
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ 

# ~ ~ ~ SUBROUTINES/FUNCTIONS CALLED ~ ~ ~
import pandas as pd
import numpy as np
import readcsv as rd
import waterexchange as we
# ~ ~ ~ END SPECIFICATIONS ~ ~ ~

'''
Reshape physical data of different zones into time series
'''
start_date = str(rd.years[0]) + "-01-01"
end_date = str(rd.years[-1]) + "-12-31 23:00"
time_index = pd.date_range(start=start_date, end=end_date, freq="4H")

area = rd.box_a[:,1]

water_volume = we.water_exchange_matrix_t.sum(axis = 0).T
water_volume = np.delete(water_volume, 5, axis=1)
water_volume_real = water_volume.copy()
water_height_real = water_volume.copy()

# water_volume_1 =  [1690337034, 839938725.9, 1621279346, 4290624552, 2293959206]
water_volume_1 =  [1481335657, 715148772.6, 1447994746, 4052718152, 2182479206]
for i in range(len(time_index)):
    water_volume_1 = water_volume_1 + water_volume[i,:]
    water_volume_real[i,:] = water_volume_1
    water_height_real[i,:] = water_volume_1/area

# height = pd.DataFrame(data=water_height_real, index=time_index)
# volume = pd.DataFrame(data=water_volume_real, index=time_index)
# volume[5] = 1000000000

'''
Get physical data from a given time
'''
# def get_h(t): 
#     target_date = height.index[0] + pd.Timedelta(minutes=t)
#     h_t = height.loc[target_date]
#     return h_t

# def get_v(t): 
#     target_date = volume.index[0] + pd.Timedelta(minutes=t)
#     v_t = volume.loc[target_date]
#     return v_t


height = rd.box_h 
volume = rd.box_v
def get_h(t): 
    h_t = height[int(t/rd.time_step),:]
    return h_t

def get_v(t): 
    v_t = volume[int(t/rd.time_step),:]
    return v_t

