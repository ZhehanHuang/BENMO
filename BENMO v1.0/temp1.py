# subroutine temp

# ~ ~ ~ PURPOSE ~ ~ ~
# this subroutine reads the temperature information from the corresponding 
# csv file (envi_T.csv)

# ~ ~ ~ INCOMING VARIABLES ~ ~ ~
# name        |units         |definition
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# temp_data   |NA            |original data from csv file (envi_T.csv)

# ~ ~ ~ SUBROUTINES/FUNCTIONS CALLED ~ ~ ~
import readcsv as rd
# ~ ~ ~ END SPECIFICATIONS ~ ~ ~

temp=rd.temp_data

'''
Get temperature from a given time
'''
def get_temp_h(t): # for time step as hours
    t=int(t/60)
    t_k = 273 + temp[t]
    return t_k

