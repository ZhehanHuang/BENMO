# subroutine readshell

# ~ ~ ~ PURPOSE ~ ~ ~
# this subroutine reads the parameters for shellfish from the corresponding 
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
# k_r_s       |NA            |[shellfish] Fraction of reproduction energy
#                            |fixed in eggs
# u_v_s       |J/g wet W     |[shellfish] Structure energy content
# q_s         |mg N/mg C     |[shellfish] N-quota of shellfish
# e_g_s	      |J/cm^3		 |[shellfish] Volume-specific costs for shellfish 
#                            |growth
# k_s	      |NA       	 |[shellfish] Catabolic flux to growth and 
#                            |maintenance in shellfish
# p_a_1_s	  |J/cm^3/min    |[shellfish] maximum surface area-specific 
#                            |assimilation rate
# e_m_s	      |J/cm^3		 |[shellfish] maximum storage density
# p_m_1_s	  |J/cm^3/min    |[shellfish] Volume-specific maintenance costs
# k_o_s	      |NA	      	 |[shellfish] Reference reaction rate for shellfish
#                            |at 288 K
# t_a_s	      |K		     |[shellfish] Arrhenius temperature of shellfish
# t_al_s	  |K		     |[shellfish] Arrhenius temperature at lower 
#                            |boundary for shellfish
# t_l_s	      |K		     |[shellfish] Lower boundary of tolerance range 
#                            |for shellfish
# t_ah_s	  |K		     |[shellfish] Arrhenius temperature at upper 
#                            |boundary for shellfish
# t_h_s	      |K		     |[shellfish] Upper boundary of tolerance range 
#                            |for shellfish
# f_h	      |mg C/m^3  	 |[shellfish] Half-saturation uptake of 
#                            |phytoplankton by shellfish
# f_s_h	      |mg C/m^3		 |[shellfish] Half-saturation uptake of food by 
#                            |shellfish
# v_p_s	      |1/cm^3	     |[shellfish] Structural volume at sexual maturity
# f_s   	  |NA		     |[shellfish] Functional response of cultured 
#                            |animals
# u_m_s	      |m^3/cm^2/min	 |[shellfish] shellfish maximum surface 
#                            |area-specific clearance
# u_vs	      |J/g wet W	 |[shellfish] Structure energy content of shellfish
# t_o_s	      |K		     |[shellfish] Reference temperature
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ 

# ~ ~ ~ SUBROUTINES/FUNCTIONS CALLED ~ ~ ~
import readcsv as rd
# ~ ~ ~ END SPECIFICATIONS ~ ~ ~
    
'''
Parameters for shellfish
'''
k_r_s = rd.bio_data[4]
u_v_s = rd.bio_data[5]
q_s = rd.bio_data[6]
e_g_s = rd.bio_data[7]
k_s = rd.bio_data[8]
p_a_1_s = rd.bio_data[9]/rd.d_to_min
e_m_s = rd.bio_data[10]
p_m_1_s = rd.bio_data[11]/rd.d_to_min
k_o_s = rd.bio_data[12]
t_a_s = rd.bio_data[13]
t_al_s = rd.bio_data[14]
t_l_s = rd.bio_data[15]
t_ah_s = rd.bio_data[16]
t_h_s = rd.bio_data[17]
f_h = rd.bio_data[18]
f_s_h = rd.bio_data[19]
v_p_s = rd.bio_data[20]
f_s = rd.bio_data[21]
u_m_s = rd.bio_data[22]/rd.d_to_min
u_vs = rd.bio_data[23]
t_o_s = rd.bio_data[24]