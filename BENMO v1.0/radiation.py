# subroutine radiation
# ~ ~ ~ PURPOSE ~ ~ ~
# this subroutine calculate the radiation

# ~ ~ ~ INCOMING VARIABLES ~ ~ ~
# name        |units         |definition
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# x_i	      |mol ph/m^2/min|[phyto] Half-saturation light level
# k_i	      |NA		     |[phyto] ??
# radiation   |W/m^2         |original data from csv file (envi_radiation.csv)
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

# ~ ~ ~ SUBROUTINES/FUNCTIONS CALLED ~ ~ ~
import pandas as pd
import numpy as np
from scipy.integrate import quad
import math
import readcsv as rd
import readphyto as rdphy
# ~ ~ ~ END SPECIFICATIONS ~ ~ ~

'''
Reshape radiation data into time series
'''
start_date = str(rd.years[0]) + "-01-01"
end_date = str(rd.years[-1]+1) + "-01-01 00:00"
time_index = pd.date_range(start=start_date, end=end_date, freq="H")
radiation = pd.DataFrame(data={"radiation": rd.radiation}, index=time_index)

'''
Get luminosity effect from a given time
'''
# Details can be found in Equation XXXX
def get_radiation(t, h):
    target_date = radiation.index[0] + pd.Timedelta(minutes=t)
    i_0 = radiation.loc[target_date, 'radiation']*0.25
    i = i_0*math.exp(-rdphy.k_i*h)
    rad = i/(i+rdphy.x_i)
    return rad

def f_l(hmax_values, t):
    results = np.vectorize(lambda hmax: quad(lambda h: get_radiation(t, h), 0,\
                           hmax)[0])(hmax_values) / hmax_values
    return results

