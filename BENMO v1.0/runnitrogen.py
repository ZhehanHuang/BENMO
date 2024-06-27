# subroutine runnitrogen

# ~ ~ ~ PURPOSE ~ ~ ~
# this subroutine calculate the process of nitrogen

# ~ ~ ~ INCOMING VARIABLES ~ ~ ~
# name        |units         |definition
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# num_step    |NA            |number of time steps 
# time_step   |min           |time step the model used
# k_nit_20    |1/d           |[environment] Water-column nitrification rate 
#                            |at 20 degree
# kt_nit      |NA            |[environment] temperature coefficient for 
#                            |nitrification
# x_nh        |g N/m^3       |[environment] half saturation constant for 
#                            |ammonium cons
# poro        |NA            |[environment] volumetric porosity
# t_k_c_nit   |K             |[environment] critical temperature for 
#                            |nitrification
# x_do        |NA            |[environment] half saturation constant for oxygen
#                            |inhib
# do          |mg/L          |[environment] ???
# k_denit_20  |1/d           |[environment] Water-column denitrification rate 
#                            |at 20 degree
# kt_denit    |NA            |[environment] temperature coefficient for 
#                            |denitrification
# x_no        |g N/m^3       |[environment] half saturation constant for 
#                            |nitrate cons
# t_k_c_den   |K             |[environment] critical temperature for 
#                            |denitrification
# k_sr	      |1/min	     |[environment] Nitrogen and carbon release rate
# k_db	      |1/min	     |[environment] Sediment N and C bury rate
# q_o	      |mg N/mg C	 |[environment] N-quota of particulate detrital 
#                            |organics
# r_don	      |NA		     |[environment] DON fraction of phytoplankton/
#                            |seaweed excretion
# k_or	      |1/min	     |[environment] Water-column DON remineralisation 
#                            |rate
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

# ~ ~ ~ SUBROUTINES/FUNCTIONS CALLED ~ ~ ~
import numpy as np
import readcsv as rd
import readall as rdall
import readzoo as rdz
import readshell as rdsh
import readfish as rdf
import readenv as rden
import readbox as rdbox
import num_shellfish as numsh
import num_fish as numf
import riverinput as rin
import temp1 as tp
import startdat as sd
# ~ ~ ~ END SPECIFICATIONS ~ ~ ~  

'''
Calculate k_nit and k_denit for a given time
'''
def get_k_nit(t,nh):
    if (tp.get_temp_h(t) < rden.t_k_c_nit).all():
        k_nit = 0
    else:
        k_nit_d = rden.k_nit_20*(rden.kt_nit**(tp.get_temp_h(t)-293))\
                *nh/(nh+rden.x_nh*rden.poro)\
                *rden.do/(rden.do+rden.x_do*rden.poro)
        k_nit = k_nit_d/rd.d_to_min
    return k_nit

def get_k_denit(t,no):
    if (tp.get_temp_h(t) < rden.t_k_c_den).all():
        k_denit = 0
    else:
        k_denit_d = rden.k_denit_20*(rden.kt_denit**(tp.get_temp_h(t)-293))\
                *no/(no+rden.x_no*rden.poro)\
                *(1-rden.do/(rden.do+rden.x_do*rden.poro))
        k_denit = k_denit_d/rd.d_to_min
    return k_denit
   
'''
Calculate the process of nitrogen
'''
def calculate_pon(i,t,pon,son,faece_z,q_p,faece_s,u_so,faece_f,w_f):      
    pon_next = pon+(1-rden.k_sr*rd.time_step-rden.k_db*rd.time_step)*(rdz.q_z*faece_z\
                     +q_p*faece_s*numsh.shellfish_num(t)/rdbox.get_v(t)\
                     -rden.q_o*u_so*numsh.shellfish_num(t)/rdbox.get_v(t)\
                     +rdf.q_f*faece_f*numsh.shellfish_num(t)/rdbox.get_v(t)\
                     +rdf.q_ff*w_f*numsh.shellfish_num(t)/rdbox.get_v(t)\
                     +rden.y_0*rd.time_step*son/rdbox.get_h(t)\
                     -rden.p_0*rd.time_step*pon)
    return pon_next
    
def calculate_poc(i,t,poc,soc,faece_z,faece_s,u_so,faece_f,w_f):
    poc_next = poc+(1-rden.k_sr*rd.time_step-rden.k_db*rd.time_step)*(faece_z\
                        +faece_s*numsh.shellfish_num(t)/rdbox.get_v(t)\
                        -u_so*numsh.shellfish_num(t)/rdbox.get_v(t)\
                        +faece_f*numsh.shellfish_num(t)/rdbox.get_v(t)\
                        +w_f*numsh.shellfish_num(t)/rdbox.get_v(t)\
                        +rden.y_0*rd.time_step*soc/rdbox.get_h(t)\
                        -rden.p_0*rd.time_step*poc)
    return poc_next
    
def calculate_no(i,t,nh,no,u_np,u_nop,u_nhp,u_nha_no):
    nit_no = get_k_nit(t,nh)*rd.time_step*nh
    u_nhp_no = u_np*u_nop/(u_nop+u_nhp)
    denit_no = get_k_denit(t,no)*rd.time_step*no
    source_point_no = np.array(rd.source_point.iloc[1,:])/np.array(rdbox.get_v(t))*rd.time_step*sd.r_point*1
    source_river_no = np.array(rin.source_river(t,'no'))/np.array(rdbox.get_v(t))*rd.time_step*sd.r_river*1.2
    source_ponds_no = np.array(rd.source_pond.iloc[1,:])/np.array(rdbox.get_v(t))*rd.time_step*sd.r_pond*2
    source_sgd_no = np.array(rd.source_sgd.iloc[1,:])/np.array(rdbox.get_v(t))*rd.time_step*0.8
    source_atmos_no = np.array(rd.source_atmo.iloc[1,:])/np.array(rdbox.get_v(t))*rd.time_step
    no_next = no+nit_no-u_nhp_no-u_nha_no-denit_no+source_point_no\
              +source_river_no+source_ponds_no+source_sgd_no+source_atmos_no
    return no_next,u_nhp_no, denit_no, source_point_no,source_river_no ,\
            source_ponds_no ,source_sgd_no ,source_atmos_no                       
    
def calculate_nh(i,t,nh,don,son,pon,excre_p,excre_z,excre_s,excre_f,excre_a,u_np,u_nhp,u_nop,u_nha_nh):    
    excre_p_nh = (1-rden.r_don)*excre_p
    excre_a_nh = (1-rden.r_don)*excre_a
    u_nhp_nh = u_np*u_nhp/(u_nop+u_nhp)
    nit_nh = get_k_nit(t,nh)*rd.time_step*nh    
    don_nh = rden.k_or*rd.time_step*don
    son_nh = rden.k_sr*rd.time_step*son/rdbox.get_h(t)*0.1
    pon_nh = rden.k_sr*rd.time_step*pon
    excre_s_nh = numsh.shellfish_num(t)*excre_s/rdbox.get_v(t)*1
    excre_f_nh = numf.fish_num(t)*excre_f/rdbox.get_v(t)*1  
    excre_z_nh = excre_z
    source_point_nh = np.array(rd.source_point.iloc[0,:])/np.array(rdbox.get_v(t))*rd.time_step*sd.r_point
    source_river_nh = np.array(rin.source_river(t,'nh'))/np.array(rdbox.get_v(t))*rd.time_step*sd.r_river
    source_ponds_nh = np.array(rd.source_pond.iloc[0,:])/np.array(rdbox.get_v(t))*rd.time_step*sd.r_pond
    source_atmos_nh = np.array(rd.source_atmo.iloc[0,:])/np.array(rdbox.get_v(t))*rd.time_step
    nh_next = nh+excre_p_nh+excre_a_nh-u_nhp_nh-u_nha_nh-nit_nh+don_nh\
              +son_nh+pon_nh+excre_s_nh+excre_f_nh+excre_z_nh+source_point_nh\
              +source_river_nh+source_ponds_nh+source_atmos_nh
    return nh_next, excre_p_nh,excre_a_nh, u_nhp_nh, nit_nh,don_nh,son_nh,pon_nh,excre_s_nh,excre_f_nh,excre_z_nh,\
           source_point_nh, source_river_nh, source_ponds_nh ,source_atmos_nh
           
                    
def calculate_don(i,t,don,excre_p,excre_a):                 
    don_next = don+rden.r_don*(excre_p+excre_a)-rden.k_or*rd.time_step*don\
               +np.array(rin.source_river(t,'don'))/np.array(rdbox.get_v(t)*rd.time_step*sd.r_river)\
               +np.array(rd.source_point.iloc[2,:])/np.array(rdbox.get_v(t)*0.36213*rd.time_step*sd.r_point)\
               +np.array(rd.source_pond.iloc[2,:])/np.array(rdbox.get_v(t)*rd.time_step*sd.r_pond)
    return don_next
    
def calculate_son(i,t,son,pon,na,q_p,m_p,m_z,m_s,m_f):
    son_next = son+(rden.p_0*rd.time_step*pon+q_p*m_p+rdz.q_z*m_z)*rdbox.get_h(t)\
               +(rdsh.q_s*m_s+rdf.q_f*m_f+rdall.s_r*rd.time_step*na)/rdbox.area\
               -rden.y_0*rd.time_step*son\
               -(rden.k_sr*rd.time_step+rden.k_db*rd.time_step)*son
    return son_next

def calculate_soc(i,t,soc,poc,ca,m_p,m_z,m_s,m_f):
    soc_next = soc+(rden.p_0*rd.time_step*poc+m_p+m_z)*rdbox.get_h(t)\
               +(m_s+m_f+rdall.s_r*rd.time_step*ca)/rdbox.area\
               -rden.y_0*rd.time_step*soc\
               -(rden.k_sr+rden.k_db)*rd.time_step*soc
    return soc_next