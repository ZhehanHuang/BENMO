# subroutine num_shellfish

# ~ ~ ~ PURPOSE ~ ~ ~
# this subroutine calculate the population size of shellfish

# ~ ~ ~ INCOMING VARIABLES ~ ~ ~
# name        |units         |definition
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# in_num_agr  |NA            |reclassified data for fish, shellfish and seaweed 
# years       |none          |years of the model
# time_step   |min           |time step the model used
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

# ~ ~ ~ LOCAL DEFINITIONS ~ ~ ~
# name                   |units         |definition
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# shellfish_num          |none          |contain time series data of shellfish 
#                                       |population size
# num_values             |none          |numpy data for 'shellfish_num'
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ 

# ~ ~ ~ SUBROUTINES/FUNCTIONS CALLED ~ ~ ~
import pandas as pd
import readcsv as rd
import readall as rdall
# ~ ~ ~ END SPECIFICATIONS ~ ~ ~

'''
Calculate the population size of shellfish
'''
# time range
start_date = str(f'{rd.years[0]}-01-01')
end_date = str(f'{rd.years[-1]+1}-01-01')
date_range = pd.date_range(start_date, end_date, freq=f'{int(rd.time_step)}T')

shellfish_num = pd.DataFrame(index=date_range, columns=['1','2','3','4','5'])
shellfish_num[['1','2','3','4','5']] = 0

num_values = shellfish_num[['1','2','3','4','5']].values

for i in range(1, len(shellfish_num)):
    is_first_year = (shellfish_num.index[i].year == rd.years[0])
    is_before_start = (shellfish_num.index[i].month < rd.t_shellfish_start[0]) or\
                         (shellfish_num.index[i].month == rd.t_shellfish_start[0] and\
                          shellfish_num.index[i].day < rd.t_shellfish_start[1])
    is_start_day = (shellfish_num.index[i].month == rd.t_shellfish_start[0] and\
                    shellfish_num.index[i].day == rd.t_shellfish_start[1] and\
                    shellfish_num.index[i].hour == rd.t_shellfish_start[2] and\
                    shellfish_num.index[i].minute == rd.t_shellfish_start[3])
    is_start_end_same_year = (rd.t_shellfish_start[4] == rd.t_shellfish_end[4])
    is_after_end = (shellfish_num.index[i].month > rd.t_shellfish_end[0]) or\
                   (shellfish_num.index[i].month == rd.t_shellfish_end[0] and\
                    shellfish_num.index[i].day > rd.t_shellfish_end[1])
    is_between_start_end = ((shellfish_num.index[i].month > rd.t_shellfish_end[0]) and\
                            (shellfish_num.index[i].month < rd.t_shellfish_start[0])) or\
                          (((shellfish_num.index[i].month == rd.t_shellfish_end[0] and\
                              shellfish_num.index[i].day > rd.t_shellfish_end[1])) and \
                            ((shellfish_num.index[i].month == rd.t_shellfish_start[0] and\
                              shellfish_num.index[i].day < rd.t_shellfish_start[1])))
    if is_start_end_same_year:
        if is_before_start or is_after_end:
            num_values[i] = 0
        elif is_start_day:
            current_year = shellfish_num.index[i].year
            initial_values_year = rd.in_num_agr['acri_shellfish/t']\
                                    .loc[rd.in_num_agr['acri_shellfish/t']\
                                    .index == current_year]
            if not initial_values_year.empty:
                initial_values_year *= 1000 / 0.05
                num_values[i] = initial_values_year.iloc[0,:].values
        else:
            diff = num_values[i-1] - num_values[i]
            num_values[i] = num_values[i-1] - (rdall.s_r * rd.time_step * diff)
    else:
        if is_first_year:
            if is_before_start:
                num_values[i] = 0
            elif is_start_day:
                current_year = shellfish_num.index[i].year
                initial_values_year = rd.in_num_agr['acri_shellfish/t']\
                                        .loc[rd.in_num_agr['acri_shellfish/t']\
                                        .index == current_year]
                if not initial_values_year.empty:
                    initial_values_year *= 1000 / 0.05
                    num_values[i] = initial_values_year.iloc[0,:].values
            else:
                diff = num_values[i-1] - num_values[i]
                num_values[i] = num_values[i-1] - (rdall.s_r * rd.time_step * diff)
        else:
            if is_between_start_end:
                num_values[i] = 0
            elif is_start_day:
                current_year = shellfish_num.index[i].year
                initial_values_year = rd.in_num_agr['acri_shellfish/t']\
                                        .loc[rd.in_num_agr['acri_shellfish/t']\
                                        .index == current_year]
                if not initial_values_year.empty:
                    initial_values_year *= 1000 / 0.05
                    num_values[i] = initial_values_year.iloc[0,:].values
            else:
                diff = num_values[i-1] - num_values[i]
                num_values[i] = num_values[i-1] - (rdall.s_r * rd.time_step * diff)       

shellfish_num.iloc[:,:] = num_values

'''
Get shellfish population size for a given time
'''
def shellfish_num(t):
    if t % rd.time_step == 0:
        num_s = num_values[int(t / rd.time_step), :]
        return num_s
    else:
        print('Error: wrong time input')
        return None
