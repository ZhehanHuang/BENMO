# subroutine num_fish

# ~ ~ ~ PURPOSE ~ ~ ~
# this subroutine calculate the population size of fish

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
# fish_num               |none          |contain time series data of fish 
#                                       |population size
# num_values             |none          |numpy data for 'fish_num'
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ 

# ~ ~ ~ SUBROUTINES/FUNCTIONS CALLED ~ ~ ~
import pandas as pd
import readcsv as rd
import readall as rdall
# ~ ~ ~ END SPECIFICATIONS ~ ~ ~

'''
Calculate the population size of fish
'''
# time range
start_date = str(f'{rd.years[0]}-01-01')
end_date = str(f'{rd.years[-1]+1}-01-01')
date_range = pd.date_range(start_date, end_date, freq=f'{int(rd.time_step)}T')

fish_num = pd.DataFrame(index=date_range, columns=['1','2','3','4','5'])
fish_num[['1','2','3','4','5']] = 0

num_values_f = fish_num[['1','2','3','4','5']].values
weight_fish=1

for i in range(1, len(fish_num)):
    is_first_year = (fish_num.index[i].year == rd.years[0])
    is_before_start = (fish_num.index[i].month < rd.t_fish_start[0]) or\
                         (fish_num.index[i].month == rd.t_fish_start[0] and\
                          fish_num.index[i].day < rd.t_fish_start[1])
    is_start_day = (fish_num.index[i].month == rd.t_fish_start[0] and\
                    fish_num.index[i].day == rd.t_fish_start[1] and\
                    fish_num.index[i].hour == rd.t_fish_start[2] and\
                    fish_num.index[i].minute == rd.t_fish_start[3])
    is_start_end_same_year = (rd.t_fish_start[4] == rd.t_fish_end[4])
    is_after_end = (fish_num.index[i].month > rd.t_fish_end[0]) or\
                   (fish_num.index[i].month == rd.t_fish_end[0] and\
                    fish_num.index[i].day > rd.t_fish_end[1])
    is_between_start_end = ((fish_num.index[i].month > rd.t_fish_end[0]) and\
                            (fish_num.index[i].month < rd.t_fish_start[0])) or\
                          (((fish_num.index[i].month == rd.t_fish_end[0] and\
                              fish_num.index[i].day > rd.t_fish_end[1])) and \
                            ((fish_num.index[i].month == rd.t_fish_start[0] and\
                              fish_num.index[i].day < rd.t_fish_start[1])))
    if is_start_end_same_year:
        if is_before_start or is_after_end:
            num_values_f[i] = 0
        elif is_start_day:
            current_year = fish_num.index[i].year
            initial_values_year = rd.in_num_agr['acri_fish/t']\
                                    .loc[rd.in_num_agr['acri_fish/t']\
                                    .index == current_year]
            if not initial_values_year.empty:
                initial_values_year *= 1000 / weight_fish
                num_values_f[i] = initial_values_year.iloc[0,:].values
        else:
            diff = num_values_f[i-1] - num_values_f[i]
            num_values_f[i] = num_values_f[i-1] - (rdall.s_r * rd.time_step * diff)
    else:
        if is_first_year:
            if is_before_start:
                num_values_f[i] = 0
            elif is_start_day:
                current_year = fish_num.index[i].year
                initial_values_year = rd.in_num_agr['acri_fish/t']\
                                        .loc[rd.in_num_agr['acri_fish/t']\
                                        .index == current_year]
                if not initial_values_year.empty:
                    initial_values_year *= 1000 / weight_fish
                    num_values_f[i] = initial_values_year.iloc[0,:].values
            else:
                diff = num_values_f[i-1] - num_values_f[i]
                num_values_f[i] = num_values_f[i-1] - (rdall.s_r * rd.time_step * diff)
        else:
            if is_between_start_end:
                num_values_f[i] = 0
            elif is_start_day:
                current_year = fish_num.index[i].year
                initial_values_year = rd.in_num_agr['acri_fish/t']\
                                        .loc[rd.in_num_agr['acri_fish/t']\
                                        .index == current_year]
                if not initial_values_year.empty:
                    initial_values_year *= 1000 / weight_fish
                    num_values_f[i] = initial_values_year.iloc[0,:].values
            else:
                diff = num_values_f[i-1] - num_values_f[i]
                num_values_f[i] = num_values_f[i-1] - (rdall.s_r * rd.time_step * diff)       

fish_num.iloc[:,:] = num_values_f

'''
Get fish population size for a given time
'''
def fish_num(t):
    if t % rd.time_step == 0:
        num_f = num_values_f[int(t / rd.time_step), :]
        return num_f
    else:
        print('Error: wrong time input')
        return None