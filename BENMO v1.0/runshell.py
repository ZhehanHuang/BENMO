# subroutine runshell

# ~ ~ ~ PURPOSE ~ ~ ~
# this subroutine calculate the process of biotization of shellfish

# ~ ~ ~ INCOMING VARIABLES ~ ~ ~
# name        |units         |definition
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# num_step    |NA            |number of time steps 
# time_step   |min           |time step the model used
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
# e_g_s	      |J/cm^3		 |[shellfish] Volume-specific costs for shellfish 
#                            |growth
# k_s	      |NA       	 |[shellfish] Catabolic flux to growth and 
#                            |maintenance in shellfish
# p_a_1_s	  |J/cm^3/min    |[shellfish] maximum surface area-specific 
#                            |assimilation rate
# e_m_s	      |J/cm^3		 |[shellfish] maximum storage density
# p_m_1_s	  |J/cm^3/min    |[shellfish] Volume-specific maintenance costs
# v_p_s	      |1/cm^3	     |[shellfish] Structural volume at sexual maturity
# f_s   	  |NA		     |[shellfish] Functional response of cultured 
#                            |animals
# u_m_s	      |m^3/cm^2/min	 |[shellfish] shellfish maximum surface 
#                            |area-specific clearance
# u_vs	      |J/g wet W	 |[shellfish] Structure energy content of shellfish
# q_s         |mg N/mg C     |[shellfish] N-quota of shellfish
# p           |g wet W/cm^3  |[all] Biovolume density of cultured animals
# u_cj        |J/mg C        |[all] Ratio of carbon to energy content
# s_r         |1/min         |[all] Natural mortality of shellfish/seaweed
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

# ~ ~ ~ LOCAL DEFINITIONS ~ ~ ~
# name        |units         |definition
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# p_c_s       |??            |Catabolic rate of shellfish
# p_m_s       |??            |Maintenance rate of shellfish
# p_j_s       |??            |Maturity maintenance of shellfish
# p_a_s       |??            |Assimilation rate of shellfish
# u_so        |??            |Consumption rate of POC by shellfish
# u_s         |??            |Consumption rate of shellfish
# m_s         |??            |C loss (mortality) of shellfish
# excre_s     |??            |Shellfish excretion
# faece_s     |??            |Faeces of shellfish
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ 

# ~ ~ ~ SUBROUTINES/FUNCTIONS CALLED ~ ~ ~
import numpy as np
import readcsv as rd
import readall as rdall
import readshell as rds
import num_shellfish as numsh
import temp1 as tp
# ~ ~ ~ END SPECIFICATIONS ~ ~ ~

'''
Calculate the temperature effect function of shellfish
'''
def temp_s(t):
    temp_s = rds.k_o_s*np.exp(rds.t_a_s/rds.t_o_s-rds.t_a_s/tp.get_temp_h(t))\
             *(1+np.exp(rds.t_al_s/tp.get_temp_h(t)-rds.t_al_s/rds.t_l_s)\
             +np.exp(rds.t_ah_s/rds.t_h_s-rds.t_ah_s/tp.get_temp_h(t)))**(-1)
    return temp_s

'''
Calculate the process of biotization of zooplankton
'''
# Details can be found in Equation XXXX
def calculate_shellfish(i,t,q_p,u_sp,e_s,v_s,e_r_s,poc):    
    p_c_s = np.nan_to_num(temp_s(t)*(e_s/v_s)/(rds.e_g_s+rds.k_s*(e_s/v_s))\
            *(rds.e_g_s*rds.p_a_1_s*rd.time_step*v_s**(2/3)/rds.e_m_s\
            +rds.p_m_1_s*rd.time_step*v_s), nan=0)
    p_m_s = temp_s(t)*rds.p_m_1_s*rd.time_step*v_s
    p_j_s = np.minimum(v_s,rds.v_p_s)*rds.p_m_1_s*rd.time_step*(1-rds.k_s)/rds.k_s 
    p_a_s = temp_s(t)*rds.f_s*rds.p_a_1_s*rd.time_step*v_s**(2/3)    
    u_so = temp_s(t)*rds.u_m_s*rd.time_step*poc*0.01*v_s**(2/3)
    u_s = u_sp+u_so
    m_s = rdall.s_r*rd.time_step*numsh.shellfish_num(t)*(v_s*rdall.p*rds.u_vs\
          +(e_s+e_r_s*rds.k_r_s))/rdall.u_cj
    excre_s = ((p_c_s-(1-rds.k_r_s)*((1-rds.k_s)*p_c_s-p_j_s)-rds.u_vs*rdall.p\
              *abs(rds.k_s*p_c_s-p_m_s)/rds.e_g_s)*rds.q_s+p_a_s\
              *abs(q_p-rds.q_s))/rdall.u_cj      
    faece_s = u_s-p_a_s/rdall.u_cj   
    v_s_next = v_s + abs(rds.k_s*p_c_s-p_m_s)/rds.e_g_s
    e_s_next = e_s + p_a_s-p_c_s
    e_r_s_next = e_r_s + (1-rds.k_s)*p_c_s-p_j_s
    return v_s_next, e_s_next, e_r_s_next, m_s, excre_s, faece_s, u_so