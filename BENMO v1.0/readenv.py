# subroutine readenv

# ~ ~ ~ PURPOSE ~ ~ ~
# this subroutine reads the parameters for environment from the corresponding 
# csv file (bio_coe.csv) and rename them into the form required by the model

# ~ ~ ~ INCOMING VARIABLES ~ ~ ~
# name        |units         |definition
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# bio_data    |NA            |original data from csv file (bio_coe.csv)
# d_to_min    |min/d         |number of minutes in a day
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ 

# ~ ~ ~ OUTGOING VARIABLES ~ ~ ~
# name        |units         |definition
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# k_sr	      |1/min	     |[environment] Nitrogen and carbon release rate
# k_db	      |1/min	     |[environment] Sediment N and C bury rate
# q_o	      |mg N/mg C	 |[environment] N-quota of particulate detrital 
#                            |organics
# y_0	      |1/min	     |[environment] Resuspension coefficient of 
#                            |sediment organic matters
# p_0	      |1/min	     |[environment] Water-column organic settling rate
# r_don	      |NA		     |[environment] DON fraction of phytoplankton/
#                            |seaweed excretion
# k_or	      |1/min	     |[environment] Water-column DON remineralisation 
#                            |rate
# k_nit_20    |1/d           |[environment] Water-column nitrification rate 
#                            |at 20 degree
# kt_nit      |NA            |[environment] temperature coefficient for 
#                            |nitrification
# x_nh        |g N/m^3       |[environment] half saturation constant for 
#                            |ammonium cons
# poro        |NA            |[environment] volumetric porosity
# t_k_c_nit   |K             |[environment] critical temperature for 
#                            |nitrification
# x_do        |NA            |[environment] half saturation constant for oxygen
#                            |inhib
# k_denit_20  |1/d           |[environment] Water-column denitrification rate 
#                            |at 20 degree
# kt_denit    |NA            |[environment] temperature coefficient for 
#                            |denitrification
# x_no        |g N/m^3       |[environment] half saturation constant for 
#                            |nitrate cons
# t_k_c_den   |K             |[environment] critical temperature for 
#                            |denitrification
# do          |mg/L          |[environment] ???
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ 

# ~ ~ ~ SUBROUTINES/FUNCTIONS CALLED ~ ~ ~
import readcsv as rd
# ~ ~ ~ END SPECIFICATIONS ~ ~ ~

'''
Parameters for the environment
'''
k_sr = rd.bio_data[104]/rd.d_to_min*0.01
k_db = rd.bio_data[105]/rd.d_to_min
q_o = rd.bio_data[106]
y_0 = rd.bio_data[107]/rd.d_to_min
p_0 = rd.bio_data[108]/rd.d_to_min
r_don = rd.bio_data[109]
k_or = rd.bio_data[110]/rd.d_to_min
k_nit_20 = rd.bio_data[111]
kt_nit = rd.bio_data[112]
x_nh = rd.bio_data[113]
poro = rd.bio_data[114]
t_k_c_nit = rd.bio_data[115]
x_do = rd.bio_data[116]
k_denit_20 = rd.bio_data[117]
kt_denit = rd.bio_data[118]
x_no = rd.bio_data[119]
t_k_c_den = rd.bio_data[120]
do = rd.bio_data[121]
