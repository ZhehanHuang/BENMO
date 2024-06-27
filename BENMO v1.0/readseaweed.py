# subroutine readseaweed

# ~ ~ ~ PURPOSE ~ ~ ~
# this subroutine reads the parameters for seaweed from the corresponding 
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
# t_a_a	      |K		     |[seaweed] Arrhenius temperature of seaweed
# t_al_a	  |K		     |[seaweed] Arrhenius temperature at lower boundary
#                            |for seaweed
# t_l_a	      |K		     |[seaweed] Lower boundary of tolerance range for 
#                            |seaweed
# t_ah_a	  |K		     |[seaweed] Arrhenius temperature at upper boundary
#                            |for seaweed
# t_h_a	      |K		     |[seaweed] Upper boundary of tolerance range for 
#                            |seaweed
# k_oa	      |NA		     |[seaweed] Reference reaction rate for seaweed at 
#                            |286 K
# t_oa	      |K		     |[seaweed] Reference temperature
# g_am	      |1/min	     |[seaweed] Maximum seaweed growth rate
# r_a	      |1/min	     |[seaweed] Respiration rate of seaweed
# e_ua	      |NA		     |[seaweed] Uptake associated excretion of seaweed
# q_amin	  |mg N/mg C	 |[seaweed] Minimum seaweed N:C ratio
# q_amax	  |mg N/mg C	 |[seaweed] Maximum seaweed N:C ratio
# q_aoff	  |mg N/mg C	 |[seaweed] Seaweed nitrogen uptake parameter
# u_nhma	  |1/min	     |[seaweed] Seaweed maximum uptake of ammonia N
# x_anh	      |mg N/m^3		 |[seaweed] Half-saturation ammonia-N for seaweed 
#                            |uptake
# u_noma	  |1/min	     |[seaweed] Seaweed maximum uptake of nitrate N
# x_ano	      |mg N/m^3		 |[seaweed] Half-saturation nitrate-N for seaweed
#                            |uptake
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ 

# ~ ~ ~ SUBROUTINES/FUNCTIONS CALLED ~ ~ ~
import readcsv as rd
# ~ ~ ~ END SPECIFICATIONS ~ ~ ~

'''
Parameters for seaweed
'''
t_a_a = rd.bio_data[87]
t_al_a = rd.bio_data[88]
t_l_a = rd.bio_data[89]
t_ah_a = rd.bio_data[90]
t_h_a = rd.bio_data[91]
k_oa = rd.bio_data[92]
t_oa = rd.bio_data[93]
g_am = rd.bio_data[94]/rd.d_to_min
r_a = rd.bio_data[95]/rd.d_to_min
e_ua = rd.bio_data[96]
q_amin = rd.bio_data[97]
q_amax = rd.bio_data[98]
q_aoff = rd.bio_data[99]
u_nhma = rd.bio_data[100]/rd.d_to_min
x_anh = rd.bio_data[101]
u_noma = rd.bio_data[102]/rd.d_to_min
x_ano = rd.bio_data[103]