# subroutine runzoo

# ~ ~ ~ PURPOSE ~ ~ ~
# this subroutine calculate the process of biotization of the zooplankton

# ~ ~ ~ INCOMING VARIABLES ~ ~ ~
# name        |units         |definition
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# num_step    |NA            |number of time steps 
# time_step   |min           |time step the model used
# k_oz	      |NA		     |[zoo] Reference reaction rate for zooplankton at 
#                            |291 K
# t_a_z	      |K	         |[zoo] Arrhenius temperature of zooplankton
# t_al_z	  |K		     |[zoo] Arrhenius temperature at lower boundary for
#                            |zooplankton
# t_l_z	      |K		     |[zoo] Lower boundary of tolerance range for 
#                            |zooplankton
# t_oz	      |K		     |[zoo] Reference temperature
# t_ah_z	  |K		     |[zoo] Arrhenius temperature at upper boundary for
#                            |zooplankton
# t_h_z	      |K		     |[zoo] Upper boundary of tolerance range for 
#                            |zooplankton
# g_zm	      |1/min         |[zoo] Maximum growth rate of zooplankton
# r_zmin	  |NA		     |[zoo] Minimum reserves for zooplankton growth
# s_z	      |1/min	     |[zoo] Zooplankton mortality
# u_poczm	  |1/min	     |[zoo] Maximum uptake rate of POC by zooplankton
# x_pocz	  |mg C/m^3		 |[zoo] Half-saturation uptake of POC by 
#                            |zooplankton
# q_z	      |mg N/mg C     |[zoo] N-quota of zooplankton
# e_uz	      |NA		     |[zoo] Uptake associated excretion of zooplankton
# d_z	      |NA		     |[zoo] Zooplankton faeces
# q_o	      |mg N/mg C	 |[environment] N-quota of particulate detrital 
#                            |organics
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

# ~ ~ ~ LOCAL DEFINITIONS ~ ~ ~
# name        |units         |definition
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# g_z         |??            |Zooplankton growth rate
# cz_p        |??            |C loss rate of zooplankton structure weight
# u_zo        |??            |Uptake of POC by zooplankton
# ez_p        |??            |C loss rate of zooplankton reserves
# u_z         |??            |Uptake of zooplankton
# excre_z     |??            |Zooplankton excretion
# faece_z     |??            |Zooplankton faeces
# m_z         |??            |Zooplankton mortality
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ 

# ~ ~ ~ SUBROUTINES/FUNCTIONS CALLED ~ ~ ~
import numpy as np
import math
import readcsv as rd
import readzoo as rdz
import readenv as rden
import temp1 as tp
# ~ ~ ~ END SPECIFICATIONS ~ ~ ~

'''
Calculate the temperature effect function of zooplankton
'''
def temp_z(t):
    temp_z = rdz.k_oz*np.exp(rdz.t_a_z/rdz.t_oz-rdz.t_a_z/tp.get_temp_h(t))\
             *(1+np.exp(rdz.t_al_z/tp.get_temp_h(t)-rdz.t_al_z/rdz.t_l_z)\
             +np.exp(rdz.t_ah_z/rdz.t_h_z-rdz.t_ah_z/tp.get_temp_h(t)))**(-1)
    return temp_z

'''
Calculate the process of biotization of zooplankton
'''
# Details can be found in Equation XXXX
def calculate_zoo(i,t,u_zp,ez,cz,poc):
    g_z = rdz.g_zm*rd.time_step*ez*temp_z(t)*np.maximum(0,1-rdz.r_zmin/(ez/(cz+ez)))
    cz_p = rdz.s_z*rd.time_step*cz
    u_zo = (cz*rdz.u_poczm*0.01*rd.time_step*poc/(poc+rdz.x_pocz))*np.minimum(rden.q_o/rdz.q_z,1)
    ez_p = rdz.s_z*rd.time_step*ez+rdz.r_z*rd.time_step*temp_z(t)*cz
    u_z = u_zo+u_zp   
    excre_z = rdz.e_uz*u_z*rdz.q_z+rdz.r_z*rd.time_step*temp_z(t)*cz*rdz.q_z   
    faece_z = rdz.d_z*(u_zp+u_zo)
    m_z = rdz.s_z*rd.time_step*(cz+ez)
    cz_next = cz+g_z-cz_p
    ez_next = ez+(1-rdz.d_z)*(u_zp+u_zo)-g_z-ez_p
    return cz_next, ez_next, excre_z, faece_z, m_z
    