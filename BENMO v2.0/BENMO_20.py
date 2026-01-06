#!/usr/bin/env python
# encoding: utf-8
"""
@author: Huang Zhehan
@contact: zhehanhuang@stu.xmu.edu.cn
@software: pycharm
@file: BENMO_20.py
@time: 2025/6/9 下午6:41
"""

import tkinter as tk
from tkinter import ttk
import numpy as np
import math
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict

class ToolTip(object):
    def __init__(self, widget, text='widget info'):
        self.waittime = 500
        self.wraplength = 180
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        self.tw = tk.Toplevel(self.widget)
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(self.tw, text=self.text, justify='left',
                         background="#ffffff", relief='solid', borderwidth=1,
                         wraplength=self.wraplength)
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw = None
        if tw:
            tw.destroy()

class ParameterLoader:
    def __init__(self, master):
        self.master = master
        self.master.title("Parameter Loader")
        self.entries = {}
        self.tab_control = ttk.Notebook(master)

        # Initial Conditions tab with series input
        self.add_tab('Initial Conditions', [
            ('PHY', '0.0435, 0.0435, 0.0435, 0.0435, 0.0435, 0.0435, 0.0435, 0.0435, 0.0435, 0.0435, 0.0435, 0.0435, 0.0435, 0.0435, 0.0435, 0.0435, 0.0435, 0.0435, 0.0435, 0.0435', 'mgC/L', 'Initial phytoplankton biomass series'),
            ('ZOO', '0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05', 'mgC/L', 'Initial zooplankton biomass series'),
            ('NH4', '0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.005', 'mgN/L', 'Initial ammonium concentration series'),
            ('NO3', '0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4', 'mgN/L', 'Initial nitrate concentration series'),
            ('ON', '0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1', 'mgN/L', 'Initial organic nitrogen concentration series'),
            ('PO4', '0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08', 'mgP/L', 'Initial phosphate concentration series'),
            ('OP', '0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02', 'mgP/L', 'Initial organic phosphorus concentration series'),
            ('PP', '0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05', 'mgP/L', 'Initial particulate phosphorus concentration series'),
            ('C_SPM', '0.2, 0.05, 0.05, 0.1, 0.1, 0.1, 0.2, 0.1, 0.2, 0.2, 0.2, 0.1, 0.05, 0.05, 0.2, 0.2, 0.2, 0.2, 0.1, 0.2', 'kg/m³', 'Initial concentration of SPM in the water column'),
            ('CBOD', '1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0', 'mgO2/L', 'Initial BCOD concentration series'),
            ('DO', '6.29, 6.29, 6.29, 6.29, 6.29, 6.29, 6.29, 6.29, 6.29, 6.29, 6.29, 6.29, 6.29, 6.29, 6.29, 6.29, 6.29, 6.29, 6.29, 6.29', 'mgO2/L', 'Initial dissolved oxygen concentration series'),
            ('I', '705539, 705539, 705539, 705539, 705539, 705539, 705539, 705539, 705539, 705539, 705539, 705539, 705539, 705539, 705539, 705539, 705539, 705539, 705539, 705539', 'lx/day', 'Initial surface light intensity series'),
            ('H', '6.861743794,40.02595618,35.80033097,4.185279406,16.87358291,9.645099978,2.594711363,10.60004844,4.20606114,6.54189523,7.264580586,17.0592759,38.15586537,22.23773208,4.628117896,2.22255415,7.402312545,5.80439337,16.9039485,2.713267632', 'm', 'Initial water depth series'),
            ('T', '20.04909, 22.73150, 22.99365, 23.83580, 23.85205, 22.99365, 22.99365, 22.99365, 22.99365, 22.99365, 22.99365, 22.99365, 22.99365, 22.99365, 22.99365, 22.99365, 22.99365, 22.99365, 22.99365, 22.99365', '°C', 'Initial temperature series'),
            ('MA', '0,0,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,0,20,20', 'gD/m²', 'Initial macroalgal biomass series'),
            # ('MA', '0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0', 'gD/m²', 'Initial macroalgal biomass series'),
            ('qN', '50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50', 'mgN/gD', 'Macroalgal cell quotas of nitrogen'),
            ('qP', '5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5', 'mgP/gD', 'Macroalgal cell quotas of phosphorus'),
            ('N_SH', '3785804.438, 0, 0, 126336979.3, 4183871.842, 0, 227012456.3, 55525559.94, 0, 377535149.1, 330634099.3, 0, 0, 3679995.239, 1215077545, 61342563.2, 2427940.471, 236319257.8, 18026278.35, 0', '-', 'Initial number of shellfish (individuals) series'),
            ('V_SH', '0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6', 'cm³', 'Initial volume of shellfish series'),
            ('E_SH', '40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40', 'J', 'Initial storage energy series'),
            ('E_R_SH', '10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10', 'J', 'Initial reproductive energy storage'),
            ('N_F', '0, 0, 36308132.92, 11246959.3, 79615100.35, 13866717.11, 1982687.219, 12612384.08, 8110870.655, 667060.6129, 119289.1572, 51539474.79, 73837822.43, 11257092.76, 9406260.351, 0, 11079676.28, 15923493.26, 19494348.39, 4090630.33', '-', 'Initial number of fishes (individuals) series'),
            ('V_F', '5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0', 'cm³', 'Initial volume of fishes series'),
            ('E_F', '42000, 42000, 42000, 42000, 42000, 42000, 42000, 42000, 42000, 42000, 42000, 42000, 42000, 42000, 42000, 42000, 42000, 42000, 42000, 42000', 'J', 'Initial storage energy series'),
            ('E_R_F', '6000, 6000, 6000, 6000, 6000, 6000, 6000, 6000, 6000, 6000, 6000, 6000, 6000, 6000, 6000, 6000, 6000, 6000, 6000, 6000', 'J', 'Initial reproductive energy storage')
        ])

        # Parameters for general biology
        self.add_tab('General Biology', [
            ('A', '21254365.49, 40880593, 43273840.78, 45116392.4, 37734875.14, 34829187.59, 28953727.35, 37689715.86, 44219607.5, 32679776.13, 35679879.05, 43391698.09, 52025867.64, 37394565.25, 34486370.52, 30497248.42, 31422979.23, 25456718.08, 29143514.83, 47734812.71', 'm²', 'Initial area series'),
            ('V', '145842010.5, 1636284824, 1549217822, 188824708, 636722544.2, 335930996.5, 75126565.36, 399512813.7, 185990372.7, 213787671.6, 259199356.6, 740230949.5, 1985092002, 831570323.3, 159606988.6, 67781786.04, 232602713.4, 147760805.7, 492640473.9, 129517322.2', 'm³', 'Initial volume series'),
            ('A_max', '0, 0, 8233002.116, 2196936.866, 8642354.683, 7761237.243, 2156180.323, 4560401.726, 2898244.292, 12249866.43, 18319823.9, 2806045.515, 1921581.758, 6528759.683, 0, 67819.07301, 4290008.942, 0, 10337714.55, 4622971.222', 'm²', 'Maximum macroalgae carrying capacity series'),
            ('S', '34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34', 'g/kg', 'Initial salinity series'),
            ('K_T', 1.068, '-', 'Temperature constant'),
            ('T_opt', 20, '°C', 'Optimal temperature value'),
            ('I_s', 1200000, 'lx/d', 'Optical saturation constant of light intensity'),
            ('K_E', 0.1, '1/m', 'Light extinction coefficient'),
            ('FEED_NH3', 1.52, 'mgN/g', 'Ammonium added to the food web'),
            ('FEED_NO3', 4.17, 'mgN/g', 'Nitrate added to the food web'),
            ('FEED_ON', 45.8, 'mgN/g', 'Organic nitrogen added to the food web'),
            ('FEED_PO4', 1.5, 'mgP/g', 'Phosphate added to the food web'),
            ('FEED_OP', 1.49, 'mgP/g', 'Organic phosphorus added to the food web'),
            ('FEED_PP', 4.5, 'mgP/g', 'Particulte phosphorus added to the food web'),
            ('FEED_CBOD', 2.2, 'mgO2/g', 'BCOD added to the food web'),
            ('W', '4.87, 5.02, 5.12, 4.89, 4.95, 4.87, 5.02, 5.12, 4.65, 5.34, 4.88, 5.21, 4.93, 5.47, 4.56, 5.05, 5.20, 4.79, 5.38, 4.62, 5.15, 4.98, 5.01', 'm/s', 'Wind speed series'),
            ('v', '0.0395, 0.0425, 0.0385, 0.0365, 0.0395, 0.0365, 0.0395, 0.0425, 0.0385, 0.0365, 0.0395, 0.0405, 0.0435, 0.0375, 0.0395, 0.0385, 0.0405, 0.0415, 0.0435', 'm/s', 'Velocity series')
        ])

        # Parameters for phytoplankton
        self.add_tab('Phytoplankton', [
            ('KC_PHY', 2.88/24, '1/d', 'Phytoplankton growth rate constant'),
            ('KN_PHY', 0.02, 'mgN/L', 'Nitrogen half saturation constant for phytoplankton growth'), # 0.05
            ('KP_PHY', 0.08, 'mgP/L', 'Phosphorus half saturation constant for phytoplankton growth'), # 0.15
            ('F_PO4', 0.9, '-', 'Fraction of dissolved inorganic phosphorus'),
            ('kappa_1_PHY', 0.05, '-', 'Temperature sensitivity coefficient below the optimum temperature'),
            ('kappa_2_PHY', 0.05, '-', 'Temperature sensitivity coefficient above the optimum temperature'),
            ('KD_PHY', 0.12/24, '1/d', 'Phytoplankton death rate constant'),
            ('M_max_PHY', 1.0, '-', 'Maximum death rate of phytoplankton'),
            ('K_PHY', 0.8, 'mgC/L', 'Environmental load of phytoplankton'),
            ('KR_PHY', 0.096/24, '1/d', 'Phytoplankton respiration rate constant')
        ])

        # Parameters for zooplankton
        self.add_tab('Zooplankton', [
            ('EFF', 0.5, '-', 'Grazing efficiency'),
            ('K_GRZ', 1.5/24, '1/d', 'Grazing rate constant'),
            ('K_PZ', 0.5, 'mgC/L', 'Half saturation constant for phytoplankton in grazing'),
            ('K_DZ', 0.01/24, '1/d', 'Zooplankton death rate')
        ])

        # Parameters for macroalgal
        self.add_tab('Macroalgal', [
            ('KC_MA', 0.7/24, '1/d', 'Macroalgal growth rate constant'),
            ('kappa_1_MA_T', 0.05, '-', 'Temperature sensitivity coefficient below the optimum temperature'),
            ('kappa_2_MA_T', 0.05, '-', 'Temperature sensitivity coefficient above the optimum temperature'),
            ('kappa_1_MA_S', 0.05, '-', 'Salinity sensitivity coefficient below the optimum salinity'),
            ('kappa_2_MA_S', 0.05, '-', 'Salinity sensitivity coefficient above the optimum salinity'),
            ('S_opt', 35, 'g/kg', 'Optimal salinity value'),
            ('q_0N', 7.2, 'mgN/gD', 'Minimum cell quotas of nitrogen'),
            ('q_0P', 1.0, 'mgP/gD', 'Minimum cell quotas of phosphorus'),
            ('KN_MA', 0.025, 'mgN/L', 'Nitrogen half saturation constant for macroalgal growth'),
            ('K_qN', 9.0, 'mgN/gD', 'half-saturation constants for intracellular nitrogen'),
            ('KP', 0.01, 'mgP/L', 'Phosphorus half saturation constant for macroalgal growth'),
            ('KE_MA', 0.09, '-', 'Algae cell excretion rate constant'),
            ('KP_MA', 0.1, 'mgP/L', 'Phosphorus half saturation constant for macroalgal growth'),
            ('K_qP', 1.3, 'mgP/gD', 'half-saturation constants for intracellular phosphorus'),
            ('KD_MA', 0.01/24, '1/d', 'Macroalgal death rate constant'),
            ('KR_MA', 0.21/24, '1/d', 'Macroalgal respiration rate constant'),
            ('MA_max', 1500, 'gD/m²', 'Maximum macroalgal biomass'),
            ('z', 5.0, 'm', 'Maximum depth of macroalgal growth'),
            ('F_UP_N', 720/24, 'mgN/gD/d', 'Maximum uptake rate of nitrogen by macroalgal'),
            ('F_UP_P', 50/24, 'mgP/gD/d', 'Maximum uptake rate of phosphorus by macroalgal'),
        ])

        # Parameters for shellfish
        self.add_tab('Shellfish', [
            ('DSH', 0.001/24, '1/d', 'Shellfish death rate constant'),
            ('kappa_SH', 0.7, '-', 'Fraction of catabolic flux to growth and maintenance'),
            ('[E_G_SH]', 2500, 'J/cm³', 'Volume-specific costs for structure'),
            ('{p_A_SH}', 440/24, 'J/cm²/d', 'Maximum surface area-specific assimilation rate'),
            ('T_0_SH', 288, 'K', 'Reference temperature'),
            ('T_A_SH', 5530, 'K', 'Arrhenius temperature'),
            ('T_AL_SH', 21000, 'K', 'Arrhenius temperature for the rate of decrease at lower boundary'),
            ('T_AH_SH', 42000, 'K', 'Arrhenius temperature for the rate of increase at upper boundary'),
            ('T_L_SH', 283, 'K', 'Lower boundary temperature of the tolerance range'),
            ('T_H_SH', 296, 'K', 'Upper boundary temperature of the tolerance range'),
            ('H_SH', 0.295, 'mgC/L', 'Half-saturation uptake of phytoplankton'),
            ('[E_m_SH]', 2600, 'J/cm³', 'Maximum reserve density'),
            ('V_p_SH', 0.36, 'cm³', 'Structural body volume at puberty'),
            ('[p_M_SH]', 12.2/24, 'J/cm³/d', 'Volume-specific maintenance rate')
        ])

        # Parameters for fish
        self.add_tab('Fish', [
            ('DF', 0.001/24, '1/d', 'Fish death rate constant'),
            ('kappa_F', 0.85, '-', 'Fraction of catabolic flux to growth and maintenance'),
            ('[E_G_F]', 6200, 'J/cm³', 'Volume-specific costs for structure'),
            ('{p_A_F}', 2250/24, 'J/cm²/d', 'Maximum surface area-specific assimilation rate'),
            ('T_0_F', 283, 'K', 'Reference temperature'),
            ('T_A_F', 6400, 'K', 'Arrhenius temperature'),
            ('T_AL_F', 3200, 'K', 'Arrhenius temperature for the rate of decrease at lower boundary'),
            ('T_AH_F', 32000, 'K', 'Arrhenius temperature for the rate of increase at upper boundary'),
            ('T_L_F', 283, 'K', 'Lower boundary temperature of the tolerance range'),
            ('T_H_F', 296, 'K', 'Upper boundary temperature of the tolerance range'),
            ('H_F', 5, 'g', 'Half-saturation uptake'),
            ('[E_m_F]', 11600, 'J/cm³', 'Maximum reserve density'),
            ('V_p_F', 9, 'cm³', 'Structural body volume at puberty'),
            ('[p_M_F]', 75.3/24, 'J/cm³/d', 'Volume-specific maintenance rate'),
            ('FEED', '0, 0, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0.15, 0, 0.15, 0.15, 0.15, 0.15', 'g/m²/d', 'Fish feeding constant'), # 存疑
            ('M_F', 500, 'g', 'Fish mass when harvested'),
            ('FCR_F', 3.5, '-', 'Feed conversion ratio of fishes')
        ])

        # Parameters for nitrogen
        self.add_tab('Nitrogen', [
            # Ammonium nitrogen
            ('NC_PHY', 0.065, 'mgN/mgC', 'N/C ratio of phytoplankton'),
            ('FON_PHY', 0.5, '-', 'Fraction of ON from phytoplankton death'),
            ('KN_PHY', 0.05, 'mgN/L', 'Nitrogen half saturation constant for phytoplankton growth'),
            ('NC_MA', 0.1, 'mgN/mgC', 'N/C ratio of macroalgal'),
            ('DC_MA', 3.0, 'mgD/mgC', 'D/C ratio of macroalgal'),
            ('KN_MA', 0.025, 'mgN/L', 'Nitrogen half saturation constant for macroalgal growth'),
            ('kappa_R_SH', 0.8, '-', 'Fraction of reproductive reserves fixed in eggs for shellfish'),
            ('mu_V_SH', 2700, 'J/gW', 'Structure energy content of shellfish'),
            ('NC_SH', 0.183, 'mgN/mgC', 'N/C ratio of shellfish'),
            ('mu_CJ', 48.8, 'J/mgC', 'Ratio of carbon to energy content'),
            ('kappa_R_F', 0.8, '-', 'Fraction of reproductive reserves fixed in eggs for fishes'),
            ('mu_V_F', 4400, 'J/gW', 'Structure energy content of fishes'),
            ('NC_F', 0.18, 'mgN/mgC', 'N/C ratio of fishes'),
            ('NC_FEED', 0.18, 'mgN/mgC', 'N/C ratio of fish feed'),
            ('KC_nit', 0.05/24, '1/d', 'Nitrification rate constant'),
            ('K_nit', 2.0, 'mgO2/L', 'Half-saturation constant for nitrification'),
            ('KNC_min', 0.075/24, '1/d', 'Mineralisation of dissolved ON rate constant'),
            # Nitrate nitrogen
            ('KC_den', 0.09/24, '1/d', 'Denitrification rate constant'),
            ('K_den', 0.1, 'mgO2/L', 'Half-saturation constant for denitrification'),
            # Organic nitrogen
            ('mu_ON_sink', 0.041, '-', 'Fraction of organic nitrogen sinking'),
            ('U_SH', 0.045/24, 'm³/cm²/d', 'Shellfish maximum surface area-specific clearance'),
            ('U_F', 380/24, 'mgC/cm²/d', 'Fish maximum surface area-specific clearance')
        ])

        # Parameters for phosphorus
        self.add_tab('Phosphorus', [
            # Inorganic phosphorus
            ('PC_PHY', 0.025, 'mgP/mgC', 'P/C ratio of phytoplankton'),
            ('FOP_PHY', 0.5, '-', 'Fraction of OP from phytoplankton death'),
            ('PC_MA', 0.01, 'mgP/mgC', 'P/C ratio of macroalgal'),
            ('KPC_min', 0.02/24, '1/d', 'Mineralisation of dissolved OP rate constant'),
            # Organic phosphorus
            ('mu_OP_sink', 0.05, '-', 'Fraction of organic phosphorus sinking'),
            ('PC_SH', 0.0025, 'mgP/mgC', 'P/C ratio of shellfish'),
            ('PC_F', 0.005, 'mgP/mgC', 'P/C ratio of fishes'),
            # Particle phosphorus
            ('f_fec', 0.4, '-', 'Fraction of fecal matter that is phosphorus'),
            ('f_PP', 0.6, '-', 'Fraction of PP in fecal matter'),
            ('K_ads', 0.002/24, 'mgP/d', 'Adsorption rate constant for PP'),
            ('K_des', 0.15/24, 'mgP/L/d', 'Desorption rate constant for PP'),
            ('V_set', 0.05/24, 'mgP/m/d', 'Settling rate constant for PP'),
            ('K_resus', 0.3/24, 'mgP/L/d', 'Resuspension rate constant for PP'),
            ('Q_max', 400, 'mgP/kg', 'Langmuir medium maximum capacity for PP')
        ])

        # Parameters for CBOD
        self.add_tab('CBOD', [
            ('OC', 1.42, 'mgO2/mgC', 'O2/C ratio'),
            ('KDC', 0.18, '1/d', 'Oxidation of CBOD rate constant'),
            ('K_BOD', 0.5, 'mgO2/L', 'CBOD half saturation constant for oxidation')
        ])

        # Parameters for dissolved oxygen
        self.add_tab('Dissolved Oxygen', [
            ('a', 3.863, '-', 'Parameter in APHA'),
            ('b', 0.5, '-', 'Parameter in APHA'),
            ('c', 0.5, '-', 'Parameter in APHA'),
            ('d', 0.4, '-', 'Parameter in APHA'),
            ('ROC_MA', 2.69, 'mgO2/mgC', 'Ratio of macroalgal use O2 to produce carbon'),
            ('SOD', 2.0, 'mgO2/L/d·m', 'Sediment oxygen demand rate constant')
        ])

        # Parameters for waterexchange
        self.sea_areas = ['Area1', 'Area2', 'Area3', 'Area4', 'Area5', 'Area6', 'Area7', 'Area8', 'Area9', 'Area10',
                          'Area11', 'Area12', 'Area13', 'Area14', 'Area15', 'Area16', 'Area17', 'Area18', 'Area19',
                          'Area20']

        # Save button
        self.save_button = ttk.Button(master, text="Save Data and Continue", command=self.save_and_continue)
        self.save_button.pack(pady=10, fill=tk.X)

        self.tab_control.pack(expand=1, fill='both')

    def get_sea_areas(self):
        return self.sea_areas

    def add_tab(self, tab_name, parameters):
        tab = ttk.Frame(self.tab_control)
        self.tab_control.add(tab, text=tab_name)
        self.add_parameters(tab, tab_name, parameters)

    def add_parameters(self, tab, tab_name, parameters):
        for name, value, unit, desc in parameters:
            frame = ttk.Frame(tab, height=18)
            frame.pack_propagate(False)
            label = ttk.Label(frame, text=name, width=13)
            label.pack(side=tk.LEFT)
            entry = ttk.Entry(frame, width=20)
            entry.insert(0, str(value))
            entry.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
            unit_label = ttk.Label(frame, text=unit, width=15)
            unit_label.pack(side=tk.LEFT)
            frame.pack(padx=10, pady=3, fill=tk.X)
            self.entries[name] = (entry, tab_name)
            ToolTip(label, desc)

    def save_and_continue(self):
        self.master.quit()  # Quit the main loop

    def get_parameter(self, name):
        entry, tab_name = self.entries[name]
        value_str = entry.get()
        value_list = [float(v) for v in value_str.split(',')]
        return value_list

    def update_initial_values(self, updated_concentrations):
        for name, values in updated_concentrations.items():
            entry, tab_name = self.entries[name]
            new_value_str = ','.join(map(str, values))
            entry.delete(0, tk.END)
            entry.insert(0, new_value_str)

class WaterExchange:
    def __init__(self, parameter_loader, exchange_data_file, outer_sea_conc_file, river_flow_file, outer_sea_scaling, time_step=1):
        self.parameter_loader = parameter_loader
        self.exchange_data_file = exchange_data_file
        self.outer_sea_scaling = outer_sea_scaling or {
            'NO3': 1.0,
            'NH4': 1.0,
            'PO4': 1.0,
        }

        self.sea_areas = [
            'Area1','Area2','Area3','Area4','Area5','Area6','Area7','Area8',
            'Area9','Area10','Area11','Area12','Area13','Area14','Area15','Area16',
            'Area17','Area18','Area19','Area20', 'OuterSea'
            ]

        self.edges = {
        'Edge1': ('Area1', 'Area18'),
        'Edge2': ('Area2', 'Area13'),
        'Edge3': ('Area2', 'OuterSea'),
        'Edge4': ('Area3', 'Area13'),
        'Edge5': ('Area3', 'Area14'),
        'Edge6': ('Area3', 'Area17'),
        'Edge7': ('Area3', 'Area5'),
        'Edge8': ('Area4', 'Area8'),
        'Edge9': ('Area5', 'Area17'),
        'Edge10': ('Area5', 'Area19'),
        'Edge11': ('Area5', 'Area10'),
        'Edge12': ('Area6', 'Area14'),
        'Edge13': ('Area6', 'Area15'),
        'Edge14': ('Area6', 'Area8'),
        'Edge15': ('Area6', 'Area9'),
        'Edge16': ('Area7', 'Area11'),
        'Edge17': ('Area7', 'Area16'),
        'Edge18': ('Area8', 'Area14'),
        'Edge19': ('Area8', 'Area17'),
        'Edge20': ('Area8', 'Area18'),
        'Edge21': ('Area9', 'Area15'),
        'Edge22': ('Area9', 'Area20'),
        'Edge23': ('Area10', 'Area11'),
        'Edge24': ('Area10', 'Area16'),
        'Edge25': ('Area10', 'Area19'),
        'Edge26': ('Area11', 'Area16'),
        'Edge27': ('Area11', 'Area19'),
        'Edge28': ('Area12', 'Area13'),
        'Edge29': ('Area12', 'Area14'),
        'Edge30': ('Area12', 'Area20'),
        'Edge31': ('Area14', 'Area17'),

        'Edge32': ('Area18', 'Area1'),
        'Edge33': ('Area13', 'Area2'),
        'Edge34': ('OuterSea', 'Area2'),
        'Edge35': ('Area13', 'Area3'),
        'Edge36': ('Area14', 'Area3'),
        'Edge37': ('Area17', 'Area3'),
        'Edge38': ('Area5', 'Area3'),
        'Edge39': ('Area8', 'Area4'),
        'Edge40': ('Area17', 'Area5'),
        'Edge41': ('Area19', 'Area5'),
        'Edge42': ('Area10', 'Area5'),
        'Edge43': ('Area14', 'Area6'),
        'Edge44': ('Area15', 'Area6'),
        'Edge45': ('Area8', 'Area6'),
        'Edge46': ('Area9', 'Area6'),
        'Edge47': ('Area11', 'Area7'),
        'Edge48': ('Area16', 'Area7'),
        'Edge49': ('Area14', 'Area8'),
        'Edge50': ('Area17', 'Area8'),
        'Edge51': ('Area18', 'Area8'),
        'Edge52': ('Area15', 'Area9'),
        'Edge53': ('Area20', 'Area9'),
        'Edge54': ('Area11', 'Area10'),
        'Edge55': ('Area16', 'Area10'),
        'Edge56': ('Area19', 'Area10'),
        'Edge57': ('Area16', 'Area11'),
        'Edge58': ('Area19', 'Area11'),
        'Edge59': ('Area13', 'Area12'),
        'Edge60': ('Area14', 'Area12'),
        'Edge61': ('Area20', 'Area12'),
        'Edge62': ('Area17', 'Area14')
        }

        self.time_step = time_step
        self.num_areas = len(self.sea_areas)
        self.outer_sea_conc_file = outer_sea_conc_file
        self.river_flow_file = river_flow_file
        self.V = np.append(self.get_parameter('V'), 1e12)
        self.outer_sea_concentrations = self.load_outer_sea_concentrations()
        self.river_flow_data = self.load_river_flows()

        # 初始化水交换矩阵
        self.water_exchange_matrix = None
        self.num_time_points = None

        # 加载水交换数据并计算矩阵
        self.load_exchange_data()
        self.load_river_flows()
        self.calculate_water_exchange_matrices()
        self.calculate_volume()

    def get_parameter(self, name):
        return self.parameter_loader.get_parameter(name)

    def load_exchange_data(self):
        # 读取水交换数据文件
        df_out_1d = pd.read_csv(self.exchange_data_file, index_col=0)
        list_area_new = [
            '4_to_18', '6_to_10', '10_to_18', '9_to_18', '1_to_12', '9_to_10', '10_to_15', '2_to_12',
            '6_to_15', '2_to_4', '4_to_9', '9_to_15', '2_to_16', '2_to_13', '13_to_16', '11_to_12',
            '11_to_13', '7_to_13', '5_to_13', '5_to_7', '3_to_7', '11_to_19', '8_to_19', '5_to_8',
            '7_to_17', '8_to_14', '0_to_17', '4_to_16', '5_to_14', '1_to_sea', '7_to_16'
        ]

        # 确保数据文件中包含所有所需列
        missing_columns = [col for col in list_area_new if col not in df_out_1d.columns]
        if missing_columns:
            raise ValueError(f"水交换数据中缺少以下列：{missing_columns}")

        # 转换数据为 numpy 数组并重构形状
        df_out_1d = df_out_1d[list_area_new].values
        df_out_1d = df_out_1d.reshape(-1, int(self.time_step / 1), df_out_1d.shape[1])
        df_xh = np.sum(df_out_1d, axis=1)

        # 初始化水交换值数组
        waterex = np.zeros((len(df_xh), len(self.edges)))

        # 计算水交换矩阵的各个边的值
        waterex[:, 0] = np.maximum(df_xh[:, 26], 0)
        waterex[:, 1] = np.maximum(df_xh[:, 4], 0)
        waterex[:, 2] = np.maximum(df_xh[:, 29], 0)
        waterex[:, 3] = np.maximum(df_xh[:, 7], 0)
        waterex[:, 4] = np.maximum(df_xh[:, 13], 0)
        waterex[:, 5] = np.maximum(df_xh[:, 12], 0)
        waterex[:, 6] = np.maximum(df_xh[:, 9], 0)
        waterex[:, 7] = np.maximum(df_xh[:, 20], 0)
        waterex[:, 8] = np.maximum(df_xh[:, 27], 0)
        waterex[:, 9] = np.maximum(df_xh[:, 0], 0)
        waterex[:, 10] = np.maximum(df_xh[:, 10], 0)
        waterex[:, 11] = np.maximum(df_xh[:, 18], 0)
        waterex[:, 12] = np.maximum(df_xh[:, 28], 0)
        waterex[:, 13] = np.maximum(df_xh[:, 19], 0)
        waterex[:, 14] = np.maximum(df_xh[:, 23], 0)
        waterex[:, 15] = np.maximum(df_xh[:, 1], 0)
        waterex[:, 16] = np.maximum(df_xh[:, 8], 0)
        waterex[:, 17] = np.maximum(df_xh[:, 17], 0)
        waterex[:, 18] = np.maximum(df_xh[:, 30], 0)
        waterex[:, 19] = np.maximum(df_xh[:, 24], 0)
        waterex[:, 20] = np.maximum(df_xh[:, 25], 0)
        waterex[:, 21] = np.maximum(df_xh[:, 22], 0)
        waterex[:, 22] = np.maximum(df_xh[:, 5], 0)
        waterex[:, 23] = np.maximum(df_xh[:, 11], 0)
        waterex[:, 24] = np.maximum(df_xh[:, 3], 0)
        waterex[:, 25] = np.maximum(df_xh[:, 6], 0)
        waterex[:, 26] = np.maximum(df_xh[:, 2], 0)
        waterex[:, 27] = np.maximum(df_xh[:, 15], 0)
        waterex[:, 28] = np.maximum(df_xh[:, 16], 0)
        waterex[:, 29] = np.maximum(df_xh[:, 21], 0)
        waterex[:, 30] = np.maximum(df_xh[:, 14], 0)

        waterex[:, 31] = np.maximum(-df_xh[:, 26], 0)
        waterex[:, 32] = np.maximum(-df_xh[:, 4], 0)
        waterex[:, 33] = np.maximum(-df_xh[:, 29], 0)
        waterex[:, 34] = np.maximum(-df_xh[:, 7], 0)
        waterex[:, 35] = np.maximum(-df_xh[:, 13], 0)
        waterex[:, 36] = np.maximum(-df_xh[:, 12], 0)
        waterex[:, 37] = np.maximum(-df_xh[:, 9], 0)
        waterex[:, 38] = np.maximum(-df_xh[:, 20], 0)
        waterex[:, 39] = np.maximum(-df_xh[:, 27], 0)
        waterex[:, 40] = np.maximum(-df_xh[:, 0], 0)
        waterex[:, 41] = np.maximum(-df_xh[:, 10], 0)
        waterex[:, 42] = np.maximum(-df_xh[:, 18], 0)
        waterex[:, 43] = np.maximum(-df_xh[:, 28], 0)
        waterex[:, 44] = np.maximum(-df_xh[:, 19], 0)
        waterex[:, 45] = np.maximum(-df_xh[:, 23], 0)
        waterex[:, 46] = np.maximum(-df_xh[:, 1], 0)
        waterex[:, 47] = np.maximum(-df_xh[:, 8], 0)
        waterex[:, 48] = np.maximum(-df_xh[:, 17], 0)
        waterex[:, 49] = np.maximum(-df_xh[:, 30], 0)
        waterex[:, 50] = np.maximum(-df_xh[:, 24], 0)
        waterex[:, 51] = np.maximum(-df_xh[:, 25], 0)
        waterex[:, 52] = np.maximum(-df_xh[:, 22], 0)
        waterex[:, 53] = np.maximum(-df_xh[:, 5], 0)
        waterex[:, 54] = np.maximum(-df_xh[:, 11], 0)
        waterex[:, 55] = np.maximum(-df_xh[:, 3], 0)
        waterex[:, 56] = np.maximum(-df_xh[:, 6], 0)
        waterex[:, 57] = np.maximum(-df_xh[:, 2], 0)
        waterex[:, 58] = np.maximum(-df_xh[:, 15], 0)
        waterex[:, 59] = np.maximum(-df_xh[:, 16], 0)
        waterex[:, 60] = np.maximum(-df_xh[:, 21], 0)
        waterex[:, 61] = np.maximum(-df_xh[:, 14], 0)

        self.num_time_points = len(waterex)
        self.water_exchange_values = {f'Edge{i + 1}': waterex[:, i] for i in range(len(self.edges))}

    def calculate_water_exchange_matrices(self):
        # 初始化水交换矩阵
        self.water_exchange_matrix = np.zeros((self.num_areas, self.num_areas, self.num_time_points))
        area_index_map = {area: idx for idx, area in enumerate(self.sea_areas)}
        outer_sea_index = self.sea_areas.index('OuterSea')

        # 构建水交换矩阵
        for edge_name, (area_from, area_to) in self.edges.items():
            index_from = area_index_map[area_from]
            index_to = area_index_map[area_to]
            edge_data = self.water_exchange_values[edge_name]

            # 赋值给水交换矩阵
            self.water_exchange_matrix[index_from, index_to, :] = edge_data

        # 保证质量守恒，设置对角线
        for t in range(self.num_time_points):
            for i in range(self.num_areas):
                if i == outer_sea_index:
                    continue  # 不对 OuterSea 行设置守恒
                self.water_exchange_matrix[i, i, t] = -np.sum(self.water_exchange_matrix[i, :, t])

        self.water_exchange_matrix *= 0.5

        return self.water_exchange_matrix

    def load_river_flows(self):
        # 读取流域流量输入数据
        df_river = pd.read_csv(self.river_flow_file)
        return df_river

    def calculate_volume(self, current_time_step=0):
        water_volume_all = np.sum(self.water_exchange_matrix, axis=0).T
        water_volume = water_volume_all[current_time_step, :]
        river_flow = self.river_flow_data.iloc[current_time_step, :]
        water_volume[14] += river_flow.iloc[1]
        water_volume[0] += river_flow.iloc[2]
        water_volume_real = self.V + water_volume
        return water_volume_real

    def load_outer_sea_concentrations(self):
        # 读取外海浓度数据
        df = pd.read_csv(self.outer_sea_conc_file)
        substances = [col for col in df.columns if col != 'Time']
        return {substance: df[substance].values for substance in substances}

    def exchange(self, concentrations, current_time_step):
        if current_time_step >= self.num_time_points:
            raise ValueError("时间步超出可用范围。")

        current_matrix = self.water_exchange_matrix[:, :, current_time_step]
        V_array_old = self.calculate_volume(current_time_step - 1)
        V_array_new = self.calculate_volume(current_time_step)
        outer_sea_index = self.sea_areas.index('OuterSea')
        # current_matrix[outer_sea_index, :] = 0.0
        updated_concentrations = {}

        # 获取当前步外海浓度（按步长索引，如果超限则取最后）
        outer_sea_current_conc = {}
        for sub in concentrations.keys():
            raw_conc = self.outer_sea_concentrations.get(sub, [0.0])
            conc_value = raw_conc[min(current_time_step, len(raw_conc) - 1)]
            scale = self.outer_sea_scaling.get(sub, 1.0)
            outer_sea_current_conc[sub] = conc_value * scale
        # outer_sea_current_conc = {
        #     sub: self.outer_sea_concentrations.get(sub, [0.0])[
        #         min(current_time_step, len(self.outer_sea_concentrations.get(sub, [0.0])) - 1)]
        #     for sub in concentrations.keys()
        # }

        for substance, conc in concentrations.items():
            conc_array = np.array(conc, dtype=np.float64)
            if len(conc_array) == len(self.sea_areas) - 1:
                conc_array = np.append(conc_array, outer_sea_current_conc[substance])

            # new_conc = fast_exchange_step(
            #     current_matrix,
            #     conc_array.copy(),
            #     V_array_old,
            #     V_array_new,
            #     outer_sea_index,
            #     outer_sea_current_conc[substance]
            # )

            # 确保 OuterSea 的浓度固定
            conc_array[outer_sea_index] = outer_sea_current_conc[substance]

            # 总质量守恒公式：质量转移 + 稀释调整
            exchanged_mass = np.dot(current_matrix, conc_array)
            new_conc = (conc_array * V_array_old + exchanged_mass) / V_array_new
            new_conc[outer_sea_index] = outer_sea_current_conc[substance]  # OuterSea 保持恒定

            updated_concentrations[substance] = new_conc.tolist()

        return updated_concentrations

    def get_water_exchange_matrix(self, t):
        # 获取某个时间步长的水交换矩阵
        if t % self.time_step != 0:
            raise ValueError("错误: 输入的时间不符合时间步长。")

        time_index = int(t / self.time_step)
        if time_index >= self.num_time_points:
            raise ValueError("错误: 超出可用的时间范围。")

        return self.water_exchange_matrix[:, :, time_index]

class Phytoplankton:
    def __init__(self, parameter_loader):
        self.parameter_loader = parameter_loader
        self.reload_parameters()
        self.cache = {}  # Cache for computed values

        # Growth-related constants from the 'Phytoplankton' tab
        self.KC_PHY = self.get_parameter('KC_PHY')[0]  # Scalar value
        self.KN_PHY = self.get_parameter('KN_PHY')[0]
        self.KP_PHY = self.get_parameter('KP_PHY')[0]
        self.F_PO4 = self.get_parameter('F_PO4')[0]
        self.KT = self.get_parameter('K_T')[0]
        self.T_opt = self.get_parameter('T_opt')[0]
        self.KE_P = self.get_parameter('K_E')[0]
        self.kappa_1 = self.get_parameter('kappa_1_PHY')[0]
        self.kappa_2 = self.get_parameter('kappa_2_PHY')[0]
        self.I_s = self.get_parameter('I_s')[0]

        # Death-related constants from the 'Phytoplankton' tab
        self.KR_PHY = self.get_parameter('KR_PHY')[0]
        self.KD_PHY = self.get_parameter('KD_PHY')[0]
        self.M_max_PHY = self.get_parameter('M_max_PHY')[0]
        self.K_PHY = self.get_parameter('K_PHY')[0]
        self.KR_T = self.get_parameter('K_T')[0]
        self.KE_MA = 0.00

    def get_parameter(self, name):
        return self.parameter_loader.get_parameter(name)

    def reload_parameters(self):
        get = self.parameter_loader.get_parameter
        self.T = get('T')
        self.I = get('I')
        self.H = get('H')
        self.A = get('A')
        self.V = get('V')
        self.PHY = get('PHY')
        self.NH4 = get('NH4')
        self.NO3 = get('NO3')
        self.PO4 = get('PO4')
        self.MA = get('MA')

    def nutrient_limitation(self):
        NH4_NO3 = [max(nh4 + no3, 0) for nh4, no3 in zip(self.NH4, self.NO3)]
        X_N = [min((nh4_no3) / (self.KN_PHY + nh4_no3), 1) for nh4_no3 in NH4_NO3]
        PO4_non_neg = [max(po4, 0) for po4 in self.PO4]
        X_P = [min(po4 / (self.KP_PHY / self.F_PO4 + po4), 1) for po4 in PO4_non_neg]
        result = [min(max(min(xn, xp), 0), 1) for xn, xp in zip(X_N, X_P)]
        self.cache['nutrient_limitation'] = result
        return result

    def temperature_limitation(self, method=1):
        if 'temperature_limitation' in self.cache:
            return self.cache['temperature_limitation']
        if method == 1:
            result = [self.KT ** (t - self.T_opt) for t in self.T]
        else:
            result = [math.exp(-self.kappa_1 * (t - self.T_opt) ** 2) if t <= self.T_opt
                      else math.exp(-self.kappa_2 * (t - self.T_opt) ** 2) for t in self.T]
        self.cache['temperature_limitation'] = result
        return result

    def light_limitation(self):
        if 'light_limitation' in self.cache:
            return self.cache['light_limitation']

        KE = self.KE_P + self.KE_MA * sum(self.MA) * (sum(self.A) / sum(self.V))

        # Adjust the h/2 value with the limit (Assume 5m is a reasonable limit)
        adjusted_h = [min(h / 2, 5) for h in self.H]

        # Calculate the light factor with the adjusted h values
        light_factor = [(i / 1200000) * math.exp(-KE * adj_h) for i, adj_h in zip(self.I, adjusted_h)]

        # Calculate the result and multiply by 2/adjusted_h
        result = [lf * math.exp(1 - lf) for lf in light_factor]

        self.cache['light_limitation'] = result

        return result

    def growth_rate(self):
        phi_N_PHY = self.nutrient_limitation()
        phi_T_PHY = self.temperature_limitation()
        phi_L_PHY = self.light_limitation()

        GP_PHY = [self.KC_PHY * min(pn, 1) * min(pt, 1) * min(pl, 1) for pn, pt, pl in
                  zip(phi_N_PHY, phi_T_PHY, phi_L_PHY)]
        result = [max(gp, 0) * phy for gp, phy in zip(GP_PHY, self.PHY)]
        self.cache['growth_rate'] = result

        return GP_PHY

    def loss_rate(self):
        """
        Dynamically selects the best `loss_rate` calculation method for each region (each index),
        based on the closest match to `growth_rate` at that index.
        """
        # Check if the result is already cached
        if 'loss_rate' in self.cache and 'loss_rate_method' in self.cache:
            return self.cache['loss_rate']

        # Compute `growth_rate` for all regions
        growth_rate = self.growth_rate()

        # Pre-calculate RES_PHY (common to both methods)
        RES_PHY = [self.KR_PHY * (self.KR_T ** (t - self.T_opt)) for t in self.T]

        # Method 1: Simple
        DPP_PHY_simple = self.KD_PHY
        DP_PHY_simple = [res + DPP_PHY_simple for res in RES_PHY]
        loss_rate_simple = [dp * phy for dp, phy in zip(DP_PHY_simple, self.PHY)]

        # Method 2: Detailed
        DPP_PHY_detailed = [
            self.KD_PHY + self.M_max_PHY / (1 + (self.K_PHY / max(phy, 1e-12)) ** (self.KC_PHY * 11)) for phy in self.PHY
        ]
        DP_PHY_detailed = [res + dpp for res, dpp in zip(RES_PHY, DPP_PHY_detailed)]
        loss_rate_detailed = [dp * phy for dp, phy in zip(DP_PHY_detailed, self.PHY)]

        # Initialize results and method tracking
        selected_loss_rate = []
        selected_methods = []

        # Compare `growth_rate[i]` with `loss_rate_simple[i]` and `loss_rate_detailed[i]` for each region
        for i in range(len(growth_rate)):
            diff_simple = abs(loss_rate_simple[i] - growth_rate[i])
            diff_detailed = abs(loss_rate_detailed[i] - growth_rate[i])

            if diff_simple <= diff_detailed:
                selected_loss_rate.append(loss_rate_simple[i])
                selected_methods.append('simple')
            else:
                selected_loss_rate.append(loss_rate_detailed[i])
                selected_methods.append('detailed')

        # Cache the result and the selected methods for each region
        self.cache['loss_rate'] = selected_loss_rate
        self.cache['loss_rate_method'] = selected_methods

        return DP_PHY_detailed

    def update_PHY(self, GRZ, GRS_PHY):
        GPP = self.growth_rate()
        DPP = self.loss_rate()
        adjusted_h = [min(h / 2, 5) for h in self.H]

        dPHY_dt = [(gpp - dpp - grz - grs) * 2 * adj_h / h for gpp, dpp, grz, grs, adj_h, h in zip(GPP, DPP, GRZ, GRS_PHY, adjusted_h, self.H)]

        # Debugging
        i = 4
        print(f'zone {i+1}')

        change = abs(GPP[i]) + abs(DPP[i]) + abs(GRZ[i]) + abs(GRS_PHY[i])
        print(f"dPHY_dt: {dPHY_dt[i]}; change: {change}; GPP: {GPP[i] / change}; DPP: {DPP[i] / change}; GRZ: {GRZ[i] / change}; GRS_PHY: {GRS_PHY[i] / change}")

        # print(f'GPP:{GPP}')
        # print(f'DPP:{DPP}')

        dPHY_dt = np.real_if_close(dPHY_dt, tol=1e-9)

        self.PHY =[phy + dphy for phy, dphy in zip(self.PHY, dPHY_dt)]

        self.PHY = [max(phy, 1e-12) for phy in self.PHY]

        return self.PHY

    def reset_cache(self):
        """resets the cache"""
        self.cache.clear()

class Zooplankton:
    def __init__(self, parameter_loader):
        self.parameter_loader = parameter_loader
        self.reload_parameters()
        self.cache = {}  # Cache for computed values

        # Grazing-related constants from the 'Zooplankton' tab
        self.EFF = self.get_parameter('EFF')[0]  # Grazing efficiency
        self.K_GRZ = self.get_parameter('K_GRZ')[0]  # Grazing rate constant
        self.K_PZ = self.get_parameter('K_PZ')[0]  # Half saturation constant for phytoplankton in grazing
        self.K_DZ = self.get_parameter('K_DZ')[0]  # Zooplankton death rate

    def get_parameter(self, name):
        return self.parameter_loader.get_parameter(name)

    def reload_parameters(self):
        get = self.parameter_loader.get_parameter
        self.PHY = get("PHY")
        self.ZOO = get("ZOO")

    def grazing_rate(self):
        """Calculate the grazing rate of zooplankton."""
        if 'grazing_rate' in self.cache:
            return self.cache['grazing_rate']

        grazing_rate = [self.K_GRZ * (phy / (phy + self.K_PZ)) for phy in self.PHY]

        self.cache['grazing_rate'] = grazing_rate

        return grazing_rate

    def growth_rate(self):
        """Calculate the growth rate of zooplankton based on grazing efficiency."""
        if 'growth_rate' in self.cache:
            return self.cache['growth_rate']

        GRZ = self.grazing_rate()
        growth_rate = [self.EFF * grz for grz in GRZ]
        self.cache['growth_rate'] = growth_rate
        return growth_rate

    def loss_rate(self):
        """Calculate the loss rate of zooplankton (death rate)."""
        if 'loss_rate' in self.cache:
            return self.cache['loss_rate']

        loss_rate = [self.K_DZ * zoo for zoo in self.ZOO]
        self.cache['loss_rate'] = loss_rate
        return [loss_rate/zoo for loss_rate, zoo in zip(loss_rate, self.ZOO)]

    def update_ZOO(self):
        """Update the zooplankton population based on growth and loss rates."""
        if 'update_ZOO' in self.cache:
            return self.cache['update_ZOO']

        GZ = self.growth_rate()
        DZ = self.loss_rate()
        dZOO_dt = [gz - dz for gz, dz in zip(GZ, DZ)]
        self.ZOO = [zoo + dzoo for zoo, dzoo in zip(self.ZOO, dZOO_dt)]

        i = 4
        change = abs(GZ[i]) + abs(DZ[i])
        print(f"dZOO_dt: {dZOO_dt[i]}; change: {change}; GZ: {GZ[i] / change}; DZ: {DZ[i] / change}")

        self.cache['update_ZOO'] = self.ZOO
        return self.ZOO

    def reset_cache(self):
        """Reset the cache"""
        self.cache.clear()

class Macroalgal:
    def __init__(self, parameter_loader):
        self.parameter_loader = parameter_loader
        self.reload_parameters()
        self.cache = {}  # Cache for computed values

        # Growth-related constants
        self.KC_MA = self.get_parameter('KC_MA')[0]  # Constant growth rate
        self.KT = self.get_parameter('K_T')[0]
        self.T_opt = self.get_parameter('T_opt')[0]
        self.kappa_1 = self.get_parameter('kappa_1_MA_T')[0]
        self.kappa_2 = self.get_parameter('kappa_2_MA_T')[0]
        self.kappa_1_S = self.get_parameter('kappa_1_MA_S')[0]
        self.kappa_2_S = self.get_parameter('kappa_2_MA_S')[0]
        self.I_s = self.get_parameter('I_s')[0]
        self.K_E = self.get_parameter('K_E')[0]
        self.KD_MA = self.get_parameter('KD_MA')[0]
        self.KR_MA = self.get_parameter('KR_MA')[0]
        self.KR_T = self.get_parameter('K_T')[0]
        self.MA_max = self.get_parameter('MA_max')[0]
        self.F_UP_N = self.get_parameter('F_UP_N')[0]
        self.F_UP_P = self.get_parameter('F_UP_P')[0]

        # Nutrient-related constants
        self.q0_N = self.get_parameter('q_0N')[0]
        self.q0_P = self.get_parameter('q_0P')[0]
        self.KN_MA = self.get_parameter('KN_MA')[0]
        self.Kq_N = self.get_parameter('K_qN')[0]
        self.KP = self.get_parameter('KP')[0]
        self.Kq_P = self.get_parameter('K_qP')[0]
        self.K_E_MA_20 = self.get_parameter('KE_MA')[0]
        self.theta_E_MA = self.get_parameter('K_T')[0]

        # Environmental conditions as lists
        self.z = self.get_parameter('z')[0]

        # Cache for internal quotas to avoid recalculating in the same timestep
        self.internal_quotas_cache = None

    def get_parameter(self, name):
        return self.parameter_loader.get_parameter(name)

    def reload_parameters(self):
        get = self.parameter_loader.get_parameter
        self.T = get("T")
        self.S = get("S")
        self.H = get("H")
        self.I = get("I")
        self.MA = get("MA")
        self.q_N = get("qN")
        self.q_P = get("qP")
        self.A = get("A")
        self.A_MA = [a * 0.01 for a in self.A]
        self.V = get("V")
        self.NH4 = get("NH4")
        self.NO3 = get("NO3")
        self.PO4 = get("PO4")

    def temperature_limitation(self, method=1):
        """Temperature limitation function with optional method selection."""
        if 'temperature_limitation' in self.cache:
            return self.cache['temperature_limitation']

        if method == 1:
            result = [1 / (1 + math.exp(-self.KT * (t - self.T_opt) / 1.5)) for t in self.T]
        else:
            result = [math.exp(-self.kappa_1 * (t - self.T_opt) ** 2) if t <= self.T_opt
                      else math.exp(-self.kappa_2 * (t - self.T_opt) ** 2) for t in self.T]

        self.cache['temperature_limitation'] = result
        return result

    def light_limitation(self):
        """Light limitation function."""
        if 'light_limitation' in self.cache:
            return self.cache['light_limitation']

        # 确保初始 MA 只在第一次读取后存储
        if not hasattr(self, 'initial_MA'):
            self.initial_MA = self.get_parameter('MA')  # 存储初始生物量列表

        H_0 = 0.2  # 初始基础深度
        k = 0.005  # 与生物量相关的比例因子

        # 动态计算深度，基于 MA 和初始值
        dynamic_H = [H_0 + k * (ma - ma_0) for ma, ma_0 in zip(self.MA, self.initial_MA)]

        K_MA = [self.K_E + 0.0004 * (max(h / self.z, 1) / min(h, self.z)) for h in dynamic_H]

        light_factor = []
        for i, h, ma, initial_ma, k_ma in zip(self.I, dynamic_H, self.MA, self.initial_MA, K_MA):
            # 确保初始光照限制因子为1，生物量和深度增加导致限制逐渐降低
            if ma <= initial_ma:
                lf = 1.0  # 初始因子为 1
            else:
                lf = (math.e / (k_ma * h)) * (math.exp(-i * math.exp(-k_ma * h) / self.I_s) - math.exp(-i / self.I_s))

            light_factor.append(lf)

        self.cache['light_limitation'] = light_factor
        return light_factor

    def space_limitation(self):
        """Space limitation function based on maximum macroalgal capacity."""
        if 'space_limitation' in self.cache:
            return self.cache['space_limitation']

        result = [1 - (ma / self.MA_max) ** 2 for ma in self.MA]
        self.cache['space_limitation'] = result
        return result

    def salinity_limitation(self, S_opt):
        """Salinity limitation function."""
        if 'salinity_limitation' in self.cache:
            return self.cache['salinity_limitation']

        result = [math.exp(-self.kappa_1_S * (s - S_opt) ** 2) if s <= S_opt
                  else math.exp(-self.kappa_2_S * (s - S_opt) ** 2) for s in self.S]

        self.cache['salinity_limitation'] = result
        return result

    def nutrient_limitation(self):
        """Nutrient limitation function based on nitrogen and phosphorus quotas."""
        if 'nutrient_limitation' in self.cache:
            return self.cache['nutrient_limitation']

        result = [min(1 - self.q0_N / qn, 1 - self.q0_P / qp) for qn, qp in zip(self.q_N, self.q_P)]
        self.cache['nutrient_limitation'] = result
        return result

    def update_internal_quotas(self):
        """Update the internal quotas for nitrogen and phosphorus."""
        if self.internal_quotas_cache is not None:
            return self.internal_quotas_cache

        # Nitrogen quotas
        F_UN_MA = [10**-3 * self.F_UP_N * ((nh4 + no3) / (self.KN_MA + nh4 + no3)) *
                   (self.Kq_N / (self.Kq_N + (q_n - self.q0_N))) * ma
                   for nh4, no3, q_n, ma in zip(self.NH4, self.NO3, self.q_N, self.MA)]
        F_EN_MA = [10**-3 * self.K_E_MA_20 * (self.theta_E_MA ** (t - 20)) * q_n * ma
                   for q_n, ma, t in zip(self.q_N, self.MA, self.T)]
        F_DN_MA = [10**-3 * dma * q_n for dma, q_n in zip(self.calculate_DMA(), self.q_N)]
        dq_N_dt = [fun - fen - fdn for fun, fen, fdn in zip(F_UN_MA, F_EN_MA, F_DN_MA)]

        self.q_N = [max(0, qn + dq) for qn, dq in zip(self.q_N, dq_N_dt)]  # Ensure non-negative quotas

        # i = 4
        # change = abs(F_UN_MA[i]) + abs(F_EN_MA[i]) + abs(F_DN_MA[i])
        # print(f"q_N: {self.q_N[i]}; dq_N_dt: {dq_N_dt[i]}; change: {change}; F_UN_MA: {F_UN_MA[i] / change}; F_EN_MA: {F_EN_MA[i] / change}; F_DN_MA: {F_DN_MA[i] / change}")

        # Phosphorus quotas
        F_UP_MA = [10**-3 * self.F_UP_P * ((po4) / (self.KP + po4)) *
                   (self.Kq_P / (self.Kq_P + (q_p - self.q0_P))) * ma
                   for po4, q_p, ma in zip(self.PO4, self.q_P, self.MA)]
        F_EP_MA = [10**-3 * self.K_E_MA_20 * (self.theta_E_MA ** (t - 20)) * q_p * ma
                   for q_p, ma, t in zip(self.q_P, self.MA, self.T)]
        F_DP_MA = [10**-3 * dma * q_p for dma, q_p in zip(self.calculate_DMA(), self.q_P)]
        dq_P_dt = [fup - fep - fdp for fup, fep, fdp in zip(F_UP_MA, F_EP_MA, F_DP_MA)]

        self.q_P = [max(0, qp + dq) for qp, dq in zip(self.q_P, dq_P_dt)]  # Ensure non-negative quotas

        self.internal_quotas_cache = (F_UN_MA, F_EN_MA, F_DN_MA, self.q_N, F_UP_MA, F_EP_MA, F_DP_MA, self.q_P)
        return self.internal_quotas_cache

    def reset_internal_quotas_cache(self):
        """Reset the cache for internal quotas."""
        self.internal_quotas_cache = None

    def calculate_GMA(self):
        """Calculate the growth of macroalgae."""
        if 'calculate_GMA' in self.cache:
            return self.cache['calculate_GMA']

        phi_T_MA = self.temperature_limitation()
        phi_L_MA = self.light_limitation()
        phi_S_MA = self.space_limitation()
        phi_Sal_MA = self.salinity_limitation(S_opt=self.get_parameter('S_opt')[0])
        self.update_internal_quotas()
        phi_N_MA = self.nutrient_limitation()

        GP_MA = [self.KC_MA * phi_t * phi_l * phi_s * phi_sal * phi_n
                 for phi_t, phi_l, phi_s, phi_sal, phi_n in zip(phi_T_MA, phi_L_MA, phi_S_MA, phi_Sal_MA, phi_N_MA)]

        # i = 4
        # print(f"phi_T_MA: {phi_T_MA[i]}, phi_L_MA: {phi_L_MA[i]}, phi_S_MA: {phi_S_MA[i]}, phi_Sal_MA: {phi_Sal_MA[i]}, phi_N_MA: {phi_N_MA[i]}")

        result = [gp * ma for gp, ma in zip(GP_MA, self.MA)]

        self.cache['calculate_GMA'] = result
        return GP_MA

    def calculate_DMA(self):
        """Calculate the death rate of macroalgae."""
        if 'calculate_DMA' in self.cache:
            return self.cache['calculate_DMA']

        DEA_MA = [self.KD_MA * (self.KR_T ** (t - self.T_opt)) for t in self.T]

        result = [dp * ma for dp, ma in zip(DEA_MA, self.MA)]

        self.cache['calculate_DMA'] = result
        return result

    def calculate_loss_rate(self):
        """Calculate the loss rate of macroalgae (mortality rate)."""
        if 'loss_rate' in self.cache:
            return self.cache['loss_rate']

        RES_MA = [self.KR_MA * (self.KR_T ** (t - self.T_opt)) for t in self.T]
        DEA_MA = [self.KD_MA * (self.KR_T ** (t - self.T_opt)) for t in self.T]
        loss_rate = [res + dea for res, dea in zip(RES_MA, DEA_MA)]

        result = [dp * ma for dp, ma in zip(loss_rate, self.MA)]
        self.cache['loss_rate'] = result
        return loss_rate

    def update_MA(self, MAS, HMA):
        """Update the macroalgae biomass based on growth, death, and harvest."""
        if 'update_MA' in self.cache:
            return self.cache['update_MA']

        GMA = self.calculate_GMA()
        DMA = self.calculate_loss_rate()
        HMA_all = [hma * ma for hma, ma in zip(HMA, self.MA)]

        self.dMA = [mas + gma - dma - hma_all for mas, gma, dma, hma_all in zip(MAS, GMA, DMA, HMA_all)]
        self.MA = [ma + dma for ma, dma in zip(self.MA, self.dMA)]

        i = 4
        change = abs(GMA[i]) + abs(DMA[i]) + abs(HMA[i])
        print(f'dMA:{self.dMA[i]}; change:{change}; GMA:{GMA[i]/change}; DMA:{DMA[i]/change}; HMA:{HMA[i]/change}')

        self.cache['update_MA'] = self.MA

        return self.MA

    def reset_cache(self):
        """Reset the cache"""
        self.cache.clear()

class Shellfish:
    def __init__(self, parameter_loader):
        self.parameter_loader = parameter_loader
        self.reload_parameters()
        self.cache = {}  # Cache for computed values

        # Biological constants from the 'Shellfish' tab
        self.DSH = float(self.get_parameter('DSH')[0])  # Mortality rate (1/day)
        self.U_SH = self.get_parameter('U_SH')[0]  # Maximum specific surface area feeding rate (m³/cm²/day)
        self.kappa_SH = self.get_parameter('kappa_SH')[0]  # Energy allocation to growth and maintenance
        self.E_m_SH = self.get_parameter('[E_m_SH]')[0]  # Maximum storage energy per unit volume (J/cm³)
        self.E_G_SH = self.get_parameter('[E_G_SH]')[0]  # Energy cost per unit volume for growth (J/cm³)
        self.V_p_SH = self.get_parameter('V_p_SH')[0]  # Volume at maturity (cm³)
        self.H_SH = self.get_parameter('H_SH')[0]  # Half-saturation constant for feeding (mgC/m³)
        self.p_A_SH_max = self.get_parameter('{p_A_SH}')[0]  # Maximum specific assimilation rate (J/cm²/day)
        self.p_M_SH_param = self.get_parameter('[p_M_SH]')[0]

        # Temperature-related constants
        self.T_SH_0 = self.get_parameter('T_0_SH')[0]
        self.T_SH_A = self.get_parameter('T_A_SH')[0]
        self.T_SH_AL = self.get_parameter('T_AL_SH')[0]
        self.T_SH_AH = self.get_parameter('T_AH_SH')[0]
        self.T_SH_L = self.get_parameter('T_L_SH')[0]
        self.T_SH_H = self.get_parameter('T_H_SH')[0]

    def get_parameter(self, name):
        return self.parameter_loader.get_parameter(name)

    def reload_parameters(self):
        get = self.parameter_loader.get_parameter
        self.T = [t + 273.15 for t in get('T')]
        self.PHY = get("PHY")
        self.ZOO = get("ZOO")
        self.V = get("V")
        self.H = get("H")
        self.N_SH = np.array(get("N_SH"))
        self.V_SH = np.array(get("V_SH"))
        self.E_SH = get("E_SH")
        self.E_R_SH = get("E_R_SH")

    def temperature_effect(self):
        """Calculate the temperature effect on shellfish metabolic processes."""
        if 'temperature_effect' in self.cache:
            return self.cache['temperature_effect']

        T = self.T[0]  # Assume a constant temperature for simplicity
        k_SH_T = (math.exp(self.T_SH_A / self.T_SH_0 - self.T_SH_A / T) /
                  (1 + math.exp(self.T_SH_AL / T - self.T_SH_AL / self.T_SH_L) +
                   math.exp(self.T_SH_AH / self.T_SH_H - self.T_SH_AH / T)))

        self.cache['temperature_effect'] = k_SH_T
        return k_SH_T

    def functional_response(self):
        """Calculate the functional response for shellfish feeding."""
        if 'functional_response' in self.cache:
            return self.cache['functional_response']

        f_SH = [phy + zoo / (phy + zoo + self.H_SH) for phy, zoo in zip(self.PHY, self.ZOO)]
        self.cache['functional_response'] = f_SH
        return f_SH

    def energy_assimilation_rate(self):
        """Calculate the energy assimilation rate for shellfish."""
        if 'energy_assimilation_rate' in self.cache:
            return self.cache['energy_assimilation_rate']

        k_SH_T = self.temperature_effect()
        f_SH = self.functional_response()
        p_A_SH = [k_SH_T * f * self.p_A_SH_max * v_sh ** (2 / 3) for f, v_sh in zip(f_SH, self.V_SH)]

        self.cache['energy_assimilation_rate'] = p_A_SH
        return p_A_SH

    def maintenance_rate(self):
        """Calculate the maintenance rate for shellfish."""
        if 'maintenance_rate' in self.cache:
            return self.cache['maintenance_rate']

        k_SH_T = self.temperature_effect()
        p_M_SH = [k_SH_T * self.p_M_SH_param * v_sh for v_sh in self.V_SH]

        self.cache['maintenance_rate'] = p_M_SH
        return p_M_SH

    def maturity_maintenance_rate(self):
        """Calculate the maturity maintenance rate for shellfish."""
        if 'maturity_maintenance_rate' in self.cache:
            return self.cache['maturity_maintenance_rate']

        p_J_SH = [min(v_sh, self.V_p_SH) * self.p_M_SH_param * (1 - self.kappa_SH) / self.kappa_SH for v_sh in self.V_SH]

        self.cache['maturity_maintenance_rate'] = p_J_SH
        return p_J_SH

    def catabolic_rate(self):
        """Calculate the catabolic rate for shellfish."""
        if 'catabolic_rate' in self.cache:
            return self.cache['catabolic_rate']

        k_SH_T = self.temperature_effect()
        E_SH_per_V_SH = [e_sh / v_sh for e_sh, v_sh in zip(self.E_SH, self.V_SH)]
        p_C_SH = [(e_sh_v / (self.E_G_SH + self.kappa_SH * e_sh_v)) *
                  (self.E_G_SH * self.p_A_SH_max * v_sh ** (2 / 3) / self.E_m_SH + k_SH_T * self.p_M_SH_param * v_sh)
                  for e_sh_v, v_sh in zip(E_SH_per_V_SH, self.V_SH)]

        self.cache['catabolic_rate'] = p_C_SH
        return p_C_SH

    def reproductive_energy_storage_rate(self):
        """Calculate the reproductive energy storage rate for shellfish."""
        if 'reproductive_energy_storage_rate' in self.cache:
            return self.cache['reproductive_energy_storage_rate']

        p_C_SH = self.catabolic_rate()
        p_J_SH = self.maturity_maintenance_rate()
        dE_R_SH_dt = [(1 - self.kappa_SH) * p_c - p_j for p_c, p_j in zip(p_C_SH, p_J_SH)]
        self.E_R_SH = [e_r_sh + de_r_sh for e_r_sh, de_r_sh in zip(self.E_R_SH, dE_R_SH_dt)]

        self.cache['reproductive_energy_storage_rate'] = (self.E_R_SH, dE_R_SH_dt)
        return self.E_R_SH, dE_R_SH_dt

    def growth_volume(self):
        """Calculate the growth in volume for shellfish."""
        if 'growth_volume' in self.cache:
            return self.cache['growth_volume']

        p_C_SH = self.catabolic_rate()
        p_M_SH = self.maintenance_rate()

        dV_SH_dt = [max((self.kappa_SH * p_c - p_m) / self.E_G_SH, 0) for p_c, p_m in zip(p_C_SH, p_M_SH)]
        self.V_SH = [v_sh + dv_sh for v_sh, dv_sh in zip(self.V_SH, dV_SH_dt)]

        self.cache['growth_volume'] = (self.V_SH, dV_SH_dt)
        return dV_SH_dt

    def population_dynamics(self, HSH):
        """Update shellfish population dynamics."""
        if 'population_dynamics' in self.cache:
            return self.cache['population_dynamics']

        dN_SH_dt = [-self.DSH * n_sh - h_sh * n_sh for n_sh, h_sh in zip(self.N_SH, HSH)]
        self.N_SH = [n_sh + dn_sh for n_sh, dn_sh in zip(self.N_SH, dN_SH_dt)]

        self.cache['population_dynamics'] = self.N_SH
        return dN_SH_dt

    def storage_energy(self):
        """Update shellfish storage energy."""
        if 'storage_energy' in self.cache:
            return self.cache['storage_energy']

        p_A_SH = self.energy_assimilation_rate()
        p_C_SH = self.catabolic_rate()
        dE_SH = [p_a - p_c for p_a, p_c in zip(p_A_SH, p_C_SH)]
        self.E_SH = [e_sh + de_sh for e_sh, de_sh in zip(self.E_SH, dE_SH)]

        self.cache['storage_energy'] = self.E_SH
        return self.E_SH

    def GRS_PHY(self):
        """Calculate the grazing rate of phytoplankton by shellfish."""
        if 'GRS_PHY' in self.cache:
            return self.cache['GRS_PHY']

        k_SH_T = self.temperature_effect()
        N_SH = self.N_SH
        GRS_PHY = [k_SH_T * self.U_SH * v_sh ** (2 / 3) * n_sh / V for v_sh, n_sh, V in zip(self.V_SH, N_SH, self.V)]

        self.cache['GRS_PHY'] = GRS_PHY
        return GRS_PHY

    def update_shellfish(self, HSH):
        """Update the shellfish biomass, energy, and population."""
        if 'update_shellfish' in self.cache:
            return self.cache['update_shellfish']

        self.population_dynamics(HSH)
        self.V_SH, _ = self.growth_volume()
        self.storage_energy()
        self.E_R_SH, _ = self.reproductive_energy_storage_rate()
        grs_phy = [self.GRS_PHY() * phy for phy in self.PHY]

        self.cache['update_shellfish'] = (self.N_SH, self.V_SH, self.E_SH, self.E_R_SH, grs_phy)

        return self.N_SH, self.V_SH, self.E_SH, self.E_R_SH, grs_phy

    def reset_cache(self):
        """Clear the cache at the end of each timestep."""
        self.cache.clear()

class Fish:
    def __init__(self, parameter_loader):
        self.parameter_loader = parameter_loader
        self.reload_parameters()
        self.cache = {}  # Cache for computed values

        # Biological constants from the 'Fish' tab
        self.DF = float(self.get_parameter('DF')[0])
        self.kappa_F = self.get_parameter('kappa_F')[0]
        self.E_m_F = self.get_parameter('[E_m_F]')[0]
        self.E_G_F = self.get_parameter('[E_G_F]')[0]
        self.V_p_F = self.get_parameter('V_p_F')[0]
        self.H_F = self.get_parameter('H_F')[0]
        self.p_A_F_max = self.get_parameter('{p_A_F}')[0]
        self.p_M_F_param = self.get_parameter('[p_M_F]')[0]

        # Temperature-related constants
        self.T_F_0 = self.get_parameter('T_0_F')[0]
        self.T_F_A = self.get_parameter('T_A_F')[0]
        self.T_F_AL = self.get_parameter('T_AL_F')[0]
        self.T_F_AH = self.get_parameter('T_AH_F')[0]
        self.T_F_L = self.get_parameter('T_L_F')[0]
        self.T_F_H = self.get_parameter('T_H_F')[0]

    def get_parameter(self, name):
        return self.parameter_loader.get_parameter(name)

    def reload_parameters(self):
        get = self.parameter_loader.get_parameter
        self.T = [t + 273.15 for t in get('T')]
        self.PHY = get("PHY")
        self.ZOO = get("ZOO")
        self.A = get("A")
        self.V = get("V")
        self.H = get("H")
        self.N_F = np.array(get("N_F"))
        self.V_F = np.array(get("V_F"))
        self.E_F = get("E_F")
        self.E_R_F = get("E_R_F")
        self.FEED = [nf * get('M_F')[0] * get('FCR_F')[0] / 365 * 24 for nf in
                     get('N_F')]

    def temperature_effect(self):
        """Calculate the temperature effect on fish metabolic processes."""
        if 'temperature_effect' in self.cache:
            return self.cache['temperature_effect']

        T = self.T[0]  # Assume a constant temperature for simplicity
        k_F_T = (math.exp(self.T_F_A / self.T_F_0 - self.T_F_A / T) /
                 (1 + math.exp(self.T_F_AL / T - self.T_F_AL / self.T_F_L) +
                  math.exp(self.T_F_AH / self.T_F_H - self.T_F_AH / T)))

        self.cache['temperature_effect'] = k_F_T
        return k_F_T

    def functional_response(self):
        """Calculate the functional response for fish feeding."""
        if 'functional_response' in self.cache:
            return self.cache['functional_response']

        f_F = [feed / (feed + self.H_F) for feed in self.FEED]
        self.cache['functional_response'] = f_F
        return f_F

    def energy_assimilation_rate(self):
        """Calculate the energy assimilation rate for fish."""
        if 'energy_assimilation_rate' in self.cache:
            return self.cache['energy_assimilation_rate']

        k_F_T = self.temperature_effect()
        f_F = self.functional_response()
        p_A_F = [k_F_T * f * self.p_A_F_max * v_f ** (2 / 3) for f, v_f in zip(f_F, self.V_F)]

        self.cache['energy_assimilation_rate'] = p_A_F
        return p_A_F

    def maintenance_rate(self):
        """Calculate the maintenance rate for fish."""
        if 'maintenance_rate' in self.cache:
            return self.cache['maintenance_rate']

        k_F_T = self.temperature_effect()
        p_M_F = [k_F_T * self.p_M_F_param * v_f for v_f in self.V_F]

        self.cache['maintenance_rate'] = p_M_F
        return p_M_F

    def maturity_maintenance_rate(self):
        """Calculate the maturity maintenance rate for fish."""
        if 'maturity_maintenance_rate' in self.cache:
            return self.cache['maturity_maintenance_rate']

        p_J_F = [min(v_f, self.V_p_F) * self.p_M_F_param * (1 - self.kappa_F) / self.kappa_F for v_f in self.V_F]

        self.cache['maturity_maintenance_rate'] = p_J_F
        return p_J_F

    def catabolic_rate(self):
        """Calculate the catabolic rate for fish."""
        if 'catabolic_rate' in self.cache:
            return self.cache['catabolic_rate']

        k_F_T = self.temperature_effect()
        p_M_F = self.maintenance_rate()
        E_F_per_V_F = [e_f / v_f for e_f, v_f in zip(self.E_F, self.V_F)]
        p_C_F = [k_F_T * (e_f_v / (self.E_G_F + self.kappa_F * e_f_v)) *
                 (self.E_G_F * self.p_A_F_max * v_f ** (2 / 3) / self.E_m_F + p_m)
                 for e_f_v, v_f, p_m in zip(E_F_per_V_F, self.V_F, p_M_F)]

        self.cache['catabolic_rate'] = p_C_F
        return p_C_F

    def reproductive_energy_storage_rate(self):
        """Calculate the reproductive energy storage rate for fish."""
        if 'reproductive_energy_storage_rate' in self.cache:
            return self.cache['reproductive_energy_storage_rate']

        p_C_F = self.catabolic_rate()
        p_J_F = self.maturity_maintenance_rate()
        dE_R_F_dt = [(1 - self.kappa_F) * p_c - p_j for p_c, p_j in zip(p_C_F, p_J_F)]
        self.E_R_F = [e_r_f + de_r_f for e_r_f, de_r_f in zip(self.E_R_F, dE_R_F_dt)]

        self.cache['reproductive_energy_storage_rate'] = (self.E_R_F, dE_R_F_dt)
        return self.E_R_F, dE_R_F_dt

    def growth_volume(self):
        """Calculate the growth in volume for fish."""
        if 'growth_volume' in self.cache:
            return self.cache['growth_volume']

        p_C_F = self.catabolic_rate()
        p_M_F = self.maintenance_rate()
        dV_F_dt = [max((self.kappa_F * p_c - p_m) / self.E_G_F, 0) for p_c, p_m in zip(p_C_F, p_M_F)]
        self.V_F = [v_f + dv_f for v_f, dv_f in zip(self.V_F, dV_F_dt)]

        self.cache['growth_volume'] = (self.V_F, dV_F_dt)
        return dV_F_dt

    def population_dynamics(self, HF):
        """Update fish population dynamics."""
        if 'population_dynamics' in self.cache:
            return self.cache['population_dynamics']

        dN_F_dt = [-self.DF * n_f - hf * n_f for n_f, hf in zip(self.N_F, HF)]
        self.N_F = [n_f + dn_f for n_f, dn_f in zip(self.N_F, dN_F_dt)]

        self.cache['population_dynamics'] = self.N_F
        return self.N_F

    def storage_energy(self):
        """Update fish storage energy."""
        if 'storage_energy' in self.cache:
            return self.cache['storage_energy']

        p_A_F = self.energy_assimilation_rate()
        p_C_F = self.catabolic_rate()
        dE_F = [p_a - p_c for p_a, p_c in zip(p_A_F, p_C_F)]
        self.E_F = [e_f + de_f for e_f, de_f in zip(self.E_F, dE_F)]

        self.cache['storage_energy'] = self.E_F
        return self.E_F

    def update_fish(self, HF):
        """Update the fish biomass, energy, and population."""
        if 'update_fish' in self.cache:
            return self.cache['update_fish']

        self.population_dynamics(HF)
        self.V_F, _ = self.growth_volume()
        self.storage_energy()
        self.E_R_F, _ = self.reproductive_energy_storage_rate()

        self.cache['update_fish'] = (self.N_F, self.V_F, self.E_F, self.E_R_F)

        return self.N_F, self.V_F, self.E_F, self.E_R_F

    def reset_cache(self):
        """Clear the cache at the end of each timestep."""
        self.cache.clear()


class ExternalInput:
    def __init__(self, parameter_loader, waterexchange, input_files, input_multipliers):
        self.parameter_loader = parameter_loader
        self.input_files = input_files
        self.waterexchange = waterexchange
        self.substances = ['NH4', 'NO3', 'ON', 'PO4', 'OP', 'CBOD', 'DO']
        self.num_zones = len(self.get_parameter('V'))

        self.input_multipliers = input_multipliers or {
            src: {sub: 1.0 for sub in self.substances}
            for src in ['river', 'groundwater', 'point_source', 'pond', 'atmosphere']
        }

        self.river_data = self.read_river_data(input_files['river'])
        self.static_inputs = self.read_static_inputs([
            input_files['point_source'],
            input_files['groundwater'],
            input_files['pond'],
            input_files['atmosphere']
        ])

    def get_parameter(self, name):
        return self.parameter_loader.get_parameter(name)

    def read_river_data(self, file_path):
        df = pd.read_csv(file_path)
        df['date'] = pd.to_datetime(df['date'])
        unique_times = sorted(df['date'].unique())
        time_map = {t: i for i, t in enumerate(unique_times)}
        df['timestep'] = df['date'].map(time_map)

        river_inputs = defaultdict(lambda: defaultdict(lambda: {sub: 0.0 for sub in self.substances}))
        for _, row in df.iterrows():
            t = row['timestep']
            zone = row['Zone']
            zone_index = int(zone[4:]) - 1
            if 0 <= zone_index < self.num_zones:
                for sub in self.substances:
                    multiplier = self.input_multipliers['river'].get(sub, 1.0)
                    river_inputs[t][zone][sub] += multiplier * row[sub]
        return river_inputs

    def read_static_inputs(self, file_paths):
        combined = {}
        for sub in self.substances:
            combined[sub] = np.zeros(self.num_zones)

        for path, source in zip(file_paths, ['point_source', 'groundwater', 'pond', 'atmosphere']):
            df = pd.read_csv(path)
            for _, row in df.iterrows():
                zone_index = int(row['Zone'][4:]) - 1
                if 0 <= zone_index < self.num_zones:
                    for sub in self.substances:
                        multiplier = self.input_multipliers[source].get(sub, 1.0)
                        combined[sub][zone_index] += multiplier * row[sub]
        return combined

    def get_external_inputs(self, current_time_step):
        V_sea = self.waterexchange.calculate_volume(current_time_step)
        total_mass = {sub: np.zeros(self.num_zones) for sub in self.substances}

        if current_time_step in self.river_data:
            for zone, values in self.river_data[current_time_step].items():
                zone_index = int(zone[4:]) - 1
                if 0 <= zone_index < self.num_zones:
                    for sub in self.substances:
                        total_mass[sub][zone_index] += values[sub]

        for sub in self.substances:
            total_mass[sub] += self.static_inputs[sub]

        total_inputs = {
            sub: [mass / vol if vol > 0 else 0.0 for mass, vol in zip(total_mass[sub], V_sea[:self.num_zones])]
            for sub in self.substances
        }
        return total_inputs

class AmmoniumNitrogen:
    def __init__(self, parameter_loader, phytoplankton, macroalgal, zooplankton, shellfish, fish):
        self.parameter_loader = parameter_loader
        self.reload_parameters()
        self.cache = {}  # Cache for computed values

        # Biological constants from the 'Ammonium Nitrogen' tab
        self.KC_nit = self.get_parameter('KC_nit')[0]
        self.KT_nit = self.get_parameter('K_T')[0]
        self.K_nit = self.get_parameter('K_nit')[0]
        self.KNC_min = self.get_parameter('KNC_min')[0]
        self.KNT_min = self.get_parameter('K_T')[0]

        # Model components
        self.phytoplankton = phytoplankton
        self.macroalgal = macroalgal
        self.zooplankton = zooplankton
        self.shellfish = shellfish
        self.fish = fish

        # External inputs
        self.external_NH4_input = None

    def get_parameter(self, name):
        return self.parameter_loader.get_parameter(name)

    def reload_parameters(self):
        get = self.parameter_loader.get_parameter
        self.T = get("T")
        self.A = get("A")
        self.V = get("V")
        self.H = get("H")
        self.NH4 = get("NH4")
        self.NO3 = get("NO3")
        self.ON = get("ON")
        self.DO = get("DO")
        self.FEED = [nf * get('M_F')[0] * get('FCR_F')[0] for nf in get('N_F')]
        self.FEED_NH3 = [0.2 * get('FEED_NH3')[0] * m / (v * 1000) for m, a, v in
                         zip(self.FEED, get('A'), get('V'))]

    def set_external_input(self, external_input):
        self.external_input = external_input
        return self.external_input

    def phytoplankton_ammonium_release(self):
        """Calculate N1_PHY: Phytoplankton death ammonium release"""
        if 'phytoplankton_ammonium_release' in self.cache:
            return self.cache['phytoplankton_ammonium_release']

        NC_PHY = self.get_parameter('NC_PHY')[0]
        FON_PHY = self.get_parameter('FON_PHY')[0]
        # DPP = self.phytoplankton.loss_rate()
        # N1_PHY = [NC_PHY * dpp * (1 - FON_PHY) for dpp in DPP]
        # self.cache['phytoplankton_ammonium_release'] = N1_PHY
        return [NC_PHY * (1 - FON_PHY)] * 20

    def phytoplankton_ammonium_absorption(self):
        """Calculate Abs1_PHY: Phytoplankton ammonium absorption"""
        if 'phytoplankton_ammonium_absorption' in self.cache:
            return self.cache['phytoplankton_ammonium_absorption']

        NC_PHY = self.get_parameter('NC_PHY')[0]
        KN_PHY = self.get_parameter('KN_PHY')[0]
        GPP = self.phytoplankton.growth_rate()
        PN_PHY = [(nh4 * no3) / ((nh4 + KN_PHY) * (no3 + KN_PHY)) + (nh4 * KN_PHY) / ((nh4 + KN_PHY) * (no3 + KN_PHY))
                  for nh4, no3 in zip(self.NH4, self.NO3)]
        Abs1_PHY = [gpp * pn * NC_PHY for gpp, pn in zip(GPP, PN_PHY)]

        self.cache['phytoplankton_ammonium_absorption'] = Abs1_PHY
        return [pn * NC_PHY for pn in PN_PHY], PN_PHY

    def macroalgal_ammonium_release(self):
        """Calculate N1_MA: Macroalgal death ammonium release"""
        if 'macroalgal_ammonium_release' in self.cache:
            return self.cache['macroalgal_ammonium_release']

        NC_MA = self.get_parameter('NC_MA')[0]
        DC_MA = self.get_parameter('DC_MA')[0]
        F_EN_MA = self.macroalgal.update_internal_quotas()[1]
        F_DN_MA = self.macroalgal.update_internal_quotas()[2]
        q_N_MA = self.macroalgal.update_internal_quotas()[3]
        f_ON_MA = [min(1,(NC_MA / DC_MA) / (q_n_ma / 1000)) for q_n_ma in q_N_MA]
        A_MA = [a * 0.01 for a in self.get_parameter('A')]
        N1_MA = [((f_en + f_dn) * (1 - f_on_ma) * a_ma ) / v
                 for f_en, f_dn, f_on_ma, a_ma, v in zip(F_EN_MA, F_DN_MA, f_ON_MA, A_MA, self.V)]

        # i = 4
        # print(f'N1_MA: {N1_MA[i]}, F_EN_MA: {F_EN_MA[i]}, F_DN_MA: {F_DN_MA[i]}, f_ON_MA: {f_ON_MA[i]}')

        self.cache['macroalgal_ammonium_release'] = N1_MA
        return N1_MA

    def macroalgal_ammonium_absorption(self):
        """Calculate Abs1_MA: Macroalgal ammonium absorption"""
        if 'macroalgal_ammonium_absorption' in self.cache:
            return self.cache['macroalgal_ammonium_absorption']

        KN_MA = self.get_parameter('KN_MA')[0]
        F_UN_MA, _, _, _, _, _, _, _ = self.macroalgal.update_internal_quotas()
        PN_MA = [(nh4 * no3) / ((nh4 + KN_MA) * (no3 + KN_MA)) + (nh4 * KN_MA) / ((nh4 + KN_MA) * (no3 + KN_MA))
                 for nh4, no3 in zip(self.NH4, self.NO3)]
        A_MA = [a * 0.01 for a in self.get_parameter('A')]
        Abs1_MA = [f_un * pn * a_ma / v  for f_un, pn, a_ma, v in zip(F_UN_MA, PN_MA, A_MA, self.V)]

        # i = 4
        # print(f'Abs1_MA: {Abs1_MA[i]}, F_UN_MA: {F_UN_MA[i]}, PN_MA: {PN_MA[i]}, A_MA: {A_MA[i]}, V: {self.V[i]}')

        self.cache['macroalgal_ammonium_absorption'] = Abs1_MA
        return Abs1_MA, PN_MA

    def shellfish_ammonium_excretion(self):
        """Calculate Ex1_SH: Shellfish ammonium excretion"""
        if 'shellfish_ammonium_excretion' in self.cache:
            return self.cache['shellfish_ammonium_excretion']

        kappa_R_SH = self.get_parameter('kappa_R_SH')[0]
        mu_V_SH = self.get_parameter('mu_V_SH')[0]
        NC_PHY = self.get_parameter('NC_PHY')[0]
        mu_CJ = self.get_parameter('mu_CJ')[0]
        NC_SH = self.get_parameter('NC_SH')[0]

        p_C_SH = self.shellfish.catabolic_rate()
        p_A_SH = self.shellfish.energy_assimilation_rate()
        _, dE_R_SH_dt = self.shellfish.reproductive_energy_storage_rate()
        _, dV_SH_dt = self.shellfish.growth_volume()

        Excr_SH = [
            ((p_c - (1 - kappa_R_SH) * de_r_sh - mu_V_SH * dv_sh) * NC_SH + p_a * max(NC_PHY - NC_SH, 0)) / mu_CJ
            for p_c, p_a, de_r_sh, dv_sh in zip(p_C_SH, p_A_SH, dE_R_SH_dt, dV_SH_dt)
        ]

        Ex1_SH = [n_sh * excr_sh / (v * 1000) for n_sh, excr_sh, v in zip(self.shellfish.N_SH, Excr_SH, self.V)]
        self.cache['shellfish_ammonium_excretion'] = Ex1_SH
        return Excr_SH

    def fish_ammonium_excretion(self):
        """Calculate Ex1_F: Fish ammonium excretion"""
        if 'fish_ammonium_excretion' in self.cache:
            return self.cache['fish_ammonium_excretion']

        kappa_R_F = self.get_parameter('kappa_R_F')[0]
        mu_V_F = self.get_parameter('mu_V_F')[0]
        NC_F = self.get_parameter('NC_F')[0]
        mu_CJ = self.get_parameter('mu_CJ')[0]
        NC_FEED = self.get_parameter('NC_FEED')[0]

        p_C_F = self.fish.catabolic_rate()
        p_A_F = self.fish.energy_assimilation_rate()
        _, dE_R_F_dt = self.fish.reproductive_energy_storage_rate()
        _, dV_F_dt = self.fish.growth_volume()

        Excr_F = [
            ((p_c - (1 - kappa_R_F) * de_r_f - mu_V_F * dv_f) * NC_F + p_a * max(NC_FEED - NC_F, 0)) / mu_CJ
            for p_c, p_a, de_r_f, dv_f in zip(p_C_F, p_A_F, dE_R_F_dt, dV_F_dt)
        ]

        Ex1_F = [n_f * excr_f / (v * 1000) for n_f, excr_f, v in zip(self.fish.N_F, Excr_F, self.V)]
        self.cache['fish_ammonium_excretion'] = Ex1_F
        return Excr_F

    def nitrification(self):
        """Calculate NitN: Ammonium nitrification"""
        if 'nitrification' in self.cache:
            return self.cache['nitrification']

        NitN = [self.KC_nit * (self.KT_nit ** (t - 20)) * nh4 * (do / (do + self.K_nit))
                for nh4, do, t in zip(self.NH4, self.DO, self.T)]

        self.cache['nitrification'] = NitN
        return NitN

    def mineralization(self):
        """Calculate MinN: Organic nitrogen mineralization"""
        if 'mineralization' in self.cache:
            return self.cache['mineralization']

        MinN = [self.KNC_min * (self.KNT_min ** (t - 20)) * on for on, t in zip(self.ON, self.T)]

        self.cache['mineralization'] = MinN
        return MinN

    def update_NH4(self):
        """Calculate the ammonium concentration change in the water"""
        if 'update_NH4' in self.cache:
            return self.cache['update_NH4']

        N1_PHY = self.phytoplankton_ammonium_release()
        N1_MA = self.macroalgal_ammonium_release()
        Ex1_SH = self.shellfish_ammonium_excretion()
        Ex1_F = self.fish_ammonium_excretion()
        MinN = self.mineralization()
        NitN = self.nitrification()
        Abs1_PHY = self.phytoplankton_ammonium_absorption()[0]
        Abs1_MA = self.macroalgal_ammonium_absorption()[0]

        dNH4_dt = [n1_phy + n1_ma + ex1_sh + ex1_f + min_n + feed_nh3 - nit_n - abs1_phy - abs1_ma + ex_nh4
                   for n1_phy, n1_ma, ex1_sh, ex1_f, min_n, feed_nh3, nit_n, abs1_phy, abs1_ma, ex_nh4 in
                   zip(N1_PHY, N1_MA, Ex1_SH, Ex1_F, MinN, self.FEED_NH3, NitN, Abs1_PHY, Abs1_MA, self.external_NH4_input)]

        # # Debugging
        # i = 4
        # change = abs(N1_PHY[i]) + abs(N1_MA[i]) + abs(Ex1_SH[i]) + abs(Ex1_F[i]) + abs(MinN[i]) + abs(self.FEED_NH3[i]) + abs(NitN[i])+ abs(Abs1_PHY[i]) + abs(Abs1_MA[i]) + abs(self.external_NH4_input[i])
        # print(f"dNH4_dt: {dNH4_dt[i]}; change: {change}; n1_phy: {N1_PHY[i] / change}; n1_ma: {N1_MA[i] / change}; ex1_sh: {Ex1_SH[i] / change}; ex1_f: {Ex1_F[i] / change}; min_n: {MinN[i] / change}; feed: {self.FEED_NH3[i] / change}; Abs1_PHY: {Abs1_PHY[i] / change}; Abs1_MA: {Abs1_MA[i] / change}; NitN: {NitN[i] / change}; ex_nh4: {self.external_NH4_input[i]/ change}")

        dNH4_dt = np.real_if_close(dNH4_dt, tol=1e-9)

        self.NH4 = [max(0, nh4 + dnh4) for nh4, dnh4 in zip(self.NH4, dNH4_dt)]

        self.cache['update_NH4'] = self.NH4
        return self.NH4

    def reset_cache(self):
        """Clear the cache at the end of each timestep."""
        self.cache.clear()

class NitrateNitrogen:
    def __init__(self, parameter_loader, phytoplankton, macroalgal):
        self.parameter_loader = parameter_loader
        self.reload_parameters()
        self.cache = {}  # Cache dictionary to store calculated results

        # Biological constants from the 'Nitrogen' tab
        self.KC_den = self.get_parameter('KC_den')[0]
        self.KT_den = self.get_parameter('K_T')[0]
        self.K_den = self.get_parameter('K_den')[0]

        # Model components
        self.phytoplankton = phytoplankton
        self.macroalgal = macroalgal

        # External inputs
        self.external_NO3_input = None

    def get_parameter(self, name):
        return self.parameter_loader.get_parameter(name)

    def reload_parameters(self):
        get = self.parameter_loader.get_parameter
        self.T = get("T")
        self.A = get("A")
        self.V = get("V")
        self.H = get("H")
        self.NO3 = get("NO3")
        self.NH4 = get("NH4")
        self.DO = get("DO")
        self.FEED = [nf * get('M_F')[0] * get('FCR_F')[0] for nf, a in zip(get('N_F'), self.A)]
        self.FEED_NO3 = [0.2 * get('FEED_NO3')[0] * m * a * 0.01 / (v * 1000) for m, a, v in
                         zip(self.FEED, self.A, self.V)]

    def set_external_input(self, external_input):
        self.external_input = external_input
        return self.external_input

    def phytoplankton_nitrate_absorption(self):
        """Calculate Abs2_PHY: Phytoplankton nitrate absorption"""
        if 'phytoplankton_nitrate_absorption' in self.cache:
            return self.cache['phytoplankton_nitrate_absorption']

        NC_PHY = self.get_parameter('NC_PHY')[0]
        # GPP = self.phytoplankton.phy_growth_rate()
        KN_PHY = self.get_parameter('KN_PHY')[0]
        PN_PHY = [(nh4 * no3) / ((nh4 + KN_PHY) * (no3 + KN_PHY)) + (nh4 * KN_PHY) / ((nh4 + KN_PHY) * (no3 + KN_PHY))
                  for nh4, no3 in zip(self.NH4, self.NO3)]
        # Abs2_PHY = [gpp * (1 - pn) * NC_PHY for gpp, pn in zip(GPP, PN_PHY)]

        # self.cache['phytoplankton_nitrate_absorption'] = Abs2_PHY
        return [(1 - pn) * NC_PHY for pn in PN_PHY]

    def macroalgal_nitrate_absorption(self):
        """Calculate Abs2_MA: Macroalgal nitrate absorption"""
        if 'macroalgal_nitrate_absorption' in self.cache:
            return self.cache['macroalgal_nitrate_absorption']

        KN_MA = self.get_parameter('KN_MA')[0]
        F_UN_MA = self.macroalgal.update_internal_quotas()[0]
        PN_MA = [(nh4 * no3) / ((nh4 + KN_MA) * (no3 + KN_MA)) + (nh4 * KN_MA) / ((nh4 + KN_MA) * (no3 + KN_MA))
                 for nh4, no3 in zip(self.NH4, self.NO3)]
        A_MA = [a * 0.01 for a in self.get_parameter('A')]
        V = self.get_parameter('V')
        Abs2_MA = [f_un * (1 - pn) * a_ma / v for f_un, pn, a_ma, v in zip(F_UN_MA, PN_MA, A_MA, V)]

        self.cache['macroalgal_nitrate_absorption'] = Abs2_MA
        return Abs2_MA

    def denitrification(self):
        """Calculate DenN: Denitrification"""
        if 'denitrification' in self.cache:
            return self.cache['denitrification']

        DenN = [self.KC_den * (self.KT_den ** (t - 20)) * no3 * (self.K_den / (do + self.K_den))
                for no3, do, t in zip(self.NO3, self.DO, self.T)]

        self.cache['denitrification'] = DenN
        return DenN

    def update_NO3(self):
        """Calculate the nitrate concentration change in the water"""
        if 'update_NO3' in self.cache:
            return self.cache['update_NO3']

        NitN = ammonium.nitrification()  # Use the nitrification rate from AmmoniumNitrogen class
        Abs2_PHY = self.phytoplankton_nitrate_absorption()
        Abs2_MA = self.macroalgal_nitrate_absorption()
        DenN = self.denitrification()

        dNO3_dt = [nit_n + feed_no3 - abs2_phy - abs2_ma - den_n + ex_no3
                   for nit_n, feed_no3, abs2_phy, abs2_ma, den_n, ex_no3 in zip(NitN, self.FEED_NO3, Abs2_PHY, Abs2_MA, DenN, self.external_NO3_input)]

        # Debugging
        i = 8
        change = abs(NitN[i]) + abs(self.FEED_NO3[i]) + abs(Abs2_PHY[i]) + abs(Abs2_MA[i]) + abs(DenN[i]) + abs(self.external_NO3_input[i])
        print(f"dNO3_dt: {dNO3_dt[i]}; change: {change}; NitN: {NitN[i] / change}; feed: {self.FEED_NO3[i] / change}; Abs2_PHY: {Abs2_PHY[i] / change}; Abs2_MA: {Abs2_MA[i] / change}; DenN: {DenN[i] / change}; ex_no3: {self.external_NO3_input[i]  / change}")

        self.NO3 = [max(1e-12, no3 + dno3) for no3, dno3 in zip(self.NO3, dNO3_dt)]

        self.cache['update_NO3'] = self.NO3
        return self.NO3

    def reset_cache(self):
        """Clear the cache at the end of each timestep"""
        self.cache.clear()

class OrganicNitrogen:
    def __init__(self, parameter_loader, phytoplankton, macroalgal, zooplankton, shellfish, fish):
        self.parameter_loader = parameter_loader
        self.reload_parameters()
        self.cache = {}  # Cache dictionary to store calculated results

        # Biological constants for mineralization
        self.KNC_min = self.get_parameter('KNC_min')[0]
        self.KNT_min = self.get_parameter('K_T')[0]

        # Model components
        self.phytoplankton = phytoplankton
        self.macroalgal = macroalgal
        self.zooplankton = zooplankton
        self.shellfish = shellfish
        self.fish = fish

        # External inputs
        self.external_ON_input = None

    def get_parameter(self, name):
        return self.parameter_loader.get_parameter(name)

    def reload_parameters(self):
        get = self.parameter_loader.get_parameter
        self.A = get("A")
        self.V = get("V")
        self.H = get("H")
        self.ON = get("ON")
        self.FEED = [nf * get('M_F')[0] * get('FCR_F')[0] for nf, a in
                     zip(get('N_F'), get('A'))]
        self.FEED_ON = [0.2 * get('FEED_ON')[0] * m * a * 0.01 / (v * 1000) for m, a, v in
                        zip(self.FEED, get('A'), get('V'))]

    def set_external_input(self, external_input):
        self.external_input = external_input
        return self.external_input

    def phytoplankton_on_release(self):
        """Calculate N2_PHY: Phytoplankton death organic nitrogen release"""
        if 'phytoplankton_on_release' in self.cache:
            return self.cache['phytoplankton_on_release']

        NC_PHY = self.get_parameter('NC_PHY')[0]
        FON_PHY = self.get_parameter('FON_PHY')[0]
        # DPP = self.phytoplankton.phy_loss_rate()
        # N2_PHY = [NC_PHY * dpp * FON_PHY for dpp in DPP]

        # self.cache['phytoplankton_on_release'] = N2_PHY
        return [NC_PHY * FON_PHY] * 20

    def macroalgal_on_release(self):
        """Calculate N2_MA: Macroalgal death and metabolism organic nitrogen release"""
        if 'macroalgal_on_release' in self.cache:
            return self.cache['macroalgal_on_release']

        F_DN_MA = self.macroalgal.update_internal_quotas()[2]
        F_EN_MA = self.macroalgal.update_internal_quotas()[1]
        A_MA = self.macroalgal.A_MA
        f_ON_MA = [max(1, (self.get_parameter('NC_MA')[0] / self.get_parameter('DC_MA')[0]) /
                   (q_n_ma / 1000)) for q_n_ma in self.macroalgal.q_N]
        mu_sink = self.get_parameter('mu_ON_sink')[0]

        N2_MA = [(f_dn + f_en) * a_ma * f_on_ma * (1 - mu_sink) / v
                 for f_dn, f_en, f_on_ma, a_ma, v in zip(F_DN_MA, F_EN_MA, f_ON_MA, A_MA, self.V)]

        self.cache['macroalgal_on_release'] = N2_MA
        return N2_MA

    def zooplankton_on_release(self):
        """Calculate N2_ZOO: Zooplankton metabolism and death organic nitrogen release"""
        if 'zooplankton_on_release' in self.cache:
            return self.cache['zooplankton_on_release']

        NC_PHY = self.get_parameter('NC_PHY')[0]
        EFF = self.get_parameter('EFF')[0]
        GRZ = self.zooplankton.grazing_rate()
        DZ = self.zooplankton.phy_loss_rate()
        N2_ZOO = [(1 - EFF) * grz + dz * NC_PHY for grz, dz in zip(GRZ, DZ)]

        self.cache['zooplankton_on_release'] = N2_ZOO
        return N2_ZOO

    def shellfish_on_release(self):
        """Calculate N2_SH: Shellfish metabolism and death organic nitrogen release"""
        if 'shellfish_on_release' in self.cache:
            return self.cache['shellfish_on_release']

        DSH = self.shellfish.DSH
        N_SH = self.shellfish.N_SH
        mu_V_SH = self.get_parameter('mu_V_SH')[0]
        V_SH = self.shellfish.V_SH
        E_SH = self.shellfish.E_SH
        E_R_SH = self.shellfish.E_R_SH
        kappa_R_SH = self.get_parameter('kappa_R_SH')[0]
        NC_SH = self.get_parameter('NC_SH')[0]
        mu_CJ = self.get_parameter('mu_CJ')[0]
        PHY = self.get_parameter('PHY')
        k_SH_T = self.shellfish.temperature_effect()
        U_SH = self.get_parameter('U_SH')[0]
        p_A_SH = self.shellfish.energy_assimilation_rate()
        mu_sink = self.get_parameter('mu_ON_sink')[0]

        # Death nitrogen loss
        DN2_SH = [DSH * n_sh * (mu_V_SH * v_sh + e_sh + e_r_sh * kappa_R_SH) * NC_SH / mu_CJ
                  for n_sh, v_sh, e_sh, e_r_sh in zip(N_SH, V_SH, E_SH, E_R_SH)]

        # Fecal nitrogen loss
        FaeceN_SH = [NC_SH * ((k_SH_T * U_SH * phy * v_sh ** (2 / 3)) - p_a_sh / mu_CJ) * n_sh / v_sh
                     for phy, v_sh, p_a_sh, n_sh in zip(PHY, V_SH, p_A_SH, N_SH)]

        N2_SH = [(dn2_sh + faece_n_sh) * (1 - mu_sink) / (v * 1000)
                 for dn2_sh, faece_n_sh, v in zip(DN2_SH, FaeceN_SH, self.V)]

        self.cache['shellfish_on_release'] = N2_SH
        return N2_SH

    def fish_on_release(self):
        """Calculate N2_F: Fish metabolism and death organic nitrogen release"""
        if 'fish_on_release' in self.cache:
            return self.cache['fish_on_release']

        DF = self.get_parameter('DF')[0]
        N_F = self.fish.N_F
        mu_V_F = self.get_parameter('mu_V_F')[0]
        V_F = self.fish.V_F
        E_F = self.fish.E_F
        E_R_F = self.fish.E_R_F
        kappa_R_F = self.get_parameter('kappa_R_F')[0]
        Q_N_F = self.get_parameter('NC_F')[0]
        mu_CJ = self.get_parameter('mu_CJ')[0]
        k_F_T = self.fish.temperature_effect()
        U_F = self.get_parameter('U_F')[0]
        p_A_F = self.fish.energy_assimilation_rate()
        mu_sink = self.get_parameter('mu_ON_sink')[0]

        # Death nitrogen loss
        DN2_F = [DF * n_f * (mu_V_F * v_f + e_f + e_r_f * kappa_R_F) * Q_N_F / mu_CJ
                 for n_f, v_f, e_f, e_r_f in zip(N_F, V_F, E_F, E_R_F)]

        # Fecal nitrogen loss
        FaeceN_F = [Q_N_F * ((k_F_T * U_F * v_f ** (2 / 3)) - p_a_f / mu_CJ) * n_f / v_f
                    for v_f, p_a_f, n_f in zip(V_F, p_A_F, N_F)]

        N2_F = [(dn2_f + faece_n_f) * (1 - mu_sink) / (v * 1000)
                for dn2_f, faece_n_f, v in zip(DN2_F, FaeceN_F, self.V)]

        self.cache['fish_on_release'] = N2_F
        return N2_F

    def mineralization(self):
        """Calculate MinN: Organic nitrogen mineralization"""
        if 'mineralization' in self.cache:
            return self.cache['mineralization']

        MinN = [self.KNC_min * (self.KNT_min ** (t - 20)) * on for on, t in zip(self.ON, self.macroalgal.T)]
        self.cache['mineralization'] = MinN
        return MinN

    def update_ON(self):
        """Calculate the organic nitrogen concentration change in the water"""
        if 'update_ON' in self.cache:
            return self.cache['update_ON']

        N2_PHY = self.phytoplankton_on_release()
        N2_MA = self.macroalgal_on_release()
        N2_ZOO = self.zooplankton_on_release()
        N2_SH = self.shellfish_on_release()
        N2_F = self.fish_on_release()
        MinN = self.mineralization()

        dON_dt = [n2_phy + n2_ma + n2_zoo + n2_sh + n2_f + feed_on - min_n + ex_on
                  for n2_phy, n2_ma, n2_zoo, n2_sh, n2_f, feed_on, min_n, ex_on in zip(N2_PHY, N2_MA, N2_ZOO, N2_SH, N2_F, self.FEED_ON, MinN, self.external_ON_input)]

        i = 4
        change = abs(N2_PHY[i]) + abs(N2_MA[i]) + abs(N2_ZOO[i]) + abs(N2_SH[i]) + abs(N2_F[i]) + abs(self.FEED_ON[i]) + abs(MinN[i]) + abs(self.external_ON_input[i])
        print(f"dON_dt: {dON_dt[i]}; change: {change}; N2_PHY: {N2_PHY[i] / change}; N2_MA: {N2_MA[i] / change}; N2_ZOO: {N2_ZOO[i] / change}; N2_SH: {N2_SH[i] / change}; N2_F: {N2_F[i] / change}; feed_on: {self.FEED_ON[i] / change}; MinN: {MinN[i] / change}; ex_on: {self.external_ON_input[i] / change}")

        dON_dt = np.real_if_close(dON_dt, tol=1e-9)

        self.ON = [max(0, on + don) for on, don in zip(self.ON, dON_dt)]

        self.cache['update_ON'] = self.ON
        return self.ON

    def reset_cache(self):
        """Clear the cache at the end of each timestep"""
        self.cache.clear()

class InorganicPhosphorus:
    def __init__(self, parameter_loader, phytoplankton, macroalgal):
        self.parameter_loader = parameter_loader
        self.reload_parameters()
        self.cache = {}  # Cache to store computed values

        # Biological constants for mineralization
        self.KPC_min = self.get_parameter('KPC_min')[0]
        self.KPT_min = self.get_parameter('K_T')[0]
        self.KT_ads = self.get_parameter('K_T')[0]
        self.KT_des = self.get_parameter('K_T')[0]
        self.K_des = self.get_parameter('K_des')[0]
        self.K_ads = self.get_parameter('K_ads')[0]
        self.Q_max = self.get_parameter('Q_max')[0]

        # Phytoplankton and macroalgal components
        self.phytoplankton = phytoplankton
        self.macroalgal = macroalgal

        # External inputs
        self.external_PO4_input = None

    def get_parameter(self, name):
        return self.parameter_loader.get_parameter(name)

    def reload_parameters(self):
        get = self.parameter_loader.get_parameter
        self.T = get("T")
        self.A = get("A")
        self.V = get("V")
        self.H = get("H")
        self.PO4 = get("PO4")
        self.OP = get("OP")
        self.DO = get("DO")
        self.PP = get("PP")
        self.C_SPM = get("C_SPM")
        self.FEED = [nf * get('M_F')[0] * get('FCR_F')[0] for nf, a in
                     zip(get('N_F'), self.A)]
        self.FEED_PO4 = [0.2 * get('FEED_PO4')[0] * m * a * 0.01 / (v * 1000) for m, a, v in
                         zip(self.FEED, get('A'), get('V'))]


    def set_external_input(self, external_input):
        self.external_input = external_input
        return self.external_input

    def phytoplankton_phosphate_release(self):
        """Calculate P1_PHY: Phytoplankton death releasing inorganic phosphorus"""
        if 'phytoplankton_phosphate_release' in self.cache:
            return self.cache['phytoplankton_phosphate_release']

        PC = self.get_parameter('PC_PHY')[0]
        FOP = self.get_parameter('FOP_PHY')[0]
        # DPP = self.phytoplankton.phy_loss_rate()
        # P1_PHY = [PC * dpp * (1 - FOP) for dpp in DPP]
        #
        # self.cache['phytoplankton_phosphate_release'] = P1_PHY
        return [PC * (1 - FOP)] * 20

    def macroalgal_phosphate_release(self):
        """Calculate P1_MA: Macroalgal metabolism and death releasing inorganic phosphorus"""
        if 'macroalgal_phosphate_release' in self.cache:
            return self.cache['macroalgal_phosphate_release']

        F_EP_MA = self.macroalgal.update_internal_quotas()[1]
        F_DP_MA = self.macroalgal.update_internal_quotas()[2]
        f_OP_MA = [(self.get_parameter('PC_MA')[0] / self.get_parameter('DC_MA')[0]) / (q_p * 1e-3)
                   for q_p in self.macroalgal.q_P]
        A_MA = self.macroalgal.A_MA
        P1_MA = [(f_ep_ma + f_dp_ma) * (1 - f_op_ma) * a_ma / v
                 for f_ep_ma, f_dp_ma, f_op_ma, a_ma, v in zip(F_EP_MA, F_DP_MA, f_OP_MA, A_MA, self.V)]

        self.cache['macroalgal_phosphate_release'] = P1_MA
        return P1_MA

    def phosphate_mineralization(self):
        """Calculate MinP: Organic phosphorus mineralization"""
        if 'phosphate_mineralization' in self.cache:
            return self.cache['phosphate_mineralization']

        MinP = [self.KPC_min * (self.KPT_min ** (t - 20)) * op for op, t in zip(self.OP, self.macroalgal.T)]

        self.cache['phosphate_mineralization'] = MinP
        return MinP

    def phytoplankton_phosphate_absorption(self):
        """Calculate Abs3_PHY: Phytoplankton absorbing inorganic phosphorus"""
        if 'phytoplankton_phosphate_absorption' in self.cache:
            return self.cache['phytoplankton_phosphate_absorption']

        PC = self.get_parameter('PC_PHY')[0]
        GPP = self.phytoplankton.phy_growth_rate()
        Abs3_PHY = [gpp * PC for gpp in GPP]

        self.cache['phytoplankton_phosphate_absorption'] = Abs3_PHY
        return Abs3_PHY

    def macroalgal_phosphate_absorption(self):
        """Calculate Abs3_MA: Macroalgal absorbing inorganic phosphorus"""
        if 'macroalgal_phosphate_absorption' in self.cache:
            return self.cache['macroalgal_phosphate_absorption']

        F_UP_MA = self.macroalgal.update_internal_quotas()[0]  # Phosphorus absorption rate (gP/m²/day)
        A_MA = self.macroalgal.A_MA  # Area of macroalgal cultivation (m²)
        Abs3_MA = [f_up_ma * a_ma / v for f_up_ma, a_ma, v in zip(F_UP_MA, A_MA, self.V)]

        self.cache['macroalgal_phosphate_absorption'] = Abs3_MA
        return Abs3_MA

    def particle_phosphorus_adsorption_desorption(self):
        if 'particle_phosphorus_adsorption_desorption' in self.cache:
            return self.cache['particle_phosphorus_adsorption_desorption']

        # PP_ads = [self.K_ads * (self.KT_ads ** (t - 20)) * po4 for t, po4 in zip(self.T, self.PO4)]
        PP_ads = [self.K_ads * c_spm * (self.KT_ads ** (t - 20)) * (1 - pp / (self.Q_max * c_spm)) * po4 for
                  c_spm, t, pp, po4 in zip(self.C_SPM, self.T, self.PP, self.PO4)]
        PP_des = [self.K_des * (self.KT_des ** (t - 20)) * pp for t, pp in zip(self.T, self.PP)]

        PP_ads_des = [pp_ads - pp_des for pp_ads, pp_des in zip(PP_ads, PP_des)]

        self.cache['particle_phosphorus_desorption'] = PP_ads_des
        return PP_ads_des

    def update_PO4(self):
        """Calculate the phosphate concentration change in the water"""
        if 'update_PO4' in self.cache:
            return self.cache['update_PO4']

        MinP = self.phosphate_mineralization()
        P1_PHY = self.phytoplankton_phosphate_release()
        P1_MA = self.macroalgal_phosphate_release()
        Abs3_PHY = self.phytoplankton_phosphate_absorption()
        Abs3_MA = self.macroalgal_phosphate_absorption()
        PP_ads_des = self.particle_phosphorus_adsorption_desorption()

        dPO4_dt = [minp + p1_phy + p1_ma + feed_po4 - abs3_phy - abs3_ma + ex_po4 - pp_ads_des
                   for minp, p1_phy, p1_ma, feed_po4, abs3_phy, abs3_ma, ex_po4, pp_ads_des in zip(MinP, P1_PHY, P1_MA, self.FEED_PO4, Abs3_PHY, Abs3_MA, self.external_PO4_input, PP_ads_des)]

        self.PO4 = [po4 + dpo4 for po4, dpo4 in zip(self.PO4, dPO4_dt)]

        self.cache['update_PO4'] = self.PO4
        return self.PO4

    def reset_cache(self):
        """Clear the cache at the end of each timestep"""
        self.cache.clear()

class OrganicPhosphorus:
    def __init__(self, parameter_loader, phytoplankton, macroalgal, zooplankton, shellfish, fish, inorganic_phosphorus):
        self.parameter_loader = parameter_loader
        self.reload_parameters()
        self.cache = {}  # Cache to store computed values

        # Model components
        self.phytoplankton = phytoplankton
        self.macroalgal = macroalgal
        self.zooplankton = zooplankton
        self.shellfish = shellfish
        self.fish = fish
        self.inorganic_phosphorus = inorganic_phosphorus

        # External inputs
        self.external_OP_input = None

    def get_parameter(self, name):
        return self.parameter_loader.get_parameter(name)

    def reload_parameters(self):
        get = self.parameter_loader.get_parameter
        self.A = get("A")
        self.V = get("V")
        self.H = get("H")
        self.OP = get("OP")
        self.DO = get("DO")
        self.FEED = [nf * get('M_F')[0] * get('FCR_F')[0] for nf, a in
                     zip(get('N_F'), self.A)]
        self.FEED_OP = [0.2 * get('FEED_OP')[0] * m * a * 0.01 / (v * 1000) for m, a, v in
                        zip(self.FEED, self.A, get('V'))]

    def set_external_input(self, external_input):
        self.external_input = external_input
        return self.external_input

    def phytoplankton_op_release(self):
        """Calculate P2_PHY: Phytoplankton death releasing organic phosphorus"""
        if 'phytoplankton_op_release' in self.cache:
            return self.cache['phytoplankton_op_release']

        PC = self.get_parameter('PC_PHY')[0]
        FOP = self.get_parameter('FOP_PHY')[0]
        # DPP = self.phytoplankton.phy_loss_rate()
        # P2_PHY = [PC * dpp * FOP for dpp in DPP]
        #
        # self.cache['phytoplankton_op_release'] = P2_PHY
        return [PC * FOP] * 20

    def macroalgal_op_release(self):
        """Calculate P2_MA: Macroalgal metabolism and death releasing organic phosphorus"""
        if 'macroalgal_op_release' in self.cache:
            return self.cache['macroalgal_op_release']

        F_DP_MA = self.macroalgal.update_internal_quotas()[2]
        F_EP_MA = self.macroalgal.update_internal_quotas()[1]
        f_OP_MA = [(self.get_parameter('PC_MA')[0] / self.get_parameter('DC_MA')[0]) / (q_p * 1e-3)
                   for q_p in self.macroalgal.q_P]
        A_MA = self.macroalgal.A_MA
        mu_sink = self.get_parameter('mu_OP_sink')[0]

        P2_MA = [(f_dp_ma * (1 - mu_sink) + f_ep_ma) * a_ma * f_op_ma / v
                 for f_dp_ma, f_ep_ma, f_op_ma, a_ma, v in zip(F_DP_MA, F_EP_MA, f_OP_MA, A_MA, self.V)]

        self.cache['macroalgal_op_release'] = P2_MA
        return P2_MA

    def zooplankton_op_release(self):
        """Calculate P2_ZOO: Zooplankton metabolism and death releasing organic phosphorus"""
        if 'zooplankton_op_release' in self.cache:
            return self.cache['zooplankton_op_release']

        PC = self.get_parameter('PC_PHY')[0]
        EFF = self.get_parameter('EFF')[0]
        GRZ = self.zooplankton.grazing_rate()
        DZ = self.zooplankton.phy_loss_rate()
        f_fec = self.get_parameter('f_fec')[0]

        P2_ZOO = [((1 - EFF) * grz * PC + dz * PC) * (1 - f_fec) for grz, dz in zip(GRZ, DZ)]

        self.cache['zooplankton_op_release'] = P2_ZOO
        return P2_ZOO

    def shellfish_op_release(self):
        """Calculate P2_SH: Shellfish metabolism and death releasing organic phosphorus"""
        if 'shellfish_op_release' in self.cache:
            return self.cache['shellfish_op_release']

        DSH = self.shellfish.DSH
        N_SH = self.shellfish.N_SH
        mu_V_SH = self.get_parameter('mu_V_SH')[0]
        E_SH = self.shellfish.E_SH
        E_R_SH = self.shellfish.E_R_SH
        kappa_R_SH = self.get_parameter('kappa_R_SH')[0]
        V_SH = self.shellfish.V_SH
        QP_SH = self.get_parameter('PC_SH')[0]
        mu_CJ = self.get_parameter('mu_CJ')[0]
        f_PP = self.get_parameter('f_PP')[0]

        # Death phosphorus loss (mgP/L)
        DP2_SH = [DSH * n_sh * (mu_V_SH * v_sh + e_sh + e_r_sh * kappa_R_SH) * QP_SH / mu_CJ /v
                  for n_sh, v_sh, e_sh, e_r_sh, v in zip(N_SH, V_SH, E_SH, E_R_SH, self.V)]

        # Feces phosphorus loss (mgP/L)
        PC = self.get_parameter('PC_PHY')[0]
        k_SH_T = self.shellfish.temperature_effect()
        U_SH = self.get_parameter('U_SH')[0]
        PHY = self.shellfish.PHY
        p_A_SH = self.shellfish.energy_assimilation_rate()

        FaeceP_SH = [PC * (k_SH_T * U_SH * phy * v_sh ** (2 / 3) - p_a_sh / mu_CJ) * n_sh / v_sh / v
                     for phy, v_sh, p_a_sh, n_sh, v in zip(PHY, V_SH, p_A_SH, N_SH, self.V)]

        P2_SH = [(dp2_sh + faecep_sh) * (1 - f_PP) for dp2_sh, faecep_sh in zip(DP2_SH, FaeceP_SH)]

        self.cache['shellfish_op_release'] = P2_SH
        return P2_SH

    def fish_op_release(self):
        """Calculate P2_F: Fish metabolism and death releasing organic phosphorus"""
        if 'fish_op_release' in self.cache:
            return self.cache['fish_op_release']

        DF = self.fish.DF
        N_F = self.fish.N_F
        mu_V_F = self.get_parameter('mu_V_F')[0]
        E_F = self.fish.E_F
        E_R_F = self.fish.E_R_F
        kappa_R_F = self.get_parameter('kappa_R_F')[0]
        V_F = self.fish.V_F
        QP_F = self.get_parameter('PC_F')[0]
        mu_CJ = self.get_parameter('mu_CJ')[0]
        f_PP = self.get_parameter('f_PP')[0]

        # Death phosphorus loss (mgP/L)
        DP2_F = [DF * n_f * (mu_V_F * v_f + e_f + e_r_f * kappa_R_F) * QP_F / mu_CJ / v
                 for n_f, v_f, e_f, e_r_f, v in zip(N_F, V_F, E_F, E_R_F, self.V)]

        # Feces phosphorus loss (mgP/L)
        k_F_T = self.fish.temperature_effect()
        U_F = self.get_parameter('U_F')[0]
        p_A_F = self.fish.energy_assimilation_rate()

        FaeceP_F = [QP_F * (k_F_T * U_F * v_f ** (2 / 3) - p_a_f / mu_CJ) * n_f / v_f / v
                    for v_f, p_a_f, n_f, v in zip(V_F, p_A_F, N_F, self.V)]

        P2_F = [(dp2_f + faecep_f) * (1 - f_PP) for dp2_f, faecep_f in zip(DP2_F, FaeceP_F)]

        self.cache['fish_op_release'] = P2_F
        return P2_F

    def phosphate_mineralization(self):
        """Calculate MinP: Organic phosphorus mineralization"""
        if 'phosphate_mineralization' in self.cache:
            return self.cache['phosphate_mineralization']

        MinP = self.inorganic_phosphorus.phosphate_mineralization()

        self.cache['phosphate_mineralization'] = MinP
        return MinP

    def update_OP(self):
        """Update the organic phosphorus concentration in water"""
        if 'update_OP' in self.cache:
            return self.cache['update_OP']

        P2_PHY = self.phytoplankton_op_release()
        P2_MA = self.macroalgal_op_release()
        P2_ZOO = self.zooplankton_op_release()
        P2_SH = self.shellfish_op_release()
        P2_F = self.fish_op_release()
        MinP = self.phosphate_mineralization()

        dOP_dt = [p2_phy + p2_ma + p2_zoo + p2_sh + p2_f + feed_op - min_p + ex_op
                  for p2_phy, p2_ma, p2_zoo, p2_sh, p2_f, feed_op, min_p, ex_op in zip(P2_PHY, P2_MA, P2_ZOO, P2_SH, P2_F, self.FEED_OP, MinP, self.external_OP_input)]

        self.OP = [op + dop for op, dop in zip(self.OP, dOP_dt)]

        self.cache['update_OP'] = self.OP
        return self.OP

    def reset_cache(self):
        """Clear the cache at the end of each timestep"""
        self.cache.clear()

class ParticulatePhosphorus:
    def __init__(self, parameter_loader, phytoplankton, zooplankton, shellfish, fish):
        self.parameter_loader = parameter_loader
        self.cache = {}  # Cache for computed values

        # Model components
        self.phytoplankton = phytoplankton
        self.zooplankton = zooplankton
        self.shellfish = shellfish
        self.fish = fish

        # External inputs
        self.external_PP_input = None

        # Constants for PP
        self.K_ads = self.get_parameter('K_ads')[0]  # Adsorption constant for PP
        self.K_des = self.get_parameter('K_des')[0]  # Desorption constant for PP
        self.V_set  = self.get_parameter('V_set')[0]  # Settling velocity for PP
        self.K_resus = self.get_parameter('K_resus')[0]  # Resuspension constant for PP
        self.KT_ads = self.get_parameter('K_T')[0]  # Temperature effect on adsorption for PP
        self.KT_des = self.get_parameter('K_T')[0]  # Temperature effect on desorption for PP
        self.Q_max = self.get_parameter('Q_max')[0]  # Maximum adsorbed quantity for PP

    def get_parameter(self, name):
        return self.parameter_loader.get_parameter(name)

    def reload_parameters(self):
        get = self.parameter_loader.get_parameter
        self.T = get("T")
        self.V = get("V")
        self.A = get("A")
        self.H = [v / a for v, a in zip(self.V, self.A)]
        self.PO4 = get("PO4")
        self.PP = get("PP")
        self.C_SPM = get("C_SPM")
        self.FEED = [nf * get('M_F')[0] * get('FCR_F')[0] for nf, a in
                     zip(get('N_F'), self.A)]
        self.FEED_PP = [0.2 * get('FEED_PP')[0] * m * a * 0.01 / (v * 1000) for m, a, v in
                         zip(self.FEED, get('A'), get('V'))]

    def zooplankton_pp_release(self):
        if 'zooplankton_op_release' in self.cache:
            return self.cache['zooplankton_op_release']

        PC = self.get_parameter('PC_PHY')[0]
        EFF = self.get_parameter('EFF')[0]
        GRZ = self.zooplankton.grazing_rate()
        DZ = self.zooplankton.loss_rate()
        f_fec = self.get_parameter('f_fec')[0]

        PP_ZOO = [((1 - EFF) * grz * PC + dz * PC) * f_fec for grz, dz in zip(GRZ, DZ)]

        self.cache['zooplankton_op_release'] = PP_ZOO
        return PP_ZOO

    def shellfish_pp_release(self):
        if 'shellfish_op_release' in self.cache:
            return self.cache['shellfish_op_release']

        DSH = self.shellfish.DSH
        N_SH = self.shellfish.N_SH
        mu_V_SH = self.get_parameter('mu_V_SH')[0]
        E_SH = self.shellfish.E_SH
        E_R_SH = self.shellfish.E_R_SH
        kappa_R_SH = self.get_parameter('kappa_R_SH')[0]
        V_SH = self.shellfish.V_SH
        QP_SH = self.get_parameter('PC_SH')[0]
        mu_CJ = self.get_parameter('mu_CJ')[0]
        f_PP = self.get_parameter('f_PP')[0]

        # Death phosphorus loss (mgP/L)
        DP2_SH = [DSH * n_sh * (mu_V_SH * v_sh + e_sh + e_r_sh * kappa_R_SH) * QP_SH / mu_CJ /v
                  for n_sh, v_sh, e_sh, e_r_sh, v in zip(N_SH, V_SH, E_SH, E_R_SH, self.V)]

        # Feces phosphorus loss (mgP/L)
        PC = self.get_parameter('PC_PHY')[0]
        k_SH_T = self.shellfish.temperature_effect()
        U_SH = self.get_parameter('U_SH')[0]
        PHY = self.shellfish.PHY
        p_A_SH = self.shellfish.energy_assimilation_rate()

        FaeceP_SH = [PC * (k_SH_T * U_SH * phy * v_sh ** (2 / 3) - p_a_sh / mu_CJ) * n_sh / v_sh / v
                     for phy, v_sh, p_a_sh, n_sh, v in zip(PHY, V_SH, p_A_SH, N_SH, self.V)]

        PP_SH = [(dp2_sh + faecep_sh) * f_PP for dp2_sh, faecep_sh in zip(DP2_SH, FaeceP_SH)]

        self.cache['shellfish_op_release'] = PP_SH
        return PP_SH

    def fish_pp_release(self):
        if 'fish_op_release' in self.cache:
            return self.cache['fish_op_release']

        DF = self.fish.DF
        N_F = self.fish.N_F
        mu_V_F = self.get_parameter('mu_V_F')[0]
        E_F = self.fish.E_F
        E_R_F = self.fish.E_R_F
        kappa_R_F = self.get_parameter('kappa_R_F')[0]
        V_F = self.fish.V_F
        QP_F = self.get_parameter('PC_F')[0]
        mu_CJ = self.get_parameter('mu_CJ')[0]
        f_PP = self.get_parameter('f_PP')[0]

        # Death phosphorus loss (mgP/L)
        DP2_F = [DF * n_f * (mu_V_F * v_f + e_f + e_r_f * kappa_R_F) * QP_F / mu_CJ / v
                 for n_f, v_f, e_f, e_r_f, v in zip(N_F, V_F, E_F, E_R_F, self.V)]

        # Feces phosphorus loss (mgP/L)
        k_F_T = self.fish.temperature_effect()
        U_F = self.get_parameter('U_F')[0]
        p_A_F = self.fish.energy_assimilation_rate()

        FaeceP_F = [QP_F * (k_F_T * U_F * v_f ** (2 / 3) - p_a_f / mu_CJ) * n_f / v_f / v
                    for v_f, p_a_f, n_f, v in zip(V_F, p_A_F, N_F, self.V)]

        PP_F = [(dp2_f + faecep_f) * f_PP for dp2_f, faecep_f in zip(DP2_F, FaeceP_F)]

        self.cache['fish_op_release'] = PP_F
        return PP_F

    def adsorption_and_desorption(self):
        if 'adsorption_and_desorption' in self.cache:
            return self.cache['adsorption_and_desorption']

        # PP_ads = [self.K_ads * (self.KT_ads ** (t - 20)) * po4 for t, po4 in zip(self.T, self.PO4)]
        PP_ads = [self.K_ads * c_spm * (self.KT_ads ** (t - 20)) * (1 - pp / (self.Q_max * c_spm)) * po4 for c_spm, t, pp, po4 in zip(self.C_SPM, self.T, self.PP, self.PO4)]
        PP_des = [self.K_des * (self.KT_des ** (t - 20)) * pp for t, pp in zip(self.T, self.PP)]

        PP_ads_des = [pp_ads - pp_des for pp_ads, pp_des in zip(PP_ads, PP_des)]

        self.cache['adsorption_and_desorption'] = PP_ads_des
        return PP_ads_des

    def sink_and_resuspension(self):
        if 'PP_sink_and_resuspension' in self.cache:
            return self.cache['PP_sink_and_resuspension']

        PP_set = [self.V_set * pp / h for pp, h in zip(self.PP, self.H)]
        PP_resus = [pp * self.K_resus for pp in self.PP]

        PP_set_resus = [pp_set - pp_resus for pp_set, pp_resus in zip(PP_set, PP_resus)]

        self.cache['PP_sink_and_resuspension'] = PP_set_resus
        return PP_set_resus

    def update_PP(self):
        """Update the particulate phosphorus concentration in water"""
        if 'update_PP' in self.cache:
            return self.cache['update_PP']

        PP_ZOO = self.zooplankton_pp_release()
        PP_SH = self.shellfish_pp_release()
        PP_F = self.fish_pp_release()
        PP_ads_des = self.adsorption_and_desorption()
        PP_set_resus = self.sink_and_resuspension()

        dPP_dt = [pp_zoo + pp_sh + pp_f + pp_ads_des - pp_set_resus
                  for pp_zoo, pp_sh, pp_f, pp_ads_des, pp_set_resus in zip(PP_ZOO, PP_SH, PP_F, PP_ads_des, PP_set_resus)]

        self.PP = [pp + dp for pp, dp in zip(self.PP, dPP_dt)]

        self.cache['update_PP'] = self.PP
        return self.PP

    def reset_cache(self):
        """Clear the cache at the end of each timestep"""
        self.cache.clear()

class CBOD:
    def __init__(self, parameter_loader, phytoplankton, macroalgal, zooplankton, shellfish, fish, nitrate):
        self.parameter_loader = parameter_loader
        self.cache = {}  # Cache for computed values

        # Load initial CBOD concentration from 'Initial Conditions' tab
        self.CBOD = self.get_parameter('CBOD')
        self.DO = self.get_parameter('DO')
        self.FEED = [nf * self.get_parameter('M_F')[0] * self.get_parameter('FCR_F')[0] / a for nf, a in
                     zip(self.get_parameter('N_F'), self.get_parameter('A'))]
        self.FEED_CBOD = [0.2 * self.get_parameter('FEED_CBOD')[0] * m * a * 0.01 / (v * 1000) for m, a, v in
                        zip(self.FEED, self.get_parameter('A'), self.get_parameter('V'))]
        self.V = self.get_parameter('V')

        # Constants for CBOD oxidation
        self.KDC = self.get_parameter('KDC')[0]  # Constant oxidation rate
        self.KDT = self.get_parameter('K_T')[0]  # Temperature constant for CBOD oxidation
        self.KBOD = self.get_parameter('K_BOD')[0]  # Half-saturation constant for CBOD oxidation

        # Model components
        self.phytoplankton = phytoplankton
        self.macroalgal = macroalgal
        self.zooplankton = zooplankton
        self.shellfish = shellfish
        self.fish = fish
        self.nitrate = nitrate

        # External inputs
        self.external_CBOD_input = None

    def get_parameter(self, name):
        return self.parameter_loader.get_parameter(name)

    def set_external_input(self, external_CBOD_input):
        self.external_CBOD_input = external_CBOD_input

    def phytoplankton_cbod(self):
        """Calculate CBOD_PHY: CBOD generated by phytoplankton death"""
        if 'phytoplankton_cbod' in self.cache:
            return self.cache['phytoplankton_cbod']

        OC = self.get_parameter('OC')[0]
        DPP = self.phytoplankton.phy_loss_rate()
        CBOD_PHY = [OC * dpp for dpp in DPP]

        self.cache['phytoplankton_cbod'] = CBOD_PHY
        return CBOD_PHY

    def zooplankton_cbod(self):
        """Calculate CBOD_ZOO: CBOD generated by zooplankton metabolism and death"""
        if 'zooplankton_cbod' in self.cache:
            return self.cache['zooplankton_cbod']

        OC = self.get_parameter('OC')[0]
        EFF = self.get_parameter('EFF')[0]
        GRZ = self.zooplankton.grazing_rate()
        DZ = self.zooplankton.phy_loss_rate()

        CBOD_ZOO = [(1 - EFF) * grz * OC + dz * OC for grz, dz in zip(GRZ, DZ)]

        self.cache['zooplankton_cbod'] = CBOD_ZOO
        return CBOD_ZOO

    def macroalgal_cbod(self):
        """Calculate CBOD_MA: CBOD generated by macroalgal metabolism and death"""
        if 'macroalgal_cbod' in self.cache:
            return self.cache['macroalgal_cbod']

        DMA = self.macroalgal.calculate_loss_rate()
        A_MA = self.macroalgal.A_MA
        QC_MA = self.get_parameter('DC_MA')[0]
        OC = self.get_parameter('OC')[0]

        CBOD_MA = [dma * a_ma * QC_MA * OC / v for dma, a_ma, v in zip(DMA, A_MA, self.V)]

        self.cache['macroalgal_cbod'] = CBOD_MA
        return CBOD_MA

    def shellfish_cbod(self):
        """Calculate CBOD_SH: CBOD generated by shellfish metabolism and death"""
        if 'shellfish_cbod' in self.cache:
            return self.cache['shellfish_cbod']

        DSH = self.shellfish.DSH
        N_SH = self.shellfish.N_SH
        mu_V_SH = self.get_parameter('mu_V_SH')[0]
        E_SH = self.shellfish.E_SH
        E_R_SH = self.shellfish.E_R_SH
        kappa_R_SH = self.get_parameter('kappa_R_SH')[0]
        V_SH = self.shellfish.V_SH
        OC = self.get_parameter('OC')[0]
        mu_CJ = self.get_parameter('mu_CJ')[0]

        # Death CBOD release (mgO₂/L)
        DC_SH = [DSH * n_sh * (mu_V_SH * v_sh + e_sh + e_r_sh * kappa_R_SH) * OC / mu_CJ / v
                 for n_sh, v_sh, e_sh, e_r_sh, v in zip(N_SH, V_SH, E_SH, E_R_SH, self.V)]

        # Feces CBOD release (mgO₂/L)
        k_SH_T = self.shellfish.temperature_effect()
        U_SH = self.get_parameter('U_SH')[0]
        PHY = self.shellfish.PHY
        p_A_SH = self.shellfish.energy_assimilation_rate()

        FaeceC_SH = [OC * (k_SH_T * U_SH * phy * v_sh ** (2 / 3) - p_a_sh / mu_CJ) * n_sh / v_sh / v
                     for phy, v_sh, p_a_sh, n_sh, v in zip(PHY, V_SH, p_A_SH, N_SH, self.V)]

        CBOD_SH = [dc_sh + faecec_sh for dc_sh, faecec_sh in zip(DC_SH, FaeceC_SH)]

        self.cache['shellfish_cbod'] = CBOD_SH
        return CBOD_SH

    def fish_cbod(self):
        """Calculate CBOD_F: CBOD generated by fish metabolism and death"""
        if 'fish_cbod' in self.cache:
            return self.cache['fish_cbod']

        DF = self.fish.DF
        N_F = self.fish.N_F
        mu_V_F = self.get_parameter('mu_V_F')[0]
        E_F = self.fish.E_F
        E_R_F = self.fish.E_R_F
        kappa_R_F = self.get_parameter('kappa_R_F')[0]
        V_F = self.fish.V_F
        OC = self.get_parameter('OC')[0]
        mu_CJ = self.get_parameter('mu_CJ')[0]

        # Death CBOD release (mgO₂/L)
        DC_F = [DF * n_f * (mu_V_F * v_f + e_f + e_r_f * kappa_R_F) * OC / mu_CJ / v
                for n_f, v_f, e_f, e_r_f, v in zip(N_F, V_F, E_F, E_R_F, self.V)]

        # Feces CBOD release (mgO₂/L)
        k_F_T = self.fish.temperature_effect()  # Temperature effect on fish
        U_F = self.get_parameter('U_F')[0]  # Maximum feeding rate
        p_A_F = self.fish.energy_assimilation_rate()

        FaeceC_F = [OC * (k_F_T * U_F * v_f ** (2 / 3) - p_a_f / mu_CJ) * n_f / v_f /v
                    for v_f, p_a_f, n_f, v in zip(V_F, p_A_F, N_F, self.V)]

        CBOD_F = [dc_f + faecec_f for dc_f, faecec_f in zip(DC_F, FaeceC_F)]

        self.cache['fish_cbod'] = CBOD_F
        return CBOD_F

    def cbod_oxidation(self):
        """Calculate OX: CBOD oxidation rate"""
        if 'cbod_oxidation' in self.cache:
            return self.cache['cbod_oxidation']

        OX = [self.KDC * (self.KDT ** (t - 20)) * cbod * (do / (do + self.KBOD))
              for cbod, do, t in zip(self.CBOD, self.DO, self.macroalgal.T)]

        self.cache['cbod_oxidation'] = OX
        return OX

    def cbod_denitrification(self):
        """Calculate CBOD_Den: CBOD removal by denitrification"""
        if 'cbod_denitrification' in self.cache:
            return self.cache['cbod_denitrification']

        DenN = self.nitrate.denitrification()  # Nitrate denitrification rate (mgN/L)
        CBOD_Den = [(5 / 4) * (32 / 14) * den_n for den_n in DenN]

        self.cache['cbod_denitrification'] = CBOD_Den
        return CBOD_Den

    def update_CBOD(self):
        """Update the CBOD concentration in water"""
        if 'update_CBOD' in self.cache:
            return self.cache['update_CBOD']

        CBOD_PHY = self.phytoplankton_cbod()
        CBOD_MA = self.macroalgal_cbod()
        CBOD_ZOO = self.zooplankton_cbod()
        CBOD_SH = self.shellfish_cbod()
        CBOD_F = self.fish_cbod()
        OX = self.cbod_oxidation()
        CBOD_Den = self.cbod_denitrification()

        dCBOD_dt = [cbod_phy + cbod_ma + cbod_zoo + cbod_sh + cbod_f + feed_cbod - ox - cbod_den + ex_cbod
                    for cbod_phy, cbod_ma, cbod_zoo, cbod_sh, cbod_f, feed_cbod, ox, cbod_den, ex_cbod in
                    zip(CBOD_PHY, CBOD_MA, CBOD_ZOO, CBOD_SH, CBOD_F, self.FEED_CBOD, OX, CBOD_Den, self.external_CBOD_input)]

        self.CBOD = [cbod + dcbod for cbod, dcbod in zip(self.CBOD, dCBOD_dt)]

        self.cache['update_CBOD'] = self.CBOD
        return self.CBOD

    def reset_cache(self):
        """Clear the cache at the end of each timestep"""
        self.cache.clear()

class DissolvedOxygen:
    def __init__(self, parameter_loader, phytoplankton, macroalgal, zooplankton, shellfish, fish, ammonium, cbod):
        self.parameter_loader = parameter_loader
        self.cache = {}  # Cache for computed values

        # Load initial DO concentration from 'Initial Conditions' tab
        self.DO = self.get_parameter('DO')
        self.T = self.get_parameter('T')
        self.H = self.get_parameter('H')
        self.S = self.get_parameter('S')
        self.W = self.get_parameter('W')
        self.v = self.get_parameter('v')
        self.V = self.get_parameter('V')
        self.SOD = self.get_parameter('SOD')[0]
        self.SODT = self.get_parameter('K_T')[0]
        self.FEED_CBOD = self.get_parameter('FEED_CBOD')[0]

        # Constants for atmospheric exchange
        self.KAT = self.get_parameter('K_T')[0]
        self.a = self.get_parameter('a')[0]
        self.b = self.get_parameter('b')[0]
        self.c = self.get_parameter('c')[0]
        self.d = self.get_parameter('d')[0]

        # Model components
        self.phytoplankton = phytoplankton
        self.macroalgal = macroalgal
        self.zooplankton = zooplankton
        self.shellfish = shellfish
        self.fish = fish
        self.ammonium = ammonium
        self.cbod = cbod

        # External inputs
        self.external_DO_input = None

    def get_parameter(self, name):
        return self.parameter_loader.get_parameter(name)

    def set_external_input(self, external_DO_input):
        self.external_DO_input = external_DO_input

    def do_atmospheric_exchange(self):
        """Calculate DO_atm: Atmospheric exchange"""
        if 'do_atmospheric_exchange' in self.cache:
            return self.cache['do_atmospheric_exchange']

        # Saturation oxygen concentration (mgO₂/L)
        O_sat = [14.621 * math.exp(-0.0134 * t) / (1 + 0.028 * s) for t, s in zip(self.T, self.S)]

        # O'Connor-Dobbins reaeration coefficient at 20°C (1/day)
        KA_20 = [(3.93 * (v ** 0.5) / min(5,h) ** 1.5) / 24 for v, h in zip(self.v, self.H)]

        # Temperature-adjusted reaeration coefficient
        KA = [ka_20 * (1.024 ** (t - 20)) for ka_20, t in zip(KA_20, self.T)]

        # Atmospheric exchange flux (mgO₂/L/day)
        DO_atm = [ka * (o_sat - max(do, 0)) for ka, o_sat, do in zip(KA, O_sat, self.DO)]

        self.cache['do_atmospheric_exchange'] = DO_atm
        return DO_atm

    def do_phytoplankton_production(self):
        """Calculate DO_PHY: Oxygen production by phytoplankton"""
        if 'do_phytoplankton_production' in self.cache:
            return self.cache['do_phytoplankton_production']

        GPP = self.phytoplankton.phy_growth_rate()
        PN_PHY = self.ammonium.phytoplankton_ammonium_absorption()[1]
        OC = self.get_parameter('OC')[0]
        NC = self.get_parameter('NC_PHY')[0]

        DO_PHY_NH4 = [pn_phy * gpp * OC for pn_phy, gpp in zip([PN_PHY] * len(GPP), GPP)]
        DO_PHY_NO3 = [(1 - PN_PHY) * gpp * 32 * (1 / 12 + 1.5 * (NC / 14)) for gpp in GPP]

        DO_PHY = [do_phy_nh4 + do_phy_no3 for do_phy_nh4, do_phy_no3 in zip(DO_PHY_NH4, DO_PHY_NO3)]

        self.cache['do_phytoplankton_production'] = DO_PHY
        return DO_PHY

    def do_macroalgal_production(self):
        """Calculate DO_MA: Oxygen production by macroalgal"""
        if 'do_macroalgal_production' in self.cache:
            return self.cache['do_macroalgal_production']

        GMA = self.macroalgal.calculate_GMA()
        A_MA = self.macroalgal.A_MA
        ROC = self.get_parameter('ROC_MA')[0]
        ADC = self.get_parameter('DC_MA')[0]
        PN_MA = self.ammonium.macroalgal_ammonium_absorption()[1]
        ANC = self.get_parameter('NC_MA')[0]

        DO_MA_NH4 = [gma * a_ma * ROC / ADC * PN_MA for gma, a_ma in zip(GMA, A_MA)]
        DO_MA_NO3 = [gma * a_ma * ANC / ADC * (1 - PN_MA) * (3 / 2) * (32 / 14) for gma, a_ma in zip(GMA, A_MA)]

        DO_MA = [(do_ma_nh4 + do_ma_no3) / v for do_ma_nh4, do_ma_no3, v in zip(DO_MA_NH4, DO_MA_NO3, self.V)]

        self.cache['do_macroalgal_production'] = DO_MA
        return DO_MA

    def do_phytoplankton_respiration(self):
        """Calculate DO_res_PHY: Oxygen consumption by phytoplankton respiration"""
        if 'do_phytoplankton_respiration' in self.cache:
            return self.cache['do_phytoplankton_respiration']

        PHY = self.phytoplankton.PHY
        KR_PHY = self.get_parameter('KR_PHY')[0]
        KR_T = self.get_parameter('K_T')[0]
        OC = self.get_parameter('OC')[0]

        RES_PHY = [KR_PHY * (KR_T ** (t - 20)) for t in self.T]
        DO_res_PHY = [phy * res_phy * OC for phy, res_phy in zip(PHY, RES_PHY)]

        self.cache['do_phytoplankton_respiration'] = DO_res_PHY
        return DO_res_PHY

    def do_macroalgal_respiration(self):
        """Calculate DO_res_MA: Oxygen consumption by macroalgal respiration"""
        if 'do_macroalgal_respiration' in self.cache:
            return self.cache['do_macroalgal_respiration']

        MA = self.macroalgal.MA
        A_MA = self.macroalgal.A_MA
        KR_MA = self.get_parameter('KR_MA')[0]
        KR_T = self.get_parameter('K_T')[0]
        OC = self.get_parameter('OC')[0]

        RES_MA = [KR_MA * (KR_T ** (t - 20)) for t in self.T]
        DO_res_MA = [ma * a_ma * res_ma * OC / v for ma, a_ma, res_ma, v in zip(MA, A_MA, RES_MA, self.V)]

        self.cache['do_macroalgal_respiration'] = DO_res_MA
        return DO_res_MA

    def do_shellfish_respiration(self, HSH):
        """Calculate DO_res_SH: Oxygen consumption by shellfish respiration"""
        if 'do_shellfish_respiration' in self.cache:
            return self.cache['do_shellfish_respiration']

        N_SH = self.shellfish.population_dynamics(HSH)
        p_C_SH = self.shellfish.catabolic_rate()

        DO_res_SH = [n_sh * p_c_sh / 14.31 / v for n_sh, p_c_sh, v in zip(N_SH, p_C_SH, self.V)]

        self.cache['do_shellfish_respiration'] = DO_res_SH
        return DO_res_SH

    def do_fish_respiration(self, HF):
        """Calculate DO_res_F: Oxygen consumption by fish respiration"""
        if 'do_fish_respiration' in self.cache:
            return self.cache['do_fish_respiration']

        N_F = self.fish.population_dynamics(HF)
        p_C_F = self.fish.catabolic_rate()

        DO_res_F = [n_f * p_c_f / 14.31 / v for n_f, p_c_f, v in zip(N_F, p_C_F, self.V)]

        self.cache['do_fish_respiration'] = DO_res_F
        return DO_res_F

    def do_nitrification(self):
        """Calculate DO_Nit: Oxygen consumption by nitrification"""
        if 'do_nitrification' in self.cache:
            return self.cache['do_nitrification']

        NitN = self.ammonium.nitrification()
        DO_Nit = [(64 / 14) * nit_n for nit_n in NitN]

        self.cache['do_nitrification'] = DO_Nit
        return DO_Nit

    def do_cbod_oxidation(self):
        """Calculate DO_CBOD: Oxygen consumption by CBOD oxidation"""
        return self.cbod.cbod_oxidation()

    def do_sediment_oxygen_demand(self):
        """Calculate DO_SOD: Oxygen consumption by sediment oxygen demand"""
        if 'do_sediment_oxygen_demand' in self.cache:
            return self.cache['do_sediment_oxygen_demand']

        DO_SOD = [(self.SOD / h) * (self.SODT ** (t - 20)) for h, t in zip(self.H, self.T)]

        self.cache['do_sediment_oxygen_demand'] = DO_SOD
        return DO_SOD

    def update_DO(self, HSH, HF):
        """Update the dissolved oxygen concentration in water"""
        if 'update_DO' in self.cache:
            return self.cache['update_DO']

        DO_atm = self.do_atmospheric_exchange()
        DO_PHY = self.do_phytoplankton_production()
        DO_MA = self.do_macroalgal_production()
        DO_res_PHY = self.do_phytoplankton_respiration()
        DO_res_MA = self.do_macroalgal_respiration()
        DO_res_SH = self.do_shellfish_respiration(HSH)
        DO_res_F = self.do_fish_respiration(HF)
        DO_Nit = self.do_nitrification()
        DO_CBOD = self.do_cbod_oxidation()
        DO_SOD = self.do_sediment_oxygen_demand()

        dDO_dt = [
            do_atm + do_phy + do_ma - do_res_phy - do_res_ma - do_res_sh - do_res_f - do_nit - do_cbod - do_sod + ex_do
            for do_atm, do_phy, do_ma, do_res_phy, do_res_ma, do_res_sh, do_res_f, do_nit, do_cbod, do_sod, ex_do
            in
            zip(DO_atm, DO_PHY, DO_MA, DO_res_PHY, DO_res_MA, DO_res_SH, DO_res_F, DO_Nit, DO_CBOD, DO_SOD, self.external_DO_input)]

        i = 4
        change = abs(DO_atm[i]) + abs(DO_PHY[i]) + abs(DO_MA[i]) + abs(DO_res_PHY[i]) + abs(DO_res_MA[i]) + abs(DO_res_SH[i]) + abs(DO_res_F[i]) + abs(DO_Nit[i]) + abs(DO_CBOD[i]) + abs(DO_SOD[i]) + abs(self.external_DO_input[i])
        print(f"dDO_dt: {dDO_dt[i]}, change: {change}, DO_atm:{DO_atm[i] / change}, DO_PHY:{DO_PHY[i] / change}, DO_MA:{DO_MA[i] / change}, DO_res_PHY:{DO_res_PHY[i] / change}, DO_res_MA:{DO_res_MA[i] / change}, DO_res_SH:{DO_res_SH[i] / change}, DO_res_F:{DO_res_F[i] / change}, DO_nit:{DO_Nit[i] / change}, DO_cbod:{DO_CBOD[i] / change}, DO_sod:{DO_SOD[i] / change}, ex_do:{self.external_DO_input[i] / change}")

        self.DO = [do + ddo for do, ddo in zip(self.DO, dDO_dt)]

        self.cache['update_DO'] = self.DO
        return self.DO

    def reset_cache(self):
        """Clear the cache at the end of each timestep"""
        self.cache.clear()



if __name__ == '__main__':
    root = tk.Tk()
    app = ParameterLoader(root)
    root.geometry("1000x600")
    root.mainloop()

    # Water exchange
    exchange_data_file = r'./database/Waterexchange_1h.csv'
    river_flow_file = r'./database/Riverflow_1h.csv'
    outer_sea_conc_file = r'./database/Outersea_1h.csv'
    water_exchange = WaterExchange(parameter_loader=app, exchange_data_file=exchange_data_file,
                                   outer_sea_conc_file=outer_sea_conc_file, river_flow_file=river_flow_file)

    # Model components
    phy = Phytoplankton(parameter_loader=app)
    zoo = Zooplankton(parameter_loader=app)
    macroalgal = Macroalgal(parameter_loader=app)
    shellfish = Shellfish(parameter_loader=app)
    fish = Fish(parameter_loader=app)
    ammonium = AmmoniumNitrogen(parameter_loader=app, phytoplankton=phy, macroalgal=macroalgal,
                                zooplankton=zoo, shellfish=shellfish, fish=fish)
    nitrate = NitrateNitrogen(parameter_loader=app, phytoplankton=phy, macroalgal=macroalgal)
    organic_nitrogen = OrganicNitrogen(parameter_loader=app, phytoplankton=phy, macroalgal=macroalgal,
                                       zooplankton=zoo, shellfish=shellfish, fish=fish)
    inorganic_phosphorus = InorganicPhosphorus(parameter_loader=app, phytoplankton=phy, macroalgal=macroalgal)
    organic_phosphorus = OrganicPhosphorus(parameter_loader=app, phytoplankton=phy, macroalgal=macroalgal,
                                           zooplankton=zoo, shellfish=shellfish, fish=fish,
                                           inorganic_phosphorus=inorganic_phosphorus)
    particulate_phosphorus = ParticulatePhosphorus(parameter_loader=app, phytoplankton=phy, zooplankton=zoo,
                                                   shellfish=shellfish, fish=fish)
    cbod = CBOD(parameter_loader=app, phytoplankton=phy, macroalgal=macroalgal,
                zooplankton=zoo, shellfish=shellfish, fish=fish, nitrate=nitrate)
    do = DissolvedOxygen(parameter_loader=app, phytoplankton=phy, macroalgal=macroalgal,
                          zooplankton=zoo, shellfish=shellfish, fish=fish, ammonium=ammonium, cbod=cbod)

    # Other inputs
    input_files = {
        'river': r'./database/Riverinput_1h.csv',
        'groundwater': r'./database/Groundwaterinput_1h.csv',
        'point_source': r'./database/Pointinput_1h.csv',
        'pond': r'./database/Pondinput_1h.csv',
        'atmosphere': r'./database/Atmosphereinput_1h.csv'
    }

    external_input = ExternalInput(parameter_loader=app, input_files=input_files, waterexchange=water_exchange)


    # Resets all caches at the end of each time step
    def reset_all_caches():
        phy.reset_cache()
        zoo.reset_cache()
        macroalgal.reset_internal_quotas_cache()
        macroalgal.reset_cache()
        shellfish.reset_cache()
        fish.reset_cache()
        ammonium.reset_cache()
        nitrate.reset_cache()
        organic_nitrogen.reset_cache()
        inorganic_phosphorus.reset_cache()
        organic_phosphorus.reset_cache()
        particulate_phosphorus.reset_cache()
        cbod.reset_cache()
        do.reset_cache()

    # Initialize empty lists for each metric to store results over time
    time_steps = []  # Stores each time step
    metrics_data = {
        'PHY': [[] for _ in range(20)],
        'ZOO': [[] for _ in range(20)],
        'MA': [[] for _ in range(20)],
        'V_SH': [[] for _ in range(20)],
        'V_F': [[] for _ in range(20)],
        'NH4': [[] for _ in range(20)],
        'NO3': [[] for _ in range(20)],
        'ON': [[] for _ in range(20)],
        'PO4': [[] for _ in range(20)],
        'OP': [[] for _ in range(20)],
        'PP': [[] for _ in range(20)],
        'CBOD': [[] for _ in range(20)],
        'DO': [[] for _ in range(20)]
    }

    # Main loop
    for timestep in range(24*12*30):  # Assuming 100 time steps
        print(f"Timestep: {timestep}")
        # print(f"Timestep: {timestep} - Initial NO3: {nitrate.NO3}")
        GRZ = zoo.grazing_rate()
        MAS = [0 for _ in macroalgal.MA]
        HMA = [0.8 if (timestep + 1) % (24*30*3) == 0 else 0 for _ in macroalgal.MA]
        HSH = [0 for _ in shellfish.N_SH]
        HF = [0 for _ in fish.N_F]

        # External inputs
        external_inputs = external_input.get_external_inputs(timestep)

        # print(f"Timestep: {timestep} - External inputs: {external_inputs['NO3']}")

        # Update the internal nitrogen and phosphorus concentrations
        new_qP = macroalgal.update_internal_quotas()[7]
        new_qN = macroalgal.update_internal_quotas()[3]
        print(f"Timestep {timestep} - q_N: {new_qN}")

        ammonium.set_external_input(external_inputs['NH4'])
        nitrate.set_external_input(external_inputs['NO3'])
        organic_nitrogen.set_external_input(external_inputs['ON'])
        inorganic_phosphorus.set_external_input(external_inputs['PO4'])
        organic_phosphorus.set_external_input(external_inputs['OP'])
        cbod.set_external_input(external_inputs['CBOD'])
        do.set_external_input(external_inputs['DO'])

        # Update the parameters with the new external inputs
        new_V = water_exchange.calculate_volume(timestep)
        new_N_SH, new_V_SH, new_E_SH, new_E_R_SH, GRS_PHY = shellfish.update_shellfish(HSH)
        new_N_F, new_V_F, new_E_F, new_E_R_F = fish.update_fish(HF)
        new_PHY = phy.update_PHY(GRZ, GRS_PHY)
        new_ZOO = zoo.update_ZOO()
        new_MA = macroalgal.update_MA(MAS, HMA)
        new_NH4 = ammonium.update_NH4()
        new_NO3 = nitrate.update_NO3()
        new_ON = organic_nitrogen.update_ON()
        new_PO4 = inorganic_phosphorus.update_PO4()
        new_OP = organic_phosphorus.update_OP()
        new_PP = particulate_phosphorus.update_PP()
        new_CBOD = cbod.update_CBOD()
        new_DO = do.update_DO(HSH, HF)

        # Water exchange
        water_exchange_params = {
            'PHY': new_PHY,
            'ZOO': new_ZOO,
            'NH4': new_NH4,
            'NO3': new_NO3,
            'ON': new_ON,
            'PO4': new_PO4,
            'OP': new_OP,
            'PP': new_PP,
            'CBOD': new_CBOD,
            'DO': new_DO
        }

        direct_update_params = {
            'V': new_V,
            'V_SH': new_V_SH,
            'N_SH': new_N_SH,
            'E_SH': new_E_SH,
            'E_R_SH': new_E_R_SH,
            'N_F': new_N_F,
            'V_F': new_V_F,
            'E_F': new_E_F,
            'E_R_F': new_E_R_F,
            'MA': new_MA,
            'qP': new_qP,
            'qN': new_qN
        }

        updated_concentrations = water_exchange.exchange(water_exchange_params, timestep + 1)

        # Update the parameters with the new concentrations
        app.update_initial_values(direct_update_params)
        app.update_initial_values(updated_concentrations)

        time_steps.append(timestep)

        # Store values for each area in the 20-element vector for each metric
        for i in range(20):  # Loop through each sea area
            metrics_data['PHY'][i].append(new_PHY[i])
            metrics_data['ZOO'][i].append(new_ZOO[i])
            metrics_data['MA'][i].append(new_MA[i])
            metrics_data['V_SH'][i].append(new_N_SH[i])
            metrics_data['V_F'][i].append(new_N_F[i])
            metrics_data['NH4'][i].append(new_NH4[i])
            metrics_data['NO3'][i].append(new_NO3[i])
            metrics_data['ON'][i].append(new_ON[i])
            metrics_data['PO4'][i].append(new_PO4[i])
            metrics_data['OP'][i].append(new_OP[i])
            metrics_data['PP'][i].append(new_PP[i])
            metrics_data['CBOD'][i].append(new_CBOD[i])
            metrics_data['DO'][i].append(new_DO[i])

        # print(f"Timestep: {timestep}")
        # print(f"Updated V: {new_V} m³")
        # print(f"Updated PHY: {new_PHY} mgC/L")
        # print(f"Updated ZOO: {new_ZOO} mgC/L")
        # print(f"Updated MA: {new_MA} gD/m^2")
        # print(f"Updated N_SH: {new_N_SH} individuals")
        # print(f"Updated V_SH: {new_V_SH} cm³")
        # print(f"Updated E_SH: {new_E_SH} J")
        # print(f"Updated E_R_SH: {new_E_R_SH} J")
        # print(f"Updated N_F: {new_N_F} individuals")
        # print(f"Updated V_F: {new_V_F} cm³")
        # print(f"Updated E_F: {new_E_F} J")
        # print(f"Updated E_R_F: {new_E_R_F} J")
        # print(f"Updated NH4: {new_NH4} mgN/L")
        # print(f"Updated NO3: {new_NO3} mgN/L")
        # print(f"Updated ON: {new_ON} mgN/L")
        # print(f"Updated PO4: {new_PO4} mgP/L")
        # print(f"Updated OP: {new_OP} mgP/L")
        # print(f"Updated CBOD: {new_CBOD} mgO₂/L")
        # print(f"Updated DO: {new_DO} mgO₂/L")

        # print(f"Timestep: {timestep} - Updated NO3: {new_NO3}")
        reset_all_caches()  # Reset all caches at the end of each time step


    def plot_metric_with_subplots(time_steps, metric_values, metric_name):
        fig, axes = plt.subplots(4, 6, figsize=(15, 10), sharex=True, sharey=False)
        fig.suptitle(f"{metric_name} Concentration Over Time in Each Sea Area", fontsize=16)

        # Flatten the axes array for easy indexing
        axes = axes.flatten()

        for i in range(20):
            axes[i].plot(time_steps, metric_values[i], label=f'Area {i + 1}')
            axes[i].set_title(f'Area {i + 1}', fontsize=10)
            axes[i].grid(True)
            if i % 6 == 0:
                axes[i].set_ylabel("Concentration")
            if i >= 18:
                axes[i].set_xlabel("Time Steps")

        plt.tight_layout(rect=[0, 0, 1, 0.95])  # Adjust layout to fit title
        plt.show()

    # Call the plotting function for each metric after the simulation loop
    for metric, values in metrics_data.items():
        plot_metric_with_subplots(time_steps, values, metric)

