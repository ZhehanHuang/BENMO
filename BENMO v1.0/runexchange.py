# subroutine runexchange

# ~ ~ ~ PURPOSE ~ ~ ~
# this subroutine calculates the wawter exchange for all process

# ~ ~ ~ SUBROUTINES/FUNCTIONS CALLED ~ ~ ~
import numpy as np
import readbox as rdbox
import waterexchange as we
import readcsv as rd
# ~ ~ ~ END SPECIFICATIONS ~ ~ ~

# def water_exchange(i,t,tp1,tp2,out_tp1,out_tp2):
#     tp_ou_1 = np.append(tp1,out_tp1)
#     tp_ou_2 = np.append(tp2,out_tp2)
#     vol_ou_1 = np.append(rdbox.get_v(t-rd.time_step),1000000000000)
#     vol_ou_2 = np.append(rdbox.get_v(t),1000000000000)
#     tp_new_ou = np.dot((tp_ou_1+tp_ou_2)*0.5,we.func_water_exchange(t))/vol_ou_2               
#     tp_new_ou = tp_ou_2*vol_ou_1/vol_ou_2 + tp_new_ou
#     tp_new = np.array(tp_new_ou[:5])
#     return tp_new



def water_exchange(i,t,tp1,tp2,out_tp1,out_tp2):
    tp_ou_1 = np.append(tp1,out_tp1)
    tp_ou_2 = np.append(tp2,out_tp2)
    vol_ou_1 = np.append(rdbox.get_v(t-rd.time_step),1000000000000)
    vol_ou_2 = np.append(rdbox.get_v(t),1000000000000)
    tp_new_ou = np.dot((tp_ou_1+tp_ou_2)*0.5,we.func_water_exchange(t))
    tp_new_ou_ex = np.array(tp_new_ou[:5])          
    tp_new_ou_1 = tp_ou_2*vol_ou_1/vol_ou_2 + tp_new_ou/vol_ou_2
    tp_new = np.array(tp_new_ou_1[:5])
    return tp_new,tp_new_ou_ex