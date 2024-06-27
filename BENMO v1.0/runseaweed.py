# subroutine runseaweed

# ~ ~ ~ PURPOSE ~ ~ ~
# this subroutine calculate the process of biotization of seaweed

# ~ ~ ~ INCOMING VARIABLES ~ ~ ~
# name        |units         |definition
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# u_nhma	  |1/min	     |[seaweed] Seaweed maximum uptake of ammonia N
# x_anh	      |mg N/m^3		 |[seaweed] Half-saturation ammonia-N for seaweed 
#                            |uptake
# u_noma	  |1/min	     |[seaweed] Seaweed maximum uptake of nitrate N
# x_ano	      |mg N/m^3		 |[seaweed] Half-saturation nitrate-N for seaweed
#                            |uptake
# g_am	      |1/min	     |[seaweed] Maximum seaweed growth rate
# q_amin	  |mg N/mg C	 |[seaweed] Minimum seaweed N:C ratio
# q_amax	  |mg N/mg C	 |[seaweed] Maximum seaweed N:C ratio
# q_aoff	  |mg N/mg C	 |[seaweed] Seaweed nitrogen uptake parameter
# e_ua	      |NA		     |[seaweed] Uptake associated excretion of seaweed
# r_a	      |1/min	     |[seaweed] Respiration rate of seaweed
# k_oa	      |NA		     |[seaweed] Reference reaction rate for seaweed at 
#                            |286 K
# t_a_a	      |K		     |[seaweed] Arrhenius temperature of seaweed
# t_al_a	  |K		     |[seaweed] Arrhenius temperature at lower boundary
#                            |for seaweed
# t_l_a	      |K		     |[seaweed] Lower boundary of tolerance range for 
#                            |seaweed
# t_ah_a	  |K		     |[seaweed] Arrhenius temperature at upper boundary
#                            |for seaweed
# t_h_a	      |K		     |[seaweed] Upper boundary of tolerance range for 
#                            |seaweed
# t_oa	      |K		     |[seaweed] Reference temperature
# s_r         |1/min         |[all] Natural mortality of shellfish/seaweed
# s_h         |1/min         |[all] Harvest mortality of shellfish/seaweed
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

# ~ ~ ~ LOCAL DEFINITIONS ~ ~ ~
# name        |units         |definition
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# u_nha       |??            |Potential uptake of ammonium N by seaweed
# u_noa       |??            |Potential uptake of nitrate N by seaweed
# u_na        |??            |Total uptake of N by seaweed
# excre_a     |??            |Seaweed excretion
# u_nha_nh    |??            |??
# u_nha_no    |??            |??
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ 

# ~ ~ ~ SUBROUTINES/FUNCTIONS CALLED ~ ~ ~
import numpy as np
import readcsv as rd
import readall as rdall
import readseaweed as rda
import radiation as rad
import readbox as rdbox
import temp1 as tp
# ~ ~ ~ END SPECIFICATIONS ~ ~ ~    

'''
Calculate the temperature effect function of seaweed
'''
def temp_a(t):
    temp_a = rda.k_oa*np.exp(rda.t_a_a/rda.t_oa-rda.t_a_a/tp.get_temp_h(t))\
             *(1+np.exp(rda.t_al_a/tp.get_temp_h(t)-rda.t_al_a/rda.t_l_a)\
             +np.exp(rda.t_ah_a/rda.t_h_a-rda.t_ah_a/tp.get_temp_h(t)))**(-1)
    return temp_a

'''
Calculate the process of biotization of seaweed
'''
def calculate_seaweed(i,t,target_time,nh,no,na,ca):
    is_first_year = (target_time.year == rd.years[0])
    is_before_start = (target_time.month < rd.t_seaweed_start[0]) or\
                      (target_time.month == rd.t_seaweed_start[0] and\
                       target_time.day < rd.t_seaweed_start[1])
    is_start_end_same_year = (rd.t_seaweed_start[4] == rd.t_seaweed_end[4])
    is_after_end = (target_time.month > rd.t_seaweed_end[0]) or\
                   (target_time.month == rd.t_seaweed_end[0] and\
                    target_time.day > rd.t_seaweed_end[1])
    is_between_start_end = ((target_time.month > rd.t_seaweed_end[0]) and\
                            (target_time.month < rd.t_seaweed_start[0])) or\
                           (((target_time.month == rd.t_seaweed_end[0] and\
                              target_time.day > rd.t_seaweed_end[1])) and \
                            ((target_time.month == rd.t_seaweed_start[0] and\
                              target_time.day < rd.t_seaweed_start[1])))
    if is_start_end_same_year:
        if is_before_start or is_after_end:
            u_nha = np.zeros(5)
            u_noa = np.zeros(5)
            u_na = np.zeros(5)
            excre_a = np.zeros(5)
            na_next = np.zeros(5)
            ca_next = np.zeros(5)
            u_nha_nh = np.zeros(5)
            u_nha_no = np.zeros(5)
        else:
            q_a = np.maximum(np.minimum(na/ca,0.25),0.1)
            u_nha = rda.u_nhma*rd.time_step*(nh/(nh+rda.x_anh*2))
            u_noa = rda.u_noma*rd.time_step*(no/(no+rda.x_ano*2))  
            u_ca = rad.f_l(rdbox.get_h(t),t)*ca*temp_a(t)*rda.g_am*rd.time_step*abs(1-rda.q_amin/q_a)
            u_na = na*temp_a(t)*(u_nha+u_noa)/(1+np.exp((q_a-rda.q_amax)/rda.q_aoff)) 
            excre_a = rda.e_ua*u_na+rda.r_a*rd.time_step*temp_a(t)*ca*q_a
            u_nha_nh = u_na*u_nha/(u_noa+u_nha)
            u_nha_no = u_na*u_noa/(u_noa+u_nha)
            ca_next = ca+u_ca-rda.r_a*rd.time_step*temp_a(t)*ca\
                      -(rdall.s_r+rdall.s_h)*rd.time_step*ca   
            na_next = na+(1-rda.e_ua)*u_na-rda.r_a*rd.time_step*temp_a(t)*na\
                      -(rdall.s_r+rdall.s_h)*rd.time_step*na
    else:
        if is_first_year: 
            if is_before_start:
                u_nha = np.zeros(5)
                u_noa = np.zeros(5)
                u_na = np.zeros(5)
                excre_a = np.zeros(5)
                na_next = np.zeros(5)
                ca_next = np.zeros(5)
                u_nha_nh = np.zeros(5)
                u_nha_no = np.zeros(5)
            else:
                q_a = np.maximum(np.minimum(na/ca,0.25),0.1)
                u_nha = rda.u_nhma*rd.time_step*(nh/(nh+rda.x_anh*2))
                u_noa = rda.u_noma*rd.time_step*(no/(no+rda.x_ano*2))  
                u_ca = rad.f_l(rdbox.get_h(t),t)*ca*temp_a(t)*rda.g_am\
                       *rd.time_step*abs(1-rda.q_amin/q_a)
                u_na = na*temp_a(t)*(u_nha+u_noa)/(1+np.exp((q_a-rda.q_amax)/rda.q_aoff)) 
                excre_a = rda.e_ua*u_na+rda.r_a*rd.time_step*temp_a(t)*ca*q_a
                u_nha_nh = u_na*u_nha/(u_noa+u_nha)
                u_nha_no = u_na*u_noa/(u_noa+u_nha)
                ca_next = ca+u_ca-rda.r_a*rd.time_step*temp_a(t)*ca\
                          -(rdall.s_r+rdall.s_h)*rd.time_step*ca   
                na_next = na+(1-rda.e_ua)*u_na-rda.r_a*rd.time_step*temp_a(t)*na\
                          -(rdall.s_r+rdall.s_h)*rd.time_step*na
        else:
            if is_between_start_end:
                u_nha = np.zeros(5)
                u_noa = np.zeros(5)
                u_na = np.zeros(5)
                excre_a = np.zeros(5)
                na_next = np.zeros(5)
                ca_next = np.zeros(5)
                u_nha_nh = np.zeros(5)
                u_nha_no = np.zeros(5)
            else:
                q_a = np.maximum(np.minimum(na/ca,0.25),0.1)
                u_nha = rda.u_nhma*rd.time_step*(nh/(nh+rda.x_anh*2))
                u_noa = rda.u_noma*rd.time_step*(no/(no+rda.x_ano*2))  
                u_ca = rad.f_l(rdbox.get_h(t),t)*ca*temp_a(t)*rda.g_am\
                       *rd.time_step*abs(1-rda.q_amin/q_a)
                u_na = na*temp_a(t)*(u_nha+u_noa)/(1+np.exp((q_a-rda.q_amax)/rda.q_aoff)) 
                excre_a = rda.e_ua*u_na+rda.r_a*rd.time_step*temp_a(t)*ca*q_a
                u_nha_nh = u_na*u_nha/(u_noa+u_nha)
                u_nha_no = u_na*u_noa/(u_noa+u_nha)
                ca_next = ca+u_ca-rda.r_a*rd.time_step*temp_a(t)*ca\
                          -(rdall.s_r+rdall.s_h)*rd.time_step*ca   
                na_next = na+(1-rda.e_ua)*u_na-rda.r_a*rd.time_step*temp_a(t)*na\
                          -(rdall.s_r+rdall.s_h)*rd.time_step*na
    return ca_next, na_next, excre_a, u_nha_nh, u_nha_no