# subroutine runphyto

# ~ ~ ~ PURPOSE ~ ~ ~
# this subroutine calculate the process of biotization of the phytoplankton

# ~ ~ ~ INCOMING VARIABLES ~ ~ ~
# name        |units         |definition
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# num_step    |NA            |number of time steps 
# time_step   |min           |time step the model used
# k_op	      |na		     |[phyto] Reference reaction rate for phytoplankton
#                            |at 292 K
# t_ap	      |K		     |[phyto] Arrhenius temperature of phytoplankton
# t_op	      |K		     |[phyto] Reference temperature
# t_alp	      |K		     |[phyto] Arrhenius temperature at lower boundary 
#                            |for phytoplankton
# t_lp	      |K		     |[phyto] Lower boundary of tolerance range for 
#                            |phytoplankton
# t_ahp	      |K		     |[phyto] Arrhenius temperature at upper boundary 
#                            |for phytoplankton
# t_hp	      |K		     |[phyto] Upper boundary of tolerance range for 
#                            |phytoplankton
# u_nhmp	  |1/min		 |[phyto] Phytoplankton maximum uptake of NH4-N
# u_nomp	  |1/min	     |[phyto] Phytoplankton maximum uptake of NO3-N
# x_pnh	      |mg N/m^3		 |[phyto] Half-saturation NH4-N for phytoplankton 
#                            |uptake
# x_pno	      |mg N/m^3		 |[phyto] Half-saturation NH4-N for phytoplankton 
#                            |uptake
# g_pm	      |1/min		 |[phyto] Maximum phytoplankton growth rate
# q_pmin	  |mg N/mg C	 |[phyto] Minimum phytoplankton N:C ratio
# s_pmin	  |1/min	     |[phyto] Minimum phytoplankton sinking rate
# s_p	      |1/min	     |[phyto] Maximum phytoplankton sinking rate
# q_pmax	  |mg N/mg C	 |[phyto] Maximum phytoplankton N:C ratio
# q_poff	  |mg N/mg C	 |[phyto] Phytoplankton nitrogen uptake parameter
# e_up	      |NA		     |[phyto] Uptake associated excretion of 
#                            |phytoplankton
# r_p	      |1/min		 |[phyto] Respiration rate of phytoplankton
# u_czm	      |1/min	     |[zoo] Maximum uptake rate of phytoplankton by 
#                            |zooplankton
# x_pz	      |mg C/m^3		 |[zoo] Half-saturation uptake of phytoplankton by
#                            |zooplankton for one minute
# q_z	      |mg N/mg C     |[zoo] N-quota of zooplankton
# u_m_s	      |m^3/cm^2/min	 |[shellfish] shellfish maximum surface 
#                            |area-specific clearance
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

# ~ ~ ~ LOCAL DEFINITIONS ~ ~ ~
# name        |units         |definition
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# q_p         |??            |Phytoplankton N quota
# u_nhp       |??            |Potential uptake of NH4 by phytoplankton
# u_nop       |??            |Potential uptake of NO3 by phytoplankton
# u_cp        |??            |Uptake of C by phytoplankton
# u_zp        |??            |Uptake of phytoplankton C by zooplankton   
# u_sp        |??            |Consumption rate of phytoplankton by shellfish
# u_np        |??            |??
# m_p         |??            |Phytoplankton C sinking rate
# excre_p     |??            |Phytoplankton excretion
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ 

# ~ ~ ~ SUBROUTINES/FUNCTIONS CALLED ~ ~ ~
import numpy as np
import readcsv as rd
import readphyto as rdphy
import readzoo as rdz
import readshell as rds
import radiation as rad
import readbox as rdbox
import num_shellfish as numsh
import riverinput as inr
import temp1 as tp
import startdat as sd
import runshell as rsh
# ~ ~ ~ END SPECIFICATIONS ~ ~ ~

'''
Calculate the temperature effect function of phytoplankton
'''
def temp_p(t):
    temp_p = rdphy.k_op*np.exp(rdphy.t_ap/rdphy.t_op-rdphy.t_ap/tp.get_temp_h(t))\
             *(1+np.exp(rdphy.t_alp/tp.get_temp_h(t)-rdphy.t_alp/rdphy.t_lp)\
             +np.exp(rdphy.t_ahp/rdphy.t_hp-rdphy.t_ahp/tp.get_temp_h(t)))**(-1)
    return temp_p

temp_p(0)
tp.get_temp_h(0)
'''
Calculate the process of biotization of phytoplankton
'''
# Details can be found in Equation XXXX
def calculate_phyto(i,t,nh,no,nph,cp,cz,v_s):
    q_p = nph/cp
    u_nhp = rdphy.u_nhmp*0.5*rd.time_step*(nh/(nh+rdphy.x_pnh*2))
    u_nop = rdphy.u_nomp*0.5*rd.time_step*(no/(no+rdphy.x_pno*10))
    u_cp = rad.f_l(rdbox.get_h(t),t)*cp*np.array(temp_p(t))*rdphy.g_pm*0.5*rd.time_step*abs(1-rdphy.q_pmin/q_p)
    u_zp = cz*rdz.u_czm*rd.time_step*(cp/(cp+rdz.x_pz))*np.minimum(q_p/rdz.q_z,1)
    u_sp = rsh.temp_s(t)*rds.u_m_s*rd.time_step*cp*v_s**(2/3)
    u_np = nph*temp_p(t)*(u_nhp+u_nop)/(1+np.exp((q_p-rdphy.q_pmax)/rdphy.q_poff))    
    m_p = cp*(rdphy.s_pmin*rd.time_step+rdphy.s_p*rd.time_step*abs(rdphy.q_pmax-q_p))  
    excre_p = rdphy.e_up*u_np+rdphy.r_p*rd.time_step*temp_p(t)*cp*q_p 
    cp_next = cp+u_cp-rdphy.r_p*rd.time_step*temp_p(t)*cp\
              -u_zp-u_sp*numsh.shellfish_num(t)/rdbox.get_v(t)\
              -m_p+np.array(inr.source_river(t,"cp"))/rdbox.get_v(t)*rd.time_step*sd.r_river
    nph_next = nph+(1-rdphy.e_up)*u_np-rdphy.r_p*rd.time_step*temp_p(t)*nph\
               -q_p*u_zp-q_p*u_sp*numsh.shellfish_num(t)/rdbox.get_v(t)\
               -q_p*m_p+np.array(inr.source_river(t,"nph"))/rdbox.get_v(t)*rd.time_step*sd.r_river
    return cp_next, nph_next, q_p, u_zp, u_sp, u_np, u_nop, u_nhp, m_p, excre_p                      
