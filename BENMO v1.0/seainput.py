# subroutine seainput

# ~ ~ ~ PURPOSE ~ ~ ~
# this subroutine reads the information about the nitrients input from sea 
# from the corresponding csv file (sea.csv) and reshape them into time series

# ~ ~ ~ INCOMING VARIABLES ~ ~ ~
# name        |units         |definition
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# sea_in      |NA            |original data from csv file (sea.csv)
# years       |none          |years of the model
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

# ~ ~ ~ LOCAL DEFINITIONS ~ ~ ~
# name        |units         |definition
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# y_nh4       |none          |original data of NH4 in 5 years
# y_no3       |none          |original data of NO3 in 5 years
# y_nh4_new   |none          |data of NH4 after cubic spline interpolation
# y_no3_new   |none          |data of NO3 after cubic spline interpolation
# sea_in_new  |none          |contain time series data for NH4 and NO3 input 
#                            |from seas after cubic spline interpolation
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ 

# ~ ~ ~ SUBROUTINES/FUNCTIONS CALLED ~ ~ ~
import pandas as pd
import numpy as np
from scipy.interpolate import interp1d
import readcsv as rd
# ~ ~ ~ END SPECIFICATIONS ~ ~ ~

'''
Reshape sea input to different types as time series
'''
rd.sea_in = rd.sea_in.reset_index()
rd.sea_in['time'] = pd.to_datetime(rd.sea_in['time'])
rd.sea_in.set_index('time', inplace=True)

'''
Cubic spline interpolation of nh4 and no3
'''
x = np.arange(len(rd.sea_in))

y_nh4 = rd.sea_in['nh4'].values
f_nh4 = interp1d(x, y_nh4, kind='cubic')

y_no3 = rd.sea_in['no3'].values
f_no3 = interp1d(x, y_no3, kind='cubic')

num_days = (rd.sea_in.index.max() - rd.sea_in.index.min()).days + 1

x_new = np.linspace(0, len(rd.sea_in)-1, num=num_days)
y_nh4_new = f_nh4(x_new)
y_no3_new = f_no3(x_new)

# prevent the new dat from less than zero
y_nh4_new = np.clip(y_nh4_new, 0.0001, None)
y_no3_new = np.clip(y_no3_new, 0.0001, None)

new_dates = pd.date_range(start=rd.sea_in.index.min(), \
                         end=rd.sea_in.index.min() +\
                         pd.Timedelta(days=len(x_new)-1), freq='D')

sea_in_new = pd.DataFrame({'nh4': y_nh4_new, 'no3': y_no3_new},index=new_dates)
sea_in_new = sea_in_new[f'{rd.years[0]}-01-01':f'{rd.years[-1]}-12-31']

'''
Get sea input for a given time
'''
def source_sea(t,tp):
    target_date = (sea_in_new.index.min() + pd.Timedelta(minutes=t)).floor('D')
    sea = sea_in_new.loc[target_date, f'{tp}']
    return sea*1000


# Show the curve
import matplotlib.pyplot as plt

# Plot original scattered points
plt.scatter(rd.sea_in.index, rd.sea_in['nh4'], label='Original nh4', marker='o')
plt.scatter(rd.sea_in.index, rd.sea_in['no3'], label='Original no3', marker='o')

# Plot cubic spline interpolation curves
plt.plot(new_dates, y_nh4_new, label='Interpolated nh4')
plt.plot(new_dates, y_no3_new, label='Interpolated no3')

# Set labels and title
plt.xlabel('Time')
plt.ylabel('Concentration')
plt.title('Cubic Spline Interpolation of nh4 and no3')
plt.legend()

# Display the plot
plt.show()
