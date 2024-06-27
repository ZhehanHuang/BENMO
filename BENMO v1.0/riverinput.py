# subroutine riverinput

# ~ ~ ~ PURPOSE ~ ~ ~
# this subroutine reads the information about the nitrients input from rivers 
# from the corresponding csv file (box_source_river.csv) and reshape them into 
# time series

# ~ ~ ~ INCOMING VARIABLES ~ ~ ~
# name        |units         |definition
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# river_in    |NA            |original data from csv file 
#                            |(box_source_river.csv)
# years       |none          |years of the model
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

# ~ ~ ~ LOCAL DEFINITIONS ~ ~ ~
# name        |units         |definition
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# types       |none          |the types of nitrients input from rivers
# data_frames |none          |contain time series data for 5 types of nitrients
#                            |input from rivers
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ 

# ~ ~ ~ SUBROUTINES/FUNCTIONS CALLED ~ ~ ~
import pandas as pd
import readcsv as rd
# ~ ~ ~ END SPECIFICATIONS ~ ~ ~

'''
Reshape river input to different types as time series
'''
data_frames = {}
types = ['nh', 'no', 'don', 'cp', 'nph']
split_position = 0
for tp in types:
    split_position_next = split_position + 60
    cut_river_in = rd.river_in[split_position:split_position_next, :]
    time_index = pd.date_range(start=f'{rd.years[0]}-01-01',\
                              periods=60, freq='MS')
    tp_river_in = pd.DataFrame(cut_river_in, index=time_index,\
                              columns=['1', '2', '3', '4', '5'])
    data_frames[f'{tp}_river_in'] = tp_river_in
    split_position = split_position_next

'''
Get river input for a given time
'''
def source_river(t,tp):
    target_date = time_index[0] + pd.Timedelta(minutes=t)
    year = target_date.year
    month = target_date.month
    tp_river = data_frames[f"{tp}_river_in"]
    row = tp_river[(tp_river.index.year == year) &\
                   (tp_river.index.month == month)].iloc[0]
    return row
