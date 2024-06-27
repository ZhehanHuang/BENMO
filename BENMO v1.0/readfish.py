# subroutine readfish

# ~ ~ ~ PURPOSE ~ ~ ~
# this subroutine reads the parameters for fish from the corresponding 
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
# p_a_1_f	  |J/cm^3/min    |[fish] fish maximum surface area-specific 
#                            |assimilation
# e_g_f	      |J/cm^3		 |[fish] Volume-specific costs for fish growth
# k_f	      |NA		     |[fish] Catabolic flux to growth and maintenance 
#                            |in fish
# e_m_f	      |J/cm^3		 |[fish] Maximum reserve density of fish
# p_m_1_f	  |J/cm^3/min    |[fish] Volume-specific maintenance rate of fish
# v_p_f	      |1/cm^3		 |[fish] fish structural volume at puberty
# t_af	      |K		     |[fish] Arrhenius temperature of fish
# t_alf	      |K		     |[fish] Arrhenius temperature at lower boundary 
#                            |for fish
# t_lf	      |K		     |[fish] Lower boundary of tolerance range for fish
# t_ahf	      |K		     |[fish] Arrhenius temperature at upper boundary 
#                            |for fish
# t_hf	      |K		     |[fish] Upper boundary of tolerance range for fish
# t_of	      |K		     |[fish] Reference temperature
# f_f	      |NA		     |[fish] Functional response of cultured animals
# f_f_h	      |g		     |[fish] Half-saturation uptake of food by fish
# f_r		  |none	         |[fish] minimum volume-specific consumption rate
# q_f	      |mg N/mg C	 |[fish] N-quota of fish
# k_of	      |NA		     |[fish] Reference physiological reaction rate for 
#                            |fish at 288 K
# q_ff	      |mg N/mg C	 |[fish] N-quota of fish feed
# k_r_f	      |NA		     |[fish] Fraction of reproduction energy fixed in 
#                            |eggs
# u_mf	      |m^3/cm^2/min	 |[fish] fish maximum surface area-specific 
#                            |consumption
# u_vf	      |J/g wet W	 |[fish] Structure energy content of fish
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ 

# ~ ~ ~ SUBROUTINES/FUNCTIONS CALLED ~ ~ ~
import readcsv as rd
# ~ ~ ~ END SPECIFICATIONS ~ ~ ~

'''
Parameters for fish
'''
p_a_1_f = rd.bio_data[25]/rd.d_to_min
e_g_f = rd.bio_data[26]
k_f = rd.bio_data[27]
e_m_f = rd.bio_data[28]
p_m_1_f = rd.bio_data[29]/rd.d_to_min
v_p_f = rd.bio_data[30]
t_af = rd.bio_data[31]
t_alf = rd.bio_data[32]
t_lf = rd.bio_data[33]
t_ahf = rd.bio_data[34]
t_hf = rd.bio_data[35]
t_of = rd.bio_data[36]
f_f = rd.bio_data[37]
f_f_h = rd.bio_data[38]
f_r = rd.bio_data[39]
q_f = rd.bio_data[40]
k_of = rd.bio_data[41]
q_ff = rd.bio_data[42]
k_r_f = rd.bio_data[43]
u_mf = rd.bio_data[44]/rd.d_to_min
u_vf = rd.bio_data[45]