# -*- coding: utf-8 -*-

import num_fish as numf
import num_shellfish as numsh
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
import riverinput as rin
i = 0
num_fish = np.zeros((rd.num_step,5))
num_shell = np.zeros((rd.num_step,5))
for t in tqdm.tqdm(range(rd.time_start, rd.time_end, rd.time_step)):
    num_fish[i] = numf.fish_num(t)
    num_shell[i] = numsh.shellfish_num(t)
    i=i+1

import matplotlib.pyplot as plt
for l in range (5):    
    plt.plot(num_fish[:,l], label='num'+'  '+str(f'area{l+1}'))
    plt.legend()
    plt.tick_params(labelsize=18)
    plt.show()


# shellfish
v_s = np.zeros((rd.num_step,5))
e_s = np.zeros((rd.num_step,5))
e_r_s = np.zeros((rd.num_step,5))

# fish
v_f = np.zeros((rd.num_step,5))
e_f = np.zeros((rd.num_step,5))
e_r_f = np.zeros((rd.num_step,5))


a_test = np.zeros((rd.num_step,5))
for t in tqdm.tqdm(range(rd.time_start, rd.time_end, rd.time_step)):
    a_test[i]=np.array(rin.source_river(t,'nh'))
    i=i+1
    
    
    np.array(rin.source_river(2400000,'nh'))
    
    
    
import readcsv as rd
import runphyto as rphy


rphy.temp_p(0)










