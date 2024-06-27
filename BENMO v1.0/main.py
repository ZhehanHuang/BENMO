# subroutine main

# ~ ~ ~ PURPOSE ~ ~ ~
# this is the main routine to calculate the nutrients in different zones

# ~ ~ ~ INCOMING VARIABLES ~ ~ ~
# name        |units         |definition
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# temp_data   |NA            |original data from csv file (envi_T_min.csv)
# years       |none          |years of the model
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

# ~ ~ ~ LOCAL DEFINITIONS ~ ~ ~
# name        |units         |definition
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ 

# ~ ~ ~ SUBROUTINES/FUNCTIONS CALLED ~ ~ ~
import numpy as np
import pandas as pd
import tqdm
import readcsv as rd
import startdat as sd
import seainput1 as ins
import runphyto as rphy
import runzoo as rzoo
import runshell as rsh
import runfish as rf
import runseaweed as ra
import runnitrogen as rn
import runexchange as rex 
import os
# ~ ~ ~ END SPECIFICATIONS ~ ~ ~

'''
Set empty variables
'''
# global parameter
i = 0

# shellfish
v_s = np.zeros((rd.num_step,5))
e_s = np.zeros((rd.num_step,5))
e_r_s = np.zeros((rd.num_step,5))

# fish
v_f = np.zeros((rd.num_step,5))
e_f = np.zeros((rd.num_step,5))
e_r_f = np.zeros((rd.num_step,5))

# nitrogen
nh = np.zeros((rd.num_step,5))
no = np.zeros((rd.num_step,5))
don = np.zeros((rd.num_step,5))
pon = np.zeros((rd.num_step,5))
poc = np.zeros((rd.num_step,5))
son = np.zeros((rd.num_step,5))
soc = np.zeros((rd.num_step,5))

# phytoplankton
nph = np.zeros((rd.num_step,5))
cp = np.zeros((rd.num_step,5))

# zooplankton
ez = np.zeros((rd.num_step,5))
cz = np.zeros((rd.num_step,5))

# seaweed
na = np.zeros((rd.num_step,5))
ca = np.zeros((rd.num_step,5))

# 额外变量输出
don_nh = np.zeros((rd.num_step,5))
son_nh = np.zeros((rd.num_step,5))
pon_nh = np.zeros((rd.num_step,5))
excre_s_nh = np.zeros((rd.num_step,5))
excre_f_nh = np.zeros((rd.num_step,5))
excre_z_nh = np.zeros((rd.num_step,5))
source_point_nh = np.zeros((rd.num_step,5))
source_river_nh = np.zeros((rd.num_step,5))
source_ponds_nh = np.zeros((rd.num_step,5))
source_atmos_nh = np.zeros((rd.num_step,5))
nh_exchange = np.zeros((rd.num_step,5))
u_1 = np.zeros((rd.num_step,5))
m_z1 = np.zeros((rd.num_step,5))
m_s1 = np.zeros((rd.num_step,5))
m_f1 = np.zeros((rd.num_step,5))
m_p1 = np.zeros((rd.num_step,5))
excre_p_nh = np.zeros((rd.num_step,5))
excre_a_nh = np.zeros((rd.num_step,5))
u_nhp_nh = np.zeros((rd.num_step,5))
nit_nh = np.zeros((rd.num_step,5))
source_point_no = np.zeros((rd.num_step,5))
source_river_no = np.zeros((rd.num_step,5))
source_ponds_no = np.zeros((rd.num_step,5))
source_sgd_no = np.zeros((rd.num_step,5))
source_atmos_no = np.zeros((rd.num_step,5))

u_nhp_no = np.zeros((rd.num_step,5))
denit_no = np.zeros((rd.num_step,5))
 
tp_new_ou_nh= np.zeros((rd.num_step,5))
tp_new_ou_no= np.zeros((rd.num_step,5))
tp_new_ou_don= np.zeros((rd.num_step,5))
u_nha_nh_all = np.zeros((rd.num_step,5))
u_nha_no_all = np.zeros((rd.num_step,5))

'''
Main part of NPZD model
'''
for t in tqdm.tqdm(range(rd.time_start, rd.time_end, rd.time_step)):
  
    target_time = pd.to_datetime(str(rd.years[0]) + "-01-01") + pd.Timedelta(minutes=t)
    
    '''Input start data'''
    # start data for shellfish and fish
    is_shellfish_start = (target_time.month == rd.t_shellfish_start[0] and\
                          target_time.day == rd.t_shellfish_start[1] and\
                          target_time.hour == rd.t_shellfish_start[2] and\
                          target_time.minute == rd.t_shellfish_start[3])
    is_fish_start = (target_time.month == rd.t_fish_start[0] and\
                     target_time.day == rd.t_fish_start[1] and\
                     target_time.hour == rd.t_fish_start[2] and\
                     target_time.minute == rd.t_fish_start[3])
    
    if is_shellfish_start:
        v_s[i] = sd.v_s
        e_s[i] = sd.e_s
        e_r_s[i] = sd.e_r_s
        
    if is_fish_start:
        v_f[i] = sd.v_f
        e_f[i] = sd.e_f
        e_r_f[i] = sd.e_r_f
          
    # start data for seaweed
    is_seaweed_start = (target_time.month == rd.t_seaweed_start[0] and\
                        target_time.day == rd.t_seaweed_start[1] and\
                        target_time.hour == rd.t_seaweed_start[2] and\
                        target_time.minute == rd.t_seaweed_start[3])
    
    if is_seaweed_start:
        na[i] = sd.st_seaweed['na mg N/m3'].loc[sd.st_seaweed['na mg N/m3']\
                                           .index == target_time.year] 
        ca[i] = sd.st_seaweed['ca mg C/m3'].loc[sd.st_seaweed['ca mg C/m3']\
                                           .index == target_time.year]

    # start data for nitrogen, phytoplankton and zooplankton
    if t == 0:
        nh[i] = sd.nh
        no[i] = sd.no
        don[i] = sd.don
        nph[i] = sd.nph
        cp[i] = sd.cp
        ez[i] = sd.ez
        cz[i] = sd.cz
        pon[i] = sd.pon
        poc[i] = sd.poc
        son[i] = sd.son
        soc[i] = sd.soc
    
    '''Calculate the process of biotization'''
    # phytoplankton
    cp[i+1] = rphy.calculate_phyto(i,t,nh[i],no[i],nph[i],cp[i],cz[i],v_s[i])[0]
    cp[i+1] = np.maximum(np.minimum(900, cp[i+1]),10)
    nph[i+1] = rphy.calculate_phyto(i,t,nh[i],no[i],nph[i],cp[i],cz[i],v_s[i])[1]
    nph[i+1] = np.maximum(np.minimum(150, nph[i+1]),2)
    q_p = rphy.calculate_phyto(i,t,nh[i],no[i],nph[i],cp[i],cz[i],v_s[i])[2]
    q_p = np.minimum(0.25, q_p)
    u_zp = rphy.calculate_phyto(i,t,nh[i],no[i],nph[i],cp[i],cz[i],v_s[i])[3]
    u_sp = rphy.calculate_phyto(i,t,nh[i],no[i],nph[i],cp[i],cz[i],v_s[i])[4]
    u_np = rphy.calculate_phyto(i,t,nh[i],no[i],nph[i],cp[i],cz[i],v_s[i])[5]
    u_nop = rphy.calculate_phyto(i,t,nh[i],no[i],nph[i],cp[i],cz[i],v_s[i])[6]
    u_nhp = rphy.calculate_phyto(i,t,nh[i],no[i],nph[i],cp[i],cz[i],v_s[i])[7]
    m_p = rphy.calculate_phyto(i,t,nh[i],no[i],nph[i],cp[i],cz[i],v_s[i])[8]
    # m_p1[i] = m_p
    excre_p = rphy.calculate_phyto(i,t,nh[i],no[i],nph[i],cp[i],cz[i],v_s[i])[9]
    
    # zooplankton
    cz[i+1] = rzoo.calculate_zoo(i,t,u_zp,ez[i],cz[i],poc[i])[0]
    cz[i+1] = np.maximum(np.minimum(400, cz[i+1]),0.1)
    ez[i+1] = rzoo.calculate_zoo(i,t,u_zp,ez[i],cz[i],poc[i])[1]
    ez[i+1] = np.maximum(np.minimum(800, ez[i+1]),0.01)
    excre_z = rzoo.calculate_zoo(i,t,u_zp,ez[i],cz[i],poc[i])[2]
    faece_z = rzoo.calculate_zoo(i,t,u_zp,ez[i],cz[i],poc[i])[3]
    m_z = rzoo.calculate_zoo(i,t,u_zp,ez[i],cz[i],poc[i])[4]
    # m_z1[i] = m_z
    
    # shellfish
    v_s[i+1] = rsh.calculate_shellfish(i,t,q_p,u_sp,e_s[i],v_s[i],e_r_s[i],poc[i])[0]
    e_s[i+1] = rsh.calculate_shellfish(i,t,q_p,u_sp,e_s[i],v_s[i],e_r_s[i],poc[i])[1]
    e_r_s[i+1] = rsh.calculate_shellfish(i,t,q_p,u_sp,e_s[i],v_s[i],e_r_s[i],poc[i])[2]
    m_s = rsh.calculate_shellfish(i,t,q_p,u_sp,e_s[i],v_s[i],e_r_s[i],poc[i])[3]
    # m_s1[i] = m_s
    excre_s = rsh.calculate_shellfish(i,t,q_p,u_sp,e_s[i],v_s[i],e_r_s[i],poc[i])[4]
    faece_s = rsh.calculate_shellfish(i,t,q_p,u_sp,e_s[i],v_s[i],e_r_s[i],poc[i])[5]
    u_so = rsh.calculate_shellfish(i,t,q_p,u_sp,e_s[i],v_s[i],e_r_s[i],poc[i])[6]
    
    # fish
    v_f[i+1] = rf.calculate_fish(i,t,e_f[i],v_f[i],e_r_f[i])[0]
    e_f[i+1] = rf.calculate_fish(i,t,e_f[i],v_f[i],e_r_f[i])[1]
    e_r_f[i+1] = rf.calculate_fish(i,t,e_f[i],v_f[i],e_r_f[i])[2]
    excre_f = rf.calculate_fish(i,t,e_f[i],v_f[i],e_r_f[i])[3]
    faece_f = rf.calculate_fish(i,t,e_f[i],v_f[i],e_r_f[i])[4]
    w_f = rf.calculate_fish(i,t,e_f[i],v_f[i],e_r_f[i])[5]
    m_f = rf.calculate_fish(i,t,e_f[i],v_f[i],e_r_f[i])[6]
    # m_f1[i] = m_f
    
    # seaweed
    ca[i+1] = ra.calculate_seaweed(i,t,target_time,nh[i],no[i],na[i],ca[i])[0]
    na[i+1] = ra.calculate_seaweed(i,t,target_time,nh[i],no[i],na[i],ca[i])[1]
    excre_a = ra.calculate_seaweed(i,t,target_time,nh[i],no[i],na[i],ca[i])[2]
    u_nha_nh = ra.calculate_seaweed(i,t,target_time,nh[i],no[i],na[i],ca[i])[3]
    # u_1[i] = u_nha_nh
    u_nha_no = ra.calculate_seaweed(i,t,target_time,nh[i],no[i],na[i],ca[i])[4]
    
    # nitrogen
    pon[i+1] = rn.calculate_pon(i,t,pon[i],son[i],faece_z,q_p,faece_s,u_so,faece_f,w_f)
    poc[i+1] = rn.calculate_poc(i,t,poc[i],soc[i],faece_z,faece_s,u_so,faece_f,w_f)
    no[i+1] = rn.calculate_no(i,t,nh[i],no[i],u_np,u_nop,u_nhp,u_nha_no)[0]
    no[i+1] = np.maximum(0.1, no[i+1])
    nh[i+1] = rn.calculate_nh(i,t,nh[i],don[i],son[i],pon[i],excre_p,excre_z,\
                              excre_s,excre_f,excre_a,u_np,u_nhp,u_nop,u_nha_nh)[0]
    nh[i+1] = np.maximum(0.01, nh[i+1])
    # excre_p_nh[i] = rn.calculate_nh(i,t,nh[i],don[i],son[i],pon[i],excre_p,excre_z,\
    #                           excre_s,excre_f,excre_a,u_np,u_nhp,u_nop,u_nha_nh)[1]
    # excre_a_nh[i] = rn.calculate_nh(i,t,nh[i],don[i],son[i],pon[i],excre_p,excre_z,\
    #                           excre_s,excre_f,excre_a,u_np,u_nhp,u_nop,u_nha_nh)[2]
    # u_nhp_nh[i] = rn.calculate_nh(i,t,nh[i],don[i],son[i],pon[i],excre_p,excre_z,\
    #                           excre_s,excre_f,excre_a,u_np,u_nhp,u_nop,u_nha_nh)[3]
    # nit_nh[i] = rn.calculate_nh(i,t,nh[i],don[i],son[i],pon[i],excre_p,excre_z,\
    #                           excre_s,excre_f,excre_a,u_np,u_nhp,u_nop,u_nha_nh)[4]
    don_nh[i] = rn.calculate_nh(i,t,nh[i],don[i],son[i],pon[i],excre_p,excre_z,\
                              excre_s,excre_f,excre_a,u_np,u_nhp,u_nop,u_nha_nh)[5]
    son_nh[i] = rn.calculate_nh(i,t,nh[i],don[i],son[i],pon[i],excre_p,excre_z,\
                              excre_s,excre_f,excre_a,u_np,u_nhp,u_nop,u_nha_nh)[6]
    pon_nh[i] = rn.calculate_nh(i,t,nh[i],don[i],son[i],pon[i],excre_p,excre_z,\
                              excre_s,excre_f,excre_a,u_np,u_nhp,u_nop,u_nha_nh)[7]
    excre_s_nh[i] = rn.calculate_nh(i,t,nh[i],don[i],son[i],pon[i],excre_p,excre_z,\
                              excre_s,excre_f,excre_a,u_np,u_nhp,u_nop,u_nha_nh)[8]
    excre_f_nh[i] = rn.calculate_nh(i,t,nh[i],don[i],son[i],pon[i],excre_p,excre_z,\
                              excre_s,excre_f,excre_a,u_np,u_nhp,u_nop,u_nha_nh)[9]
    excre_z_nh[i] = rn.calculate_nh(i,t,nh[i],don[i],son[i],pon[i],excre_p,excre_z,\
                              excre_s,excre_f,excre_a,u_np,u_nhp,u_nop,u_nha_nh)[10]
    # source_point_nh[i] = rn.calculate_nh(i,t,nh[i],don[i],son[i],pon[i],excre_p,excre_z,\
    #                           excre_s,excre_f,excre_a,u_np,u_nhp,u_nop,u_nha_nh)[11]
    # source_river_nh[i] = rn.calculate_nh(i,t,nh[i],don[i],son[i],pon[i],excre_p,excre_z,\
    #                           excre_s,excre_f,excre_a,u_np,u_nhp,u_nop,u_nha_nh)[12]
    # source_ponds_nh[i] = rn.calculate_nh(i,t,nh[i],don[i],son[i],pon[i],excre_p,excre_z,\
    #                           excre_s,excre_f,excre_a,u_np,u_nhp,u_nop,u_nha_nh)[13]
    don[i+1] = rn.calculate_don(i,t,don[i],excre_p,excre_a)
    son[i+1] = rn.calculate_son(i,t,son[i],pon[i],na[i],q_p,m_p,m_z,m_s,m_f)
    soc[i+1] = rn.calculate_soc(i,t,soc[i],poc[i],ca[i],m_p,m_z,m_s,m_f)
   
    '''Calculate water exchange'''
    if t > 0:
        nh[i+1] = rex.water_exchange(i,t,nh[i],nh[i+1],ins.source_sea(t,'nh4'),\
                                      ins.source_sea(int(t+rd.time_step),'nh4'))[0]
        no[i+1] = rex.water_exchange(i,t,no[i],no[i+1],ins.source_sea(t,'no3'),\
                                      ins.source_sea(int(t+rd.time_step),'no3'))[0]
        don[i+1] = rex.water_exchange(i,t,don[i],don[i+1],sd.don[0],sd.don[0])[0]
        nph[i+1] = rex.water_exchange(i,t,nph[i],nph[i+1],sd.nph[0],sd.nph[0])[0]
        cp[i+1] = rex.water_exchange(i,t,cp[i],cp[i+1],sd.cp[0],sd.cp[0])[0]
        ez[i+1] = rex.water_exchange(i,t,ez[i],ez[i+1],sd.ez[0],sd.ez[0])[0]
        cz[i+1] = rex.water_exchange(i,t,cz[i],cz[i+1],sd.cz[0],sd.cz[0])[0]
        pon[i+1] = rex.water_exchange(i,t,pon[i],pon[i+1],sd.pon[0],sd.pon[0])[0]
        poc[i+1] = rex.water_exchange(i,t,poc[i],poc[i+1],sd.poc[0],sd.poc[0])[0] 
        tp_new_ou_nh[i] = rex.water_exchange(i,t,nh[i],nh[i+1],ins.source_sea(t,'nh4'),\
                                      ins.source_sea(int(t+rd.time_step),'nh4'))[1]
        tp_new_ou_no[i] = rex.water_exchange(i,t,no[i],no[i+1],ins.source_sea(t,'no3'),\
                                      ins.source_sea(int(t+rd.time_step),'no3'))[1]
        tp_new_ou_don[i] = rex.water_exchange(i,t,don[i],don[i+1],sd.don[0],sd.don[0])[1]
    
    # son[i+1] = rex.water_exchange(i,t,son[i],son[i+1],sd.son[0],sd.son[0])
    # soc[i+1] = rex.water_exchange(i,t,soc[i],soc[i+1],sd.soc[0],sd.soc[0])


    '''Calculate contribution'''  
    excre_p_nh[i] = rn.calculate_nh(i,t,nh[i],don[i],son[i],pon[i],excre_p,excre_z,\
                                    excre_s,excre_f,excre_a,u_np,u_nhp,u_nop,u_nha_nh)[1]
    excre_a_nh[i] = rn.calculate_nh(i,t,nh[i],don[i],son[i],pon[i],excre_p,excre_z,\
                              excre_s,excre_f,excre_a,u_np,u_nhp,u_nop,u_nha_nh)[2]
    u_nhp_nh[i] = rn.calculate_nh(i,t,nh[i],don[i],son[i],pon[i],excre_p,excre_z,\
                              excre_s,excre_f,excre_a,u_np,u_nhp,u_nop,u_nha_nh)[3]
    nit_nh[i] = rn.calculate_nh(i,t,nh[i],don[i],son[i],pon[i],excre_p,excre_z,\
                              excre_s,excre_f,excre_a,u_np,u_nhp,u_nop,u_nha_nh)[4]
    don_nh[i] = rn.calculate_nh(i,t,nh[i],don[i],son[i],pon[i],excre_p,excre_z,\
                              excre_s,excre_f,excre_a,u_np,u_nhp,u_nop,u_nha_nh)[5]
    son_nh[i] = rn.calculate_nh(i,t,nh[i],don[i],son[i],pon[i],excre_p,excre_z,\
                              excre_s,excre_f,excre_a,u_np,u_nhp,u_nop,u_nha_nh)[6]
    pon_nh[i] = rn.calculate_nh(i,t,nh[i],don[i],son[i],pon[i],excre_p,excre_z,\
                              excre_s,excre_f,excre_a,u_np,u_nhp,u_nop,u_nha_nh)[7]
    excre_s_nh[i] = rn.calculate_nh(i,t,nh[i],don[i],son[i],pon[i],excre_p,excre_z,\
                              excre_s,excre_f,excre_a,u_np,u_nhp,u_nop,u_nha_nh)[8]
    excre_f_nh[i] = rn.calculate_nh(i,t,nh[i],don[i],son[i],pon[i],excre_p,excre_z,\
                              excre_s,excre_f,excre_a,u_np,u_nhp,u_nop,u_nha_nh)[9]
    excre_z_nh[i] = rn.calculate_nh(i,t,nh[i],don[i],son[i],pon[i],excre_p,excre_z,\
                              excre_s,excre_f,excre_a,u_np,u_nhp,u_nop,u_nha_nh)[10]
    source_point_nh[i] = rn.calculate_nh(i,t,nh[i],don[i],son[i],pon[i],excre_p,excre_z,\
                              excre_s,excre_f,excre_a,u_np,u_nhp,u_nop,u_nha_nh)[11]
    source_river_nh[i] = rn.calculate_nh(i,t,nh[i],don[i],son[i],pon[i],excre_p,excre_z,\
                              excre_s,excre_f,excre_a,u_np,u_nhp,u_nop,u_nha_nh)[12]
    source_ponds_nh[i] = rn.calculate_nh(i,t,nh[i],don[i],son[i],pon[i],excre_p,excre_z,\
                              excre_s,excre_f,excre_a,u_np,u_nhp,u_nop,u_nha_nh)[13]
    source_atmos_nh[i] = rn.calculate_nh(i,t,nh[i],don[i],son[i],pon[i],excre_p,excre_z,\
                              excre_s,excre_f,excre_a,u_np,u_nhp,u_nop,u_nha_nh)[14]           
    u_nhp_no[i] = rn.calculate_no(i,t,nh[i],no[i],u_np,u_nop,u_nhp,u_nha_no)[1]
    denit_no[i] = rn.calculate_no(i,t,nh[i],no[i],u_np,u_nop,u_nhp,u_nha_no)[2]
    source_point_no[i] = rn.calculate_no(i,t,nh[i],no[i],u_np,u_nop,u_nhp,u_nha_no)[3]
    source_river_no[i] =rn.calculate_no(i,t,nh[i],no[i],u_np,u_nop,u_nhp,u_nha_no)[4]
    source_ponds_no[i] =rn.calculate_no(i,t,nh[i],no[i],u_np,u_nop,u_nhp,u_nha_no)[5]
    source_sgd_no[i] =rn.calculate_no(i,t,nh[i],no[i],u_np,u_nop,u_nhp,u_nha_no)[6]
    source_atmos_no[i] =rn.calculate_no(i,t,nh[i],no[i],u_np,u_nop,u_nhp,u_nha_no)[7]
    u_nha_nh_all[i] = ra.calculate_seaweed(i,t,target_time,nh[i],no[i],na[i],ca[i])[3]
    u_nha_no_all[i] = ra.calculate_seaweed(i,t,target_time,nh[i],no[i],na[i],ca[i])[4]
    i = i + 1