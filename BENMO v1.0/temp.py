# subroutine temp

# ~ ~ ~ PURPOSE ~ ~ ~
# this subroutine reads the temperature information from the corresponding 
# csv file (envi_T_min.csv) and reshape them into time series

# ~ ~ ~ INCOMING VARIABLES ~ ~ ~
# name        |units         |definition
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# temp_data   |NA            |original data from csv file (envi_T_min.csv)
# years       |none          |years of the model
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

# ~ ~ ~ LOCAL DEFINITIONS ~ ~ ~
# name        |units         |definition
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# temp_lunar  |centigrade(°C)|water temperature time series data for 
#                            |lunar years
# temp_normal |centigrade(°C)|water temperature time series data for 
#                            |normal years
# temp_combine|centigrade(°C)|water temperature time series data for all the 
#                            |years of the model
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ 

# ~ ~ ~ SUBROUTINES/FUNCTIONS CALLED ~ ~ ~
import numpy as np
import pandas as pd
import readcsv as rd
# ~ ~ ~ END SPECIFICATIONS ~ ~ ~

'''
Reshape temperature time series data: from 10 minutes to 1h
'''
temp_reshape = rd.temp_data[:52705//6*6].reshape(-1, 6)
resampled_temp = temp_reshape.mean(axis=1) # reshape the data into per hour
temp_lunar = resampled_temp
temp_normal = resampled_temp[:8760]

'''
Link the temperature to time series index
'''
temp_combine = []
for year in rd.years:
    if year%4 == 0:
        temp_combine.append(temp_lunar)
    else:
        temp_combine.append(temp_normal)
temp_combine = np.concatenate(temp_combine, axis=0)
start_date = str(rd.years[0]) + "-01-01"
end_date = str(rd.years[-1]) + "-12-31 23:00"
time_index = pd.date_range(start=start_date, end=end_date, freq="H")
temp = pd.DataFrame(data={"temperature": temp_combine}, index=time_index)

'''
Get temperature from a given time
'''
def get_temp_min(t): # for time step less than an hour
    target_date = temp.index[0] + pd.Timedelta(minutes=t)
    t_k = 273 + temp.resample('T').interpolate().loc[target_date, 'temperature']
    return t_k

def get_temp_h(t): # for time step as hours
    target_date = temp.index[0] + pd.Timedelta(minutes=t)
    t_k = 273 + temp.loc[target_date, 'temperature']
    return t_k
