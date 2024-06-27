# subroutine readphyto

# ~ ~ ~ PURPOSE ~ ~ ~
# this subroutine reads the parameters for phytoplankton from the corresponding 
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
# r_p	      |1/min		 |[phyto] Respiration rate of phytoplankton
# e_up	      |NA		     |[phyto] Uptake associated excretion of 
#                            |phytoplankton
# g_pm	      |1/min		 |[phyto] Maximum phytoplankton growth rate
# q_pmin	  |mg N/mg C	 |[phyto] Minimum phytoplankton N:C ratio
# s_pmin	  |1/min	     |[phyto] Minimum phytoplankton sinking rate
# s_p	      |1/min	     |[phyto] Maximum phytoplankton sinking rate
# q_pmax	  |mg N/mg C	 |[phyto] Maximum phytoplankton N:C ratio
# q_poff	  |mg N/mg C	 |[phyto] Phytoplankton nitrogen uptake parameter
# k_op	      |na		     |[phyto] Reference reaction rate for phytoplankton
#                            |at 292 K
# t_ap	      |K		     |[phyto] Arrhenius temperature of phytoplankton
# t_alp	      |K		     |[phyto] Arrhenius temperature at lower boundary 
#                            |for phytoplankton
# t_lp	      |K		     |[phyto] Lower boundary of tolerance range for 
#                            |phytoplankton
# t_ahp	      |K		     |[phyto] Arrhenius temperature at upper boundary 
#                            |for phytoplankton
# t_op	      |K		     |[phyto] Reference temperature
# t_hp	      |K		     |[phyto] Upper boundary of tolerance range for 
#                            |phytoplankton
# x_i	      |mol ph/m^2/min|[phyto] Half-saturation light level
# i_0	      |mol/m^2/s	 |[phyto] Reference irradiance for seaweed 
#                            |photosynthesis
# k_i	      |NA		     |[phyto] ??
# u_nhmp	  |1/min		 |[phyto] Phytoplankton maximum uptake of NH4-N
# x_pnh	      |mg N/m^3		 |[phyto] Half-saturation NH4-N for phytoplankton 
#                            |uptake
# u_nomp	  |1/min	     |[phyto] Phytoplankton maximum uptake of NO3-N
# x_pno	      |mg N/m^3		 |[phyto] Half-saturation NH4-N for phytoplankton 
#                            |uptake
# e_up	      |NA		     |[phyto] Uptake associated excretion of 
#                            |phytoplankton
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ 

# ~ ~ ~ SUBROUTINES/FUNCTIONS CALLED ~ ~ ~
import readcsv as rd
# ~ ~ ~ END SPECIFICATIONS ~ ~ ~

'''
Parameters for phytoplankton
'''
r_p = rd.bio_data[46]/rd.d_to_min
e_up = rd.bio_data[47]
g_pm = rd.bio_data[48]/rd.d_to_min
q_pmin = rd.bio_data[49]
s_pmin = rd.bio_data[50]/rd.d_to_min
s_p = rd.bio_data[51]/rd.d_to_min
q_pmax = rd.bio_data[52]
q_poff = rd.bio_data[53]
k_op = rd.bio_data[54]
t_ap = rd.bio_data[55]
t_alp = rd.bio_data[56]
t_lp = rd.bio_data[57]
t_ahp = rd.bio_data[58]
t_op = rd.bio_data[59]
t_hp = rd.bio_data[60]
x_i = rd.bio_data[61]/rd.d_to_min
# i_0 = rd.bio_data[62]
k_i = rd.bio_data[63]
u_nhmp = rd.bio_data[64]/rd.d_to_min
x_pnh = rd.bio_data[65]
u_nomp = rd.bio_data[66]/rd.d_to_min
x_pno = rd.bio_data[67]
e_up = rd.bio_data[68]