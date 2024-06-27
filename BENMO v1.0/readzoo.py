# subroutine readzoo

# ~ ~ ~ PURPOSE ~ ~ ~
# this subroutine reads the parameters for zooplankton from the corresponding 
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
# d_z	      |NA		     |[zoo] Zooplankton faeces
# g_zm	      |1/min         |[zoo] Maximum growth rate of zooplankton
# r_zmin	  |NA		     |[zoo] Minimum reserves for zooplankton growth
# s_z	      |1/min	     |[zoo] Zooplankton mortality
# u_czm	      |1/min	     |[zoo] Maximum uptake rate of phytoplankton by 
#                            |zooplankton
# x_pz	      |mg C/m^3		 |[zoo] Half-saturation uptake of phytoplankton by
#                            |zooplankton for one minute
# q_z	      |mg N/mg C     |[zoo] N-quota of zooplankton
# u_poczm	  |1/min	     |[zoo] Maximum uptake rate of POC by zooplankton
# x_pocz	  |mg C/m^3		 |[zoo] Half-saturation uptake of POC by 
#                            |zooplankton
# r_z	      |1/min	     |[zoo] Respiration rate of zooplankton
# t_a_z	      |K	         |[zoo] Arrhenius temperature of zooplankton
# t_al_z	  |K		     |[zoo] Arrhenius temperature at lower boundary for
#                            |zooplankton
# t_l_z	      |K		     |[zoo] Lower boundary of tolerance range for 
#                            |zooplankton
# t_ah_z	  |K		     |[zoo] Arrhenius temperature at upper boundary for
#                            |zooplankton
# t_h_z	      |K		     |[zoo] Upper boundary of tolerance range for 
#                            |zooplankton
# k_oz	      |NA		     |[zoo] Reference reaction rate for zooplankton at 
#                            |291 K
# t_oz	      |K		     |[zoo] Reference temperature
# e_uz	      |NA		     |[zoo] Uptake associated excretion of zooplankton
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ 

# ~ ~ ~ SUBROUTINES/FUNCTIONS CALLED ~ ~ ~
import readcsv as rd
# ~ ~ ~ END SPECIFICATIONS ~ ~ ~

'''
Parameters for zooplankton
'''
d_z = rd.bio_data[69]
g_zm = rd.bio_data[70]/rd.d_to_min
r_zmin = rd.bio_data[71]
s_z = rd.bio_data[72]/rd.d_to_min
u_czm = rd.bio_data[73]/rd.d_to_min
x_pz = rd.bio_data[74]
q_z = rd.bio_data[75]
u_poczm = rd.bio_data[76]/rd.d_to_min
x_pocz = rd.bio_data[77]
r_z = rd.bio_data[78]/rd.d_to_min
t_a_z = rd.bio_data[79]
t_al_z = rd.bio_data[80]
t_l_z = rd.bio_data[81]
t_ah_z = rd.bio_data[82]
t_h_z = rd.bio_data[83]
k_oz = rd.bio_data[84]
t_oz = rd.bio_data[85]
e_uz = rd.bio_data[86]