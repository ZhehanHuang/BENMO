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
from scipy.optimize import curve_fit
import readcsv as rd
# ~ ~ ~ END SPECIFICATIONS ~ ~ ~

# Reset index and convert 'time' to datetime
rd.sea_in = rd.sea_in.reset_index()
rd.sea_in['time'] = pd.to_datetime(rd.sea_in['time'])
rd.sea_in.set_index('time', inplace=True)

# Create an array of x values
x = np.arange(len(rd.sea_in))

# Original data
y_nh4 = rd.sea_in['nh4'].values
y_no3 = rd.sea_in['no3'].values

# Calculate the number of days in the data
num_days = (rd.sea_in.index.max() - rd.sea_in.index.min()).days + 1

# Generate x values for the new data
x_new = np.linspace(0, len(rd.sea_in) - 1, num=num_days)

# Define the dual sinusoidal function
def dual_sin_function(x, amplitude1, frequency1, phase1, amplitude2, frequency2, phase2, offset):
    frequency1 = 1/5
    frequency2 = 1/3.8
    term1 = amplitude1 * np.sin(2 * np.pi * frequency1 * x + phase1)
    term2 = amplitude2 * np.sin(2 * np.pi * frequency2 * x + phase2)
    return term1 + term2 + offset

# Provide refined initial parameter guesses
initial_guess_nh4 = [np.max(y_nh4), 1/5, 0, np.max(y_nh4)/2, 2/365, np.pi, np.min(y_nh4)]
initial_guess_no3 = [np.max(y_no3), 1/3, 0, np.max(y_no3)/2, 2/365, np.pi, np.min(y_no3)]

# Fit the dual sinusoidal function to the data with refined initial guesses
params_nh4, _ = curve_fit(dual_sin_function, x, y_nh4, p0=initial_guess_nh4, maxfev=5000)
params_no3, _ = curve_fit(dual_sin_function, x, y_no3, p0=initial_guess_no3, maxfev=5000)

# Generate the new y values using the fitted dual sinusoidal functions
y_nh4_new = dual_sin_function(x_new, *params_nh4)
y_no3_new = dual_sin_function(x_new, *params_no3)

# Prevent the new data from being less than zero
y_nh4_new = np.clip(y_nh4_new, 0.0001, None)
y_no3_new = np.clip(y_no3_new, 0.0001, None)

# Create new dates for the DataFrame
new_dates = pd.date_range(start=rd.sea_in.index.min(),
                          end=rd.sea_in.index.min() +
                          pd.Timedelta(days=len(x_new) - 1), freq='D')

# Create a new DataFrame with the filled values
sea_in_new = pd.DataFrame({'nh4': y_nh4_new, 'no3': y_no3_new}, index=new_dates)

# Filter the new DataFrame to match the original date range
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
plt.title('Trigonometric function fitting of $NH_4$ and $NO_3$')
plt.legend(bbox_to_anchor=(1.05, 0), loc=3, borderaxespad=0)

# Display the plot
plt.savefig('外海输入.png',dpi=1000, bbox_inches='tight')
plt.show()
