# subroutine runfish

# ~ ~ ~ PURPOSE ~ ~ ~
# this subroutine calculate the process of biotization of fish

# ~ ~ ~ INCOMING VARIABLES ~ ~ ~
# name        |units         |definition
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# num_step    |NA            |number of time steps 
# time_step   |min           |time step the model used
# k_of	      |NA		     |[fish] Reference physiological reaction rate for 
#                            |fish at 288 K
# t_af	      |K		     |[fish] Arrhenius temperature of fish
# t_alf	      |K		     |[fish] Arrhenius temperature at lower boundary 
#                            |for fish
# t_lf	      |K		     |[fish] Lower boundary of tolerance range for fish
# t_ahf	      |K		     |[fish] Arrhenius temperature at upper boundary 
#                            |for fish
# t_hf	      |K		     |[fish] Upper boundary of tolerance range for fish
# e_g_f	      |J/cm^3		 |[fish] Volume-specific costs for fish growth
# k_f	      |NA		     |[fish] Catabolic flux to growth and maintenance 
#                            |in fish
# p_a_1_f	  |J/cm^3/min    |[fish] fish maximum surface area-specific 
#                            |assimilation
# e_m_f	      |J/cm^3		 |[fish] Maximum reserve density of fish
# p_m_1_f	  |J/cm^3/min    |[fish] Volume-specific maintenance rate of fish
# v_p_f	      |1/cm^3		 |[fish] fish structural volume at puberty
# f_f	      |NA		     |[fish] Functional response of cultured animals
# u_mf	      |m^3/cm^2/min	 |[fish] fish maximum surface area-specific 
#                            |consumption
# k_r_f	      |NA		     |[fish] Fraction of reproduction energy fixed in 
#                            |eggs
# u_vf	      |J/g wet W	 |[fish] Structure energy content of fish
# q_f	      |mg N/mg C	 |[fish] N-quota of fish
# q_ff	      |mg N/mg C	 |[fish] N-quota of fish feed
# p           |g wet W/cm^3  |[all] Biovolume density of cultured animals
# u_cj        |J/mg C        |[all] Ratio of carbon to energy content
# s_r         |1/min         |[all] Natural mortality of shellfish/seaweed
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

# ~ ~ ~ LOCAL DEFINITIONS ~ ~ ~
# name        |units         |definition
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# p_c_f       |??            |Catabolic rate of fish 
# p_m_f       |??            |Maintenance rate of fish
# p_j_f       |??            |Maturity maintenance of fish
# p_a_f       |??            |Assimilation rate of fish
# u_f         |??            |Consumption rate of fish
# excre_f     |??            |Fish excretion
# faece_f     |??            |Faeces of fish
# w_f         |??            |Waste feed
# m_f         |??            |C loss (mortality) of fish
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ 

# ~ ~ ~ SUBROUTINES/FUNCTIONS CALLED ~ ~ ~
import numpy as np
import readcsv as rd
import readall as rdall
import readfish as rdf
import num_fish as numf
import temp1 as tp
# ~ ~ ~ END SPECIFICATIONS ~ ~ ~    

'''
Calculate the temperature effect function of fish
'''
def temp_f(t):
    temp_f = rdf.k_of*np.exp(rdf.t_af/rdf.t_of-rdf.t_af/tp.get_temp_h(t))\
             *(1+np.exp(rdf.t_alf/tp.get_temp_h(t)-rdf.t_alf/rdf.t_lf)\
             +np.exp(rdf.t_ahf/rdf.t_hf-rdf.t_ahf/tp.get_temp_h(t)))**(-1)
    return temp_f

'''
Calculate the process of biotization of zooplankton
'''
# Details can be found in Equation XXXX
def calculate_fish(i,t,e_f,v_f,e_r_f):
    p_c_f = np.nan_to_num(temp_f(t)*(e_f/v_f)/(rdf.e_g_f+rdf.k_f*(e_f/v_f))\
            *((rdf.e_g_f*rdf.p_a_1_f*rd.time_step*v_f**(2/3))/rdf.e_m_f\
            +rdf.p_m_1_f*rd.time_step*v_f), nan=0)
    p_m_f = temp_f(t)*rdf.p_m_1_f*rd.time_step*v_f
    p_j_f = np.minimum(v_f,rdf.v_p_f)*rdf.p_m_1_f*rd.time_step*(1-rdf.k_f)/rdf.k_f 
    p_a_f = temp_f(t)*rdf.f_f*rdf.p_a_1_f*rd.time_step*v_f**(2/3)   
    u_f = temp_f(t)*rdf.u_mf*rd.time_step*v_f**(2/3)
    excre_f = ((p_c_f-(1-rdf.k_r_f)*((1-rdf.k_f)*p_c_f-p_j_f)\
              -rdf.u_vf*rdall.p*abs(rdf.k_f*p_c_f-p_m_f)/rdf.e_g_f)*rdf.q_f\
              +p_a_f*abs(rdf.q_ff-rdf.q_f))/rdall.u_cj    
    faece_f =u_f-p_a_f/rdall.u_cj
    w_f = temp_f(t)*rdf.u_mf*rd.time_step*v_f**(2/3)
    m_f = rdall.s_r*rd.time_step*numf.fish_num(t)*(v_f*rdall.p*rdf.u_vf\
          +(e_f+e_r_f*rdf.k_r_f))/rdall.u_cj
    v_f_next = v_f + abs(rdf.k_f*p_c_f-p_m_f)/rdf.e_g_f  
    e_f_next =  e_f + p_a_f-p_c_f  
    e_r_f_next = e_r_f + (1-rdf.k_f)*p_c_f-p_j_f
    return v_f_next, e_f_next, e_r_f_next, excre_f, faece_f, w_f, m_f