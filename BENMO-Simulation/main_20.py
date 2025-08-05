#!/usr/bin/env python
# encoding: utf-8
import tkinter as tk
import argparse
import numpy as np
import pandas as pd
from tqdm import tqdm
import threading
from BENMO_20 import (ParameterLoader, WaterExchange, ExternalInput, Phytoplankton, Zooplankton, Macroalgal, Shellfish,
                      Fish, AmmoniumNitrogen, NitrateNitrogen, OrganicNitrogen, InorganicPhosphorus, OrganicPhosphorus,
                      ParticulatePhosphorus)  # 从原代码导入必要类

# --------------------------
# 调试框架配置
# --------------------------
SIM_DAYS = 365*3 # 模拟天数
TIME_STEP = 1  # 时间步长（小时）
PLOT_ZONE = 6  # 选择要可视化的区域编号（0-23） # 0——贝+鱼，1——贝+鱼+藻，3——全无

# --------------------------
# CLI 参数解析
# --------------------------
parser = argparse.ArgumentParser()
parser.add_argument('--no-gui', action='store_true', help='Disable GUI for parameter loading')
args = parser.parse_args()

# --------------------------
# 参数加载器
# --------------------------
root = tk.Tk()
app = ParameterLoader(root)
root.geometry("1000x600")
def auto_run():
    root.after(1000, app.save_and_continue)
threading.Thread(target=auto_run).start()
root.mainloop()

# --------------------------
# 初始化水交换模块（使用示例数据）
# --------------------------
outer_sea_scaling = {
    'NO3': 10.0,
    'NH4': 20.0,
    'PO4': 10.0
}

water_exchange = WaterExchange(
    parameter_loader=app,
    exchange_data_file="E:/亿方云/FangcloudV2/collab_space/2023-黄喆晗/04 科研工作/人海耦合环境社会经济大模型/代码整理/过程数据/水交换计算/cleaned_class_exchange_flux_extended.csv",  # 用实际路径替换
    outer_sea_conc_file="./database/Outersea_1h_new.csv",      # 用实际路径替换
    river_flow_file="./database/Riverflow_1h.csv",         # 用实际路径替换
    outer_sea_scaling=outer_sea_scaling,
    time_step=TIME_STEP
)

# --------------------------

# --
# --------------------------
input_files = {
        'river': r'./database/Riverinput_1h_20.csv',
        'groundwater': r'./database/Groundwaterinput_1h_20.csv',
        'point_source': r'./database/Pointinput_1h_20.csv',
        'pond': r'./database/Pondinput_1h_20.csv',
        'atmosphere': r'./database/Atmosphereinput_1h_20.csv'
    }

input_multipliers = {
    'river': {'NH4': 1.0, 'NO3': 5, 'ON': 1.0, 'PO4': 1.0, 'OP': 1.0, 'CBOD': 1.0, 'DO': 1.0},
    'groundwater': {'NH4': 48, 'NO3': 55, 'ON': 15, 'PO4': 50, 'OP': 15, 'CBOD': 15, 'DO': 15}, # 48
    'point_source': {'NH4': 6, 'NO3': 150, 'ON': 10, 'PO4': 60, 'OP': 1.0, 'CBOD': 1.0, 'DO': 1.0}, # 6
    'pond': {'NH4': 5, 'NO3': 100, 'ON': 1.0, 'PO4': 20, 'OP': 1.0, 'CBOD': 1.0, 'DO': 1.0}, # 5
    'atmosphere': {'NH4': 1.0, 'NO3': 10, 'ON': 1.0, 'PO4': 2.0, 'OP': 1.0, 'CBOD': 1.0, 'DO': 1.0}
}

external_input = ExternalInput(parameter_loader=app, input_files=input_files, waterexchange=water_exchange, input_multipliers=input_multipliers)

# --------------------------
# 初始化环境参数记录列表
# --------------------------
T_values = []      # 温度记录
I_values = []      # 光照记录
DO_values = []     # 溶解氧浓度
H_values = []      # H值记录

NH4_values = []    # 铵盐浓度
NH4_all_zones = []  # 每时刻记录所有 20 个海区的 NH₄ 浓度
NO3_values = []    # 硝酸盐浓度
NO3_all_zones = []  # 每时刻记录所有 20 个海区的 NO₃ 浓度
ON_values = []     # 有机氮浓度
ON_all_zones = []  # 每时刻记录所有 20 个海区的 ON 浓度
PO4_values = []    # 磷酸盐浓度
PO4_all_zones = []  # 每时刻记录所有 20 个海区的 PO₄ 浓度
OP_values = []     # 总磷浓度
OP_all_zones = []  # 每时刻记录所有 20 个海区的 OP 浓度
PP_values = []     # 颗粒态磷浓度
PP_all_zones = []  # 每时刻记录所有 20 个海区的 PP 浓度

# --------------------------
# 自定义外部输入生成器（替换实际数据源）
# --------------------------
def generate_external_inputs(t):
    """生成动态环境参数（示例随机扰动）"""
    return {
        'T': [20 + 5 * np.sin(t / 24 * 2 * np.pi) + np.random.normal(0, 1) for _ in range(20)],
        'I': [700000 + 100000 * np.sin(t / 12 * np.pi) for _ in range(20)],
        # 'NH4': [0.02 * (1 + 0.1 * np.random.randn()) for _ in range(20)],
        # 'NO3': [0.6 * (1 + 0.1 * np.random.randn()) for _ in range(20)],
        # 'ON' : [0.1 * (1 + 0.01 * np.random.randn()) for _ in range(20)],
        # 'PO4': [0.04 * (1 + 0.1 * np.random.randn()) for _ in range(20)],
        # 'OP' : [0.01 * (1 + 0.01 * np.random.randn()) for _ in range(20)],
        'DO' : [6.65 * (1 + 0.1 * np.random.randn()) for _ in range(20)]
    }

# --------------------------
# 新增水深更新函数
# --------------------------
def update_water_depth(V, A, H_initial):
    new_H = [max(0.1, v / a) if a > 0 else H_initial[i] for i, (v, a) in enumerate(zip(V, A))]
    return new_H

# --------------------------
# 主模拟循环
# --------------------------
phy_biomass = []  # 记录浮游植物生物量
zoo_biomass = []  # 记录浮游动物生物量
macro_phy_biomass = []  # 记录大型藻类生物量
shellfish_N_SH_values = []  # 记录贝类数量
shellfish_V_SH_values = []  # 记录贝类体积
fish_N_F_values = []  # 记录鱼类数量
fish_V_F_values = []  # 记录鱼类体积
timesteps = list(range(SIM_DAYS * 24 // TIME_STEP))  # 生成时间步序列

# 重置初始参数
N_SH_initial = [3785804.438, 0, 0, 126336979.3, 4183871.842, 0, 227012456.3, 55525559.94, 0, 377535149.1, 330634099.3, 0, 0, 3679995.239, 1215077545, 61342563.2, 2427940.471, 236319257.8, 18026278.35, 0]
V_SH_initial = 0.6
N_F_initial = [0, 0, 36308132.92, 11246959.3, 79615100.35, 13866717.11, 1982687.219, 12612384.08, 8110870.655, 667060.6129, 119289.1572, 51539474.79, 73837822.43, 11257092.76, 9406260.351, 0, 11079676.28, 15923493.26, 19494348.39, 4090630.33]
V_F_initial = 5.0
FEED_NH3 = app.get_parameter('FEED_NH3')[0]
FEED_NO3 = app.get_parameter('FEED_NO3')[0]
FEED_ON = app.get_parameter('FEED_ON')[0]
FEED_PO4 = app.get_parameter('FEED_PO4')[0]
FEED_OP = app.get_parameter('FEED_OP')[0]
FEED_PP = app.get_parameter('FEED_PP')[0]
EFF = app.get_parameter('EFF')[0]
f_fec = app.get_parameter('f_fec')[0]
NC_PHY = app.get_parameter('NC_PHY')[0]
PC_PHY = app.get_parameter('PC_PHY')[0]

# 导入所需类
phy = Phytoplankton(parameter_loader=app)
zoo = Zooplankton(parameter_loader=app)
macro_phy = Macroalgal(parameter_loader=app)
shellfish = Shellfish(parameter_loader=app)
fish = Fish(parameter_loader=app)
ammonia = AmmoniumNitrogen(parameter_loader=app, phytoplankton=phy, macroalgal=macro_phy, zooplankton=zoo, shellfish=shellfish, fish=fish)
nitrate = NitrateNitrogen(parameter_loader=app, phytoplankton=phy, macroalgal=macro_phy)
organic_ammonia = OrganicNitrogen(parameter_loader=app, phytoplankton=phy, macroalgal=macro_phy, zooplankton=zoo, shellfish=shellfish, fish=fish)
inorganic_phosphorus = InorganicPhosphorus(parameter_loader=app, phytoplankton=phy, macroalgal=macro_phy)
organic_phosphorus = OrganicPhosphorus(parameter_loader=app, phytoplankton=phy, macroalgal=macro_phy, zooplankton=zoo,
                                       shellfish=shellfish, fish=fish, inorganic_phosphorus=inorganic_phosphorus)
particulate_phosphorus = ParticulatePhosphorus(parameter_loader=app, phytoplankton=phy,  zooplankton=zoo, shellfish=shellfish, fish=fish)

contributions_record = {
    'ammonia': {
        'external_input': np.zeros(20),
        'phy_release': np.zeros(20),
        'phy_absorption': np.zeros(20),
        'ma_release': np.zeros(20),
        'ma_absorption': np.zeros(20),
        'sh_excretion': np.zeros(20),
        'f_excretion': np.zeros(20),
        'nitrification': np.zeros(20),
        'mineralization_NH4': np.zeros(20),
        'feed': np.zeros(20)
    },
    'nitrate':{
        'external_input': np.zeros(20),
        'nitrification': np.zeros(20),
        'phy_absorption': np.zeros(20),
        'ma_absorption': np.zeros(20),
        'denitrification': np.zeros(20),
        'feed': np.zeros(20)
    },
    'organic_ammonia':{
        'external_input': np.zeros(20),
        'phy_release': np.zeros(20),
        'zoo_release': np.zeros(20),
        'ma_release': np.zeros(20),
        'sh_release': np.zeros(20),
        'f_release': np.zeros(20),
        'mineralization_ON': np.zeros(20),
        'feed': np.zeros(20)
    },
    'inorganic_phosphorus':{
        'external_input': np.zeros(20),
        'phy_release': np.zeros(20),
        'phy_absorption': np.zeros(20),
        'ma_release': np.zeros(20),
        'ma_absorption': np.zeros(20),
        'mineralization_PO4': np.zeros(20),
        'particulate_ads_des': np.zeros(20),
        'feed': np.zeros(20)
    },
    'organic_phosphorus':{
        'external_input': np.zeros(20),
        'phy_release': np.zeros(20),
        'zoo_release': np.zeros(20),
        'ma_release': np.zeros(20),
        'sh_release': np.zeros(20),
        'f_release': np.zeros(20),
        'mineralization_OP': np.zeros(20),
        'feed': np.zeros(20)
    },
    'particulate_phosphorus':{
        'zoo_release': np.zeros(20),
        'sh_release': np.zeros(20),
        'f_release': np.zeros(20),
        'ads_des': np.zeros(20),
        'set_resus': np.zeros(20),
        'feed': np.zeros(20)
    }
}

exported_mass = {
    'ammonia': 0.0,
    'nitrate': 0.0,
    'organic_ammonia': 0.0,
    'inorganic_phosphorus': 0.0,
    'organic_phosphorus': 0.0,
    'particulate_phosphorus': 0.0
}
import_mass = exported_mass.copy()

outer_idx = water_exchange.sea_areas.index('OuterSea')

LITERS_PER_M3 = 1000.0

def record_contributions(nutrient: str, data: dict, vol: np.ndarray):
    factor = vol * LITERS_PER_M3  # L
    for key, arr in data.items():
        mass = np.abs(arr * factor)  # mg
        contributions_record[nutrient][key] += mass

for t in tqdm(timesteps, desc="模拟进度", ncols=100):
# for t in timesteps:
    # 1. 注入外部环境参数
    external_data = generate_external_inputs(t)
    external_inputs = external_input.get_external_inputs(t)
    app.update_initial_values(external_data)
    phy.reload_parameters()
    zoo.reload_parameters()
    macro_phy.reload_parameters()
    shellfish.reload_parameters()
    fish.reload_parameters()
    ammonia.reload_parameters()
    nitrate.reload_parameters()
    organic_ammonia.reload_parameters()
    inorganic_phosphorus.reload_parameters()
    organic_phosphorus.reload_parameters()
    particulate_phosphorus.reload_parameters()
    volume = np.array(water_exchange.calculate_volume(t)[:20])
    W = water_exchange.water_exchange_matrix
    flux_to_outer = W[:20, outer_idx, t]
    flux_from_outer = W[outer_idx, :20, t]

    # 2.1 执行贝类生长计算
    shellfish.reset_cache()  # 清除缓存确保使用新参数
    shellfish_V_growth = np.array(shellfish.growth_volume())
    shellfish_grs = np.array(shellfish.GRS_PHY()) # 计算贝类对浮游生物的捕食率
    shellfish.V_SH = shellfish.V_SH + shellfish_V_growth
    if (t + 1) % (24 * 30 * 6) == 1:
        shellfish.V_SH = np.full(20, V_SH_initial)
    harvest_flag = (t + 1) % (24 * 30 * 6) == 0
    harvest_rate = 1.0 if harvest_flag else 0.0
    shellfish.N_SH = np.maximum(0, shellfish.N_SH * (1 - shellfish.DSH - harvest_rate))
    if (t + 1) % (24 * 30 * 6) == 1:
        shellfish.N_SH = N_SH_initial.copy()

    # 2.2 执行鱼类生长计算
    fish.reset_cache()  # 清除缓存确保使用新参数
    fish_V_growth = np.array(fish.growth_volume())
    fish.V_F = fish.V_F + fish_V_growth
    if (t + 1) % (24 * 30 * 12) == 1:
        fish.V_F = np.full(20, V_F_initial)
    harvest_flag = (t + 1) % (24 * 30 * 12) == 0
    harvest_rate = 1.0 if harvest_flag else 0.0
    fish.N_F = np.maximum(0, fish.N_F * (1 - fish.DF - harvest_rate))
    if (t + 1) % (24 * 30 * 12) == 1:
        fish.N_F = N_F_initial.copy()

    # 2.3 执行浮游动物生长计算
    zoo.reset_cache()  # 清除缓存确保使用新参数
    zoo_grazing_rate = np.array(zoo.grazing_rate())
    zoo_growth_rate = np.array(zoo.growth_rate())
    zoo_loss_rate = np.array(zoo.loss_rate())
    delta_ZOO = zoo_growth_rate - zoo_loss_rate - shellfish_grs
    zoo.ZOO = np.maximum(1e-12, zoo.ZOO * (1 + delta_ZOO))

    # 2.4 执行浮游植物生长计算
    phy.reset_cache()  # 清除缓存确保使用新参数
    phy_growth_rate = np.array(phy.growth_rate())
    phy_loss_rate = np.array(phy.loss_rate())
    phy_growth_rate = np.real_if_close(phy_growth_rate, tol=1e-13)
    phy_loss_rate = np.real_if_close(phy_loss_rate, tol=1e-13)
    delta_PHY = phy_growth_rate - phy_loss_rate - zoo_grazing_rate - shellfish_grs
    phy.PHY = np.maximum(1e-12, phy.PHY * (1 + delta_PHY))

    # 2.5 执行大型藻类生长计算
    macro_phy.reset_cache()  # 清除缓存确保使用新参数
    macro_phy_growth_rate = np.array(macro_phy.calculate_GMA())
    macro_phy_loss_rate = np.array(macro_phy.calculate_loss_rate())
    harvest_flag_MA = (t + 1) % (24 * 30 * 3) == 0
    harvest_rate = 0.8 if harvest_flag_MA else 0.0
    delta_MA = macro_phy_growth_rate - macro_phy_loss_rate - harvest_rate
    macro_phy.MA = np.maximum(1e-12, macro_phy.MA * (1 + delta_MA))

    # 3.1 氨氮浓度变化模拟
    ammonia.reset_cache()
    ammonia.set_external_input(external_inputs['NH4'])
    ammonia_external_input = ammonia.external_input

    ammonia_phy_release = np.array(ammonia.phytoplankton_ammonium_release()) * phy_loss_rate * phy.PHY
    ammonia_phy_absorption = np.array(ammonia.phytoplankton_ammonium_absorption()[0]) * phy_growth_rate * phy.PHY
    ammonia_ma_release = np.array(ammonia.macroalgal_ammonium_release())
    ammonia_ma_absorption = np.array(ammonia.macroalgal_ammonium_absorption()[0])
    ammonia_sh_excretion = np.array(ammonia.shellfish_ammonium_excretion()) * shellfish.N_SH / (volume * 1000)
    ammonia_f_excretion = np.array(ammonia.fish_ammonium_excretion()) * fish.N_F / (volume * 1000)
    ammonia_nitrification = np.array(ammonia.nitrification())
    ammonia_mineralization = np.array(ammonia.mineralization())
    ammonia_feed = (0.8 * FEED_NH3 * np.array(ammonia.FEED) / (24 * 30 * 12) / 1000) / volume

    ammonia_data = {
        'external_input': np.array(ammonia.external_input),
        'phy_release': ammonia_phy_release,
        'phy_absorption': -ammonia_phy_absorption,
        'ma_release': ammonia_ma_release,
        'ma_absorption': -ammonia_ma_absorption,
        'sh_excretion': ammonia_sh_excretion,
        'f_excretion': ammonia_f_excretion,
        'nitrification': -ammonia_nitrification,
        'mineralization_NH4': ammonia_mineralization,
        'feed': ammonia_feed
    }

    record_contributions('ammonia', ammonia_data, volume)
    NH4_before_exchange = ammonia.NH4 + sum(ammonia_data.values())
    exported_mass['ammonia'] += np.sum(flux_to_outer * NH4_before_exchange * 1000.0)
    import_mass['ammonia'] += np.sum(flux_from_outer * 2 * water_exchange.outer_sea_concentrations['NH4'][t] * 1000.0)

    # 3.2 硝氮浓度变化模拟
    nitrate.reset_cache()
    nitrate.set_external_input(external_inputs['NO3'])
    nitrate_external_input = nitrate.external_input

    nitrate_phy_absorption = np.array(nitrate.phytoplankton_nitrate_absorption()) * phy_growth_rate * phy.PHY
    nitrate_ma_absorption = np.array(nitrate.macroalgal_nitrate_absorption())
    nitrate_denitrification = np.array(nitrate.denitrification())
    nitrate_feed = (0.8 * FEED_NO3 * np.array(nitrate.FEED) / (24 * 30 * 12) / 1000) / volume

    nitrate_data = {
        'external_input': np.array(nitrate_external_input),
        'nitrification': ammonia_nitrification,
        'phy_absorption': -nitrate_phy_absorption,
        'ma_absorption': -nitrate_ma_absorption,
        'denitrification': -nitrate_denitrification,
        'feed': nitrate_feed
    }

    record_contributions('nitrate', nitrate_data, volume)
    NO3_before_exchange = nitrate.NO3 + sum(nitrate_data.values())
    exported_mass['nitrate'] += np.sum(flux_to_outer * NO3_before_exchange * 1000.0)
    import_mass['nitrate'] += np.sum(flux_from_outer * 2 * water_exchange.outer_sea_concentrations['NO3'][t] * 1000.0)

    # 3.3 有机氮浓度变化模拟
    organic_ammonia.reset_cache()
    organic_ammonia.set_external_input(external_inputs['ON'])
    organic_ammonia_external_input = organic_ammonia.external_input

    organic_ammonia_phy_release = np.array(organic_ammonia.phytoplankton_on_release()) * phy_loss_rate * phy.PHY
    organic_ammonia_ma_release = np.array(organic_ammonia.macroalgal_on_release())
    organic_ammonia_zoo_release = ((1 - EFF) * zoo_grazing_rate + zoo_loss_rate) * NC_PHY
    organic_ammonia_sh_release = np.array(organic_ammonia.shellfish_on_release())
    organic_ammonia_f_release = np.array(organic_ammonia.fish_on_release())
    organic_ammonia_mineralization = np.array(organic_ammonia.mineralization())
    organic_ammonia_feed = (0.8 * FEED_ON * np.array(organic_ammonia.FEED) / (24 * 30 * 12) / 1000) / volume

    organic_ammonia_data = {
        'external_input': np.array(organic_ammonia_external_input),
        'phy_release': organic_ammonia_phy_release,
        'zoo_release': organic_ammonia_zoo_release,
        'ma_release': organic_ammonia_ma_release,
        'sh_release': organic_ammonia_sh_release,
        'f_release': organic_ammonia_f_release,
        'mineralization_ON': -organic_ammonia_mineralization,
        'feed': organic_ammonia_feed
    }

    record_contributions('organic_ammonia', organic_ammonia_data, volume)
    ON_before_exchange = organic_ammonia.ON + sum(organic_ammonia_data.values())
    exported_mass['organic_ammonia'] += np.sum(flux_to_outer * ON_before_exchange * 1000.0)
    import_mass['organic_ammonia'] += np.sum(flux_from_outer * 2 * water_exchange.outer_sea_concentrations['ON'][t] * 1000.0)

    # 3.4 无机磷酸盐浓度变化模拟
    inorganic_phosphorus.reset_cache()
    inorganic_phosphorus.set_external_input(external_inputs['PO4'])
    inorganic_phosphorus_external_input = inorganic_phosphorus.external_input

    inorganic_phosphorus_phy_release = (np.array(inorganic_phosphorus.phytoplankton_phosphate_release()) * phy_loss_rate * phy.PHY)
    inorganic_phosphorus_ma_release = np.array(inorganic_phosphorus.macroalgal_phosphate_release())
    inorganic_phosphorus_phy_absorption = PC_PHY * phy_growth_rate * phy.PHY
    inorganic_phosphorus_ma_absorption = np.array(inorganic_phosphorus.macroalgal_phosphate_absorption())
    inorganic_phosphorus_mineralization = np.array(inorganic_phosphorus.phosphate_mineralization())
    particulate_phosphorus_ads_des = np.array(particulate_phosphorus.adsorption_and_desorption())
    inorganic_phosphorus_feed = (0.8 * FEED_PO4 * np.array(inorganic_phosphorus.FEED) / (24 * 30 * 12) / 1000) / volume

    inorganic_phosphorus_data = {
        'external_input': np.array(inorganic_phosphorus_external_input),
        'phy_release': inorganic_phosphorus_phy_release,
        'phy_absorption': -inorganic_phosphorus_phy_absorption,
        'ma_release': inorganic_phosphorus_ma_release,
        'ma_absorption': -inorganic_phosphorus_ma_absorption,
        'mineralization_PO4': inorganic_phosphorus_mineralization,
        'particulate_ads_des': -particulate_phosphorus_ads_des,
        'feed': inorganic_phosphorus_feed
    }

    record_contributions('inorganic_phosphorus', inorganic_phosphorus_data, volume)
    PO4_before_exchange = inorganic_phosphorus.PO4[:20] + sum(inorganic_phosphorus_data.values())
    exported_mass['inorganic_phosphorus'] += np.sum(flux_to_outer * PO4_before_exchange * 1000.0)
    import_mass['inorganic_phosphorus'] += np.sum(flux_from_outer * 2 * water_exchange.outer_sea_concentrations['PO4'][t] * 1000.0)

    # Debugging: 输出浓度变化
    # if t % 1 == 0:  # 每天输出一次
    #     zone = PLOT_ZONE
    #     print(f"\n--- Timestep {t} | Zone {zone} PO4 Update Breakdown ---")
    #     for k in inorganic_phosphorus_data:
    #         print(f"{k:16s}: {inorganic_phosphorus_data[k][zone]:+.6f}")
    #     print(f"Before Exchange PO4: {inorganic_phosphorus.PO4[zone]:.5f}")
    #     print(f"After Bio-Update   : {PO4_before_exchange[zone]:.5f}")

    # 3.5 有机磷酸盐浓度变化模拟
    organic_phosphorus.reset_cache()
    organic_phosphorus.set_external_input(external_inputs['OP'])
    organic_phosphorus_external_input = organic_phosphorus.external_input

    organic_phosphorus_phy_release = (np.array(organic_phosphorus.phytoplankton_op_release()) * phy_loss_rate * phy.PHY)
    organic_phosphorus_ma_release = np.array(organic_phosphorus.macroalgal_op_release())
    organic_phosphorus_zoo_release = ((1 - f_fec) * (1 - EFF) * zoo_grazing_rate + zoo_loss_rate) * PC_PHY
    organic_phosphorus_sh_release = np.array(organic_phosphorus.shellfish_op_release())
    organic_phosphorus_f_release = np.array(organic_phosphorus.fish_op_release())
    organic_phosphorus_mineralization = np.array(organic_phosphorus.phosphate_mineralization())
    organic_phosphorus_feed = (0.8 * FEED_OP * np.array(organic_phosphorus.FEED) / (24 * 30 * 12) / 1000) / volume

    organic_phosphorus_data = {
        'external_input': np.array(organic_phosphorus_external_input),
        'phy_release': organic_phosphorus_phy_release,
        'zoo_release': organic_phosphorus_zoo_release,
        'ma_release': organic_phosphorus_ma_release,
        'sh_release': organic_phosphorus_sh_release,
        'f_release': organic_phosphorus_f_release,
        'mineralization_OP': -organic_phosphorus_mineralization,
        'feed': organic_phosphorus_feed
    }

    record_contributions('organic_phosphorus', organic_phosphorus_data, volume)
    OP_before_exchange = organic_phosphorus.OP[:20] + sum(organic_phosphorus_data.values())
    exported_mass['organic_phosphorus'] += np.sum(flux_to_outer * OP_before_exchange * 1000.0)
    import_mass['organic_phosphorus'] += np.sum(flux_from_outer * 2 * water_exchange.outer_sea_concentrations['OP'][t] * 1000.0)

    # 3.6 颗粒态磷酸盐浓度变化模拟
    particulate_phosphorus.reset_cache()

    particulate_phosphorus_zoo_release = (f_fec * (1 - EFF) * zoo_grazing_rate + zoo_loss_rate) * PC_PHY
    particulate_phosphorus_sh_release = np.array(particulate_phosphorus.shellfish_pp_release())
    particulate_phosphorus_f_release = np.array(particulate_phosphorus.fish_pp_release())
    particulate_phosphorus_ads_des = np.array(particulate_phosphorus.adsorption_and_desorption())
    particulate_phosphorus_set_resus = np.array(particulate_phosphorus.sink_and_resuspension())
    particulate_phosphorus_feed = (0.8 * FEED_PP * np.array(particulate_phosphorus.FEED) / (24 * 30 * 12) / 1000) / volume

    particulate_phosphorus_data = {
        'zoo_release': particulate_phosphorus_zoo_release,
        'sh_release': particulate_phosphorus_sh_release,
        'f_release': particulate_phosphorus_f_release,
        'ads_des': particulate_phosphorus_ads_des,
        'set_resus': -particulate_phosphorus_set_resus,
        'feed': particulate_phosphorus_feed
    }

    record_contributions('particulate_phosphorus', particulate_phosphorus_data, volume)
    PP_before_exchange = particulate_phosphorus.PP[:20] + sum(particulate_phosphorus_data.values())
    exported_mass['particulate_phosphorus'] += np.sum(flux_to_outer * PP_before_exchange * 1000.0)
    import_mass['particulate_phosphorus'] += np.sum(flux_from_outer * 0 * 1000.0)

    # 4. 水交换模拟
    water_exchange_params = {'PHY': phy.PHY, 'ZOO': zoo.ZOO, 'NH4': NH4_before_exchange, 'NO3': NO3_before_exchange,
                             'ON': ON_before_exchange, 'PO4': PO4_before_exchange, 'OP': OP_before_exchange, 'PP': PP_before_exchange}
    exchanged = water_exchange.exchange(water_exchange_params, t)

    # 4.1 获取当前水量和面积（从 water_exchange 中提取）
    current_volume = water_exchange.calculate_volume(t)
    area = app.get_parameter('A')

    # 4.2 更新水深（H）
    initial_H = app.get_parameter('H')
    new_H = update_water_depth(current_volume, area, initial_H)
    app.update_initial_values({'H': new_H})

    # 4.3 更新交换量
    # 更新交换后状态（向量裁剪 + 赋值）
    phy.PHY = np.clip(exchanged['PHY'][:20], 0.005, 0.1)
    zoo.ZOO = np.clip(exchanged['ZOO'][:20], 0.005, 0.1)
    ammonia.NH4 = np.clip(exchanged['NH4'][:20], 0.005, 0.2)
    nitrate.NO3 = np.clip(exchanged['NO3'][:20], 1E-12, 1.5)
    organic_ammonia.ON = np.clip(exchanged['ON'][:20], 1E-12, 0.5)
    inorganic_phosphorus.PO4 = np.clip(exchanged['PO4'][:20], 0.005, 0.15)
    organic_phosphorus.OP = np.clip(exchanged['OP'][:20], 0.005, 0.15)
    particulate_phosphorus.PP = np.clip(exchanged['PP'][:20], 0.005, 0.15)

    # if t % 1 == 0:
    #     zone = PLOT_ZONE
    #     print(f"After Exchange     : {inorganic_phosphorus.PO4[zone]:.5f}")
    #     print(f"Δ total step PO4   : {inorganic_phosphorus.PO4[zone] - PO4_values[-1] if PO4_values else 0:+.5f}")

    app.update_initial_values({'PHY': phy.PHY,
                               'ZOO': zoo.ZOO,
                               'MA': macro_phy.MA,
                               'N_SH': shellfish.N_SH, 'V_SH': shellfish.V_SH,
                               'V_F': fish.V_F, 'N_F': fish.N_F,
                               'NH4': ammonia.NH4,
                               'NO3': nitrate.NO3,
                               'ON': organic_ammonia.ON,
                               'PO4': inorganic_phosphorus.PO4,
                               'OP': organic_phosphorus.OP,
                               'PP': particulate_phosphorus.PP})

    # 5. 记录结果
    phy_biomass.append(phy.PHY[PLOT_ZONE])
    zoo_biomass.append(zoo.ZOO[PLOT_ZONE])
    macro_phy_biomass.append(macro_phy.MA[PLOT_ZONE])
    shellfish_N_SH_values.append(shellfish.N_SH[PLOT_ZONE])
    shellfish_V_SH_values.append(shellfish.V_SH[PLOT_ZONE])
    fish_N_F_values.append(fish.N_F[PLOT_ZONE])
    fish_V_F_values.append(fish.V_F[PLOT_ZONE])
    NH4_values.append(ammonia.NH4[PLOT_ZONE])
    NH4_all_zones.append(ammonia.NH4.copy())
    NO3_values.append(nitrate.NO3[PLOT_ZONE])
    NO3_all_zones.append(nitrate.NO3.copy())
    ON_values.append(organic_ammonia.ON[PLOT_ZONE])
    ON_all_zones.append(organic_ammonia.ON.copy())
    PO4_values.append(inorganic_phosphorus.PO4[PLOT_ZONE])
    PO4_all_zones.append(inorganic_phosphorus.PO4.copy())
    OP_values.append(organic_phosphorus.OP[PLOT_ZONE])
    OP_all_zones.append(organic_phosphorus.OP.copy())
    PP_values.append(particulate_phosphorus.PP[PLOT_ZONE])
    PP_all_zones.append(particulate_phosphorus.PP.copy())

    # 附加： 记录环境参数（仅记录选定区域）
    # T_values.append(external_data['T'][PLOT_ZONE])
    # I_values.append(external_data['I'][PLOT_ZONE])
    # NH4_values.append(external_data['NH4'][PLOT_ZONE])
    # NO3_values.append(external_data['NO3'][PLOT_ZONE])
    # ON_values.append(external_data['ON'][PLOT_ZONE])
    # PO4_values.append(external_data['PO4'][PLOT_ZONE])
    # DO_values.append(external_data['DO'][PLOT_ZONE])
    # H_values.append(new_H[PLOT_ZONE])

    # 打印调试信息
    # print(f"Timestep {t:03d} | Zone {PLOT_ZONE} | "
    #       f"PHY: {phy.PHY[PLOT_ZONE]:.4f} mgC/L | "
    #       f"Growth: {phy_growth_rate[PLOT_ZONE]:.4f} | "
    #       f"Loss: {phy_loss_rate[PLOT_ZONE]:.4f} | "
    #       f"ZOO: {zoo.ZOO[PLOT_ZONE]:.4f} mgC/L | "
    #       f"Grazing: {zoo_grazing_rate[PLOT_ZONE]:.4f} | "
    #       f"Growth: {zoo_growth_rate[PLOT_ZONE]:.4f} | "
    #       f"Loss: {zoo_loss_rate[PLOT_ZONE]:.4f} | "
    #       f"MA: {macro_phy.MA[PLOT_ZONE]:.4f} mgC/L | "
    #       # f"growth: {macro_phy_growth_rate[PLOT_ZONE]:.4f} | "
    #       # f"loss: {macro_phy_loss_rate[PLOT_ZONE]:.4f} | "
    #       # f"harvest: {harvest_rate[0]:.4f} | "
    #       f"N_SH: {shellfish.N_SH[PLOT_ZONE]:.4f} | "
    #       f"V_SH: {shellfish.V_SH[PLOT_ZONE]:.4f} | "
    #       # f"GRS_PHY: {shellfish_grs[PLOT_ZONE]:.4f} | "
    #       # f"V_SH_growth: {shellfish_V_growth[PLOT_ZONE]:.4f} | "
    #       # f"p_C_SH: {shellfish_p_c[PLOT_ZONE]:.4f} | "
    #       # f"p_M_SH: {shellfish_p_m[PLOT_ZONE]:.4f} | "
    #       f"N_F: {fish.N_F[PLOT_ZONE]:.4f} | "
    #       f"V_F: {fish.V_F[PLOT_ZONE]:.4f} | "
    #       f"NH4: {ammonia.NH4[PLOT_ZONE]:.4f} | "
    #       f"NO3: {nitrate.NO3[PLOT_ZONE]:.4f} | "
    #       f"ON: {organic_ammonia.ON[PLOT_ZONE]:.4f} | "
    #       f"PO4: {inorganic_phosphorus.PO4[PLOT_ZONE]:.4f} | "
    #       f"OP: {organic_phosphorus.OP[PLOT_ZONE]:.4f} | "
    #       )

np.save("./baseline_results/NH4_simulated_test.npy", np.array(NH4_all_zones))
np.save("./baseline_results/NO3_simulated_test.npy", np.array(NO3_all_zones))
np.save("./baseline_results/ON_simulated_test.npy", np.array(ON_all_zones))
np.save("./baseline_results/PO4_simulated_test.npy", np.array(PO4_all_zones))
np.save("./baseline_results/OP_simulated_test.npy", np.array(OP_all_zones))
np.save("./baseline_results/PP_simulated_test.npy", np.array(PP_all_zones))

# np.save("./sensitivity_results/NH4_atmosphere_minus.npy", np.array(NH4_all_zones))
# np.save("./sensitivity_results/NO3_atmosphere_minus.npy", np.array(NO3_all_zones))
# np.save("./sensitivity_results/ON_atmosphere_minus.npy", np.array(ON_all_zones))
# np.save("./sensitivity_results/PO4_atmosphere_minus.npy", np.array(PO4_all_zones))
# np.save("./sensitivity_results/OP_atmosphere_minus.npy", np.array(OP_all_zones))

out_rows = []
for nut, proc_dict in contributions_record.items():
    for proc, vec in proc_dict.items():
        row = {'Nutrient': nut, 'Process': proc}
        row.update({f'Area{i+1}': vec[i] for i in range(20)})
        out_rows.append(row)

df_contrib = pd.DataFrame(out_rows)
df_contrib.to_csv('cumulative_contributions_3y.csv', index=False)
print('✅ 已保存三年累计贡献 → cumulative_contributions_3y.csv')

rows = []
for nut in exported_mass:
    out_mg = exported_mass[nut]
    in_mg  = import_mass[nut]
    net_mg = out_mg - in_mg
    rows.append({
        'Nutrient': nut,
        'Exported_mass_mg': out_mg,
        'Imported_mass_mg': in_mg,
        'Net_export_mg'   : net_mg,
        'Exported_t'      : out_mg / 1e9,
        'Imported_t'      : in_mg  / 1e9,
        'Net_export_t'    : net_mg / 1e9
    })

export_df = pd.DataFrame(rows)
export_df.to_csv('net_export_to_outer_sea.csv', index=False)
print("✅ 已导出净流出外海质量 → net_export_to_outer_sea.csv")