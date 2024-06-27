# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import timedelta
from matplotlib.dates import MonthLocator, DateFormatter
from datetime import datetime
import os
from matplotlib.colors import to_rgba
from matplotlib.patches import Rectangle
# from main import nh,no,cp,cz,v_f,e_f,e_r_f,v_s,ca


#定义输出路径
output_folder = 'D:/yal/model_redesign2/output'

def date_from_start(start_year,start_mon,start_day,t):
    start_date=f'{start_year}-{start_mon}-{start_day}'
    end_date=pd.to_datetime(start_date)+timedelta(minutes=t)
    return end_date


def day_from_start(start_year,start_mon,start_day,end_year,end_mon,end_day):
    start_date=f'{start_year}-{start_mon}-{start_day}'
    end_date=f'{end_year}-{end_mon}-{end_day}'
    year_start_t=(pd.to_datetime(end_date) - pd.to_datetime(start_date)).total_seconds()/(3600*24)
    year_start_t=int(year_start_t)
    return year_start_t


#将输出结果按照天平均，data为数据，t_start、t_end为起止天数（以2016-1-1为起始），zone_num为海区号，r为浓度换算
def plt_data(data,t_start,t_end,zone_num,r):
    data_0 = pd.DataFrame(data)
    for t in range(0,10961):        
        data_0.loc[t,5]=date_from_start(2016,1,1,0)+pd.Timedelta(minutes=240*t)

    data_0.set_index(5, inplace=True)
    data_0_daily_average = data_0.resample('D').mean().reset_index()
    data_0_daily_average=data_0_daily_average.values
    x = data_0_daily_average[t_start:t_end, 0]
    y = data_0_daily_average[t_start:t_end, zone_num]/r
    return x,y

#常用颜色
rgb_green=(138/255,209/255,199/255)
rgb_green_2=(44/255,162/255,95/255)
rgb_blue=(69/255,117/255,177/255)
rgb_blue_2=(123/255,178/255,212/255)
rgb_red=(216/255,54/255,43/255)
rgb_red_2=(194/255,109/255,88/255)
rgb_purple=(122/255,94/255,166/255)
rgb_yellow=(254/255,238/255,168/255)
rgb_orange=(243/255,124/255,72/255)
rgb_grey=(199/255,197/255,210/255)

#计算x,y
x= plt_data(nh,10,1825,1,1000)[0]
y_nh= plt_data(nh,10,1825,1,1000)[1]
y_no= plt_data(no,10,1825,1,1000)[1]
y_cp= plt_data(cp,10,1825,1,1000)[1]
y_cha= plt_data(cp,10,1825,1,43.5)[1]


#养殖生长状态变量
start_fish=day_from_start(2016,1,1,2017,6,1)
end_fish=day_from_start(2016,1,1,2018,6,1)
x_f= plt_data(v_f,start_fish,end_fish,1,1)[0]
y_vf=plt_data(v_f,start_fish,end_fish,1,1)[1]
y_ef=plt_data(e_f,start_fish,end_fish,1,1)[1]
y_erf=plt_data(e_r_f,start_fish,end_fish,1,1)[1]

start_shellfish=day_from_start(2016,1,1,2017,6,30)
end_shellfish=day_from_start(2016,1,1,2017,12,31)
x_s= plt_data(v_s,start_shellfish,end_shellfish,1,1)[0]
y_vs=plt_data(v_s,start_shellfish,end_shellfish,1,1)[1]

y_ca= plt_data(ca,10,1825,1,1)[1]

# #养殖生长情况作图，V,E,Er
# plt.figure(figsize=(18,12))
# plt.subplot(3,1,1)
# plt.plot(x,y_vf,label='Zone1', marker='o',markersize=4,
#          linestyle='-',markerfacecolor='white',markeredgecolor=rgb_blue,
#          color='black',linewidth=1)
# plt.grid(which="major", axis='x', color='#DAD8D7', alpha=0.5, zorder=1)
# plt.grid(which="major", axis='y', color='#DAD8D7', alpha=0.5, zorder=1)
# plt.tick_params(axis='both', labelsize=18)
# plt.xlabel('Date', fontsize=18, labelpad=10) 
# plt.ylabel('V(cm3)', fontsize=18, labelpad=10) 

# plt.subplot(3,1,2)
# plt.plot(x,y_ef,label='Zone1', marker='o',markersize=4,
#          linestyle='-',markerfacecolor='white',markeredgecolor=rgb_blue,
#          color='black',linewidth=1)
# plt.grid(which="major", axis='x', color='#DAD8D7', alpha=0.5, zorder=1)
# plt.grid(which="major", axis='y', color='#DAD8D7', alpha=0.5, zorder=1)
# plt.tick_params(axis='both', labelsize=18)
# plt.xlabel('Date', fontsize=18, labelpad=10) 
# plt.ylabel('E(J)', fontsize=18, labelpad=10) 

# plt.subplot(3,1,3)
# plt.plot(x,y_erf,label='Zone1', marker='o',markersize=4,
#          linestyle='-',markerfacecolor='white',markeredgecolor=rgb_blue,
#          color='black',linewidth=1)
# plt.grid(which="major", axis='x', color='#DAD8D7', alpha=0.5, zorder=1)
# plt.grid(which="major", axis='y', color='#DAD8D7', alpha=0.5, zorder=1)
# plt.tick_params(axis='both', labelsize=18)
# plt.xlabel('Date', fontsize=18, labelpad=10) 
# plt.ylabel('Er(J)', fontsize=18, labelpad=10) 
# plt.legend()
# plt.tight_layout()
# plt.show()

#养殖生长情况作图，鱼类和贝类体积V
plt.figure(figsize=(14,6))
plt.rcParams['font.family']='serif'
font_size=14
plt.subplot(1,2,1)
plt.plot(x_f,y_vf,label='Fish', marker='o',markersize=4,
         linestyle='-',markerfacecolor='white',markeredgecolor=rgb_blue,
         color='black',linewidth=1)
plt.grid(which="major", axis='x', color='#DAD8D7', alpha=0.5, zorder=1)
plt.grid(which="major", axis='y', color='#DAD8D7', alpha=0.5, zorder=1)
plt.tick_params(axis='both', labelsize=font_size)
plt.xlabel('Month', fontsize=font_size, labelpad=10) 
plt.ylabel('V (cm$^3$)', fontsize=font_size, labelpad=10) 
plt.legend(frameon=False,handlelength=0,fontsize=font_size)
plt.gca().xaxis.set_major_locator(MonthLocator())
plt.gca().xaxis.set_major_formatter(DateFormatter('%b'))  # '%b'表示月份的简写形式，例如J、F、M、A等

plt.subplot(1,2,2)
plt.plot(x_s,y_vs,label='Shellfish', marker='o',markersize=4,
         linestyle='-',markerfacecolor='white',markeredgecolor=rgb_blue,
         color='black',linewidth=1)
plt.grid(which="major", axis='x', color='#DAD8D7', alpha=0.5, zorder=1)
plt.grid(which="major", axis='y', color='#DAD8D7', alpha=0.5, zorder=1)
plt.tick_params(axis='both', labelsize=font_size)
plt.xlabel('Month', fontsize=font_size, labelpad=10) 
plt.ylabel('V (cm$^3$)', fontsize=font_size, labelpad=10) #_x下标，^{x}上标
plt.legend(frameon=False,handlelength=0,fontsize=font_size)
plt.gca().xaxis.set_major_locator(MonthLocator())
plt.gca().xaxis.set_major_formatter(DateFormatter('%b'))  # '%b'表示月份的简写形式，例如J、F、M、A等
plt.tight_layout()
note="v_mariculture"
plt.savefig(os.path.join(output_folder,f'output_{note}.png'),dpi=300)
plt.show()



#养殖藻类碳含量变化
start_seaweed=day_from_start(2016,1,1,2016,1,1)
end_seaweed=day_from_start(2016,1,1,2016,6,30)
x_a= plt_data(ca,start_seaweed,end_seaweed,1,1)[0]
y_ca=plt_data(ca,start_seaweed,end_seaweed,1,1)[1]

plt.figure(figsize=(10,5))
plt.rcParams['font.family']='serif'
font_size=14
plt.plot(x_a,y_ca,label='Zone1', marker='o',markersize=5,
         linestyle='-',markerfacecolor='white',markeredgecolor=rgb_green_2,
         color='black',linewidth=1)
plt.grid(which="major", axis='x', color='#DAD8D7', alpha=0.5, zorder=1)
plt.grid(which="major", axis='y', color='#DAD8D7', alpha=0.5, zorder=1)
plt.tick_params(axis='both', labelsize=font_size)
plt.xlabel('Month', fontsize=font_size, labelpad=10) 
plt.ylabel('Seaweed (mg C/m3)', fontsize=font_size, labelpad=10) 
plt.gca().xaxis.set_major_locator(MonthLocator())
plt.gca().xaxis.set_major_formatter(DateFormatter('%b'))  # '%b'表示月份的简写形式，例如J、F、M、A等
plt.tight_layout()
# plt.savefig(os.path.join(output_folder,'output_ca.png'),dpi=300)
plt.show()


#叶绿素
plt.figure(figsize=(10,5))
plt.rcParams['font.family']='serif'
font_size=14
plt.plot(x,y_cha,label='Zone1', marker='o',markersize=5,
         linestyle='-',markerfacecolor='white',markeredgecolor=rgb_green_2,
         color='black',linewidth=1)
plt.grid(which="major", axis='x', color='#DAD8D7', alpha=0.5, zorder=1)
plt.grid(which="major", axis='y', color='#DAD8D7', alpha=0.5, zorder=1)
plt.tick_params(axis='both', labelsize=font_size)
plt.xlabel('Date', fontsize=font_size, labelpad=10) 
plt.ylabel('Chlorophyll a (μg/L)', fontsize=font_size, labelpad=10) 
plt.tight_layout()
plt.savefig(os.path.join(output_folder,'output_cha.png'),dpi=300)
plt.show()




#作图 nh no cha
x= plt_data(nh,10,1825,2,1000)[0]
y_nh= plt_data(nh,10,1825,2,1000)[1]
y_no= plt_data(no,10,1825,2,1000)[1]
y_cha= plt_data(cp,10,1825,2,43.5)[1]


plt.figure(figsize=(12,9))
plt.rcParams['font.family']='serif'
font_size=12
plt.subplot(3,1,1)
plt.plot(x,y_nh,label='Zone1', marker='o',markersize=4,
         linestyle='-',markerfacecolor='white',markeredgecolor=rgb_blue,
         color='black',linewidth=1)
plt.grid(which="major", axis='x', color='#DAD8D7', alpha=0.5, zorder=1)
plt.grid(which="major", axis='y', color='#DAD8D7', alpha=0.5, zorder=1)
plt.tick_params(axis='both', labelsize=font_size)
plt.xlabel('Date', fontsize=font_size, labelpad=10) 
plt.ylabel('NH$_4^{-}$ (mg/L)', fontsize=font_size, labelpad=10) 


plt.subplot(3,1,2)
plt.plot(x,y_no,label='Zone1', marker='o',markersize=4,
         linestyle='-',markerfacecolor='white',markeredgecolor=rgb_orange,
         color='black',linewidth=1)
plt.grid(which="major", axis='x', color='#DAD8D7', alpha=0.5, zorder=1)
plt.grid(which="major", axis='y', color='#DAD8D7', alpha=0.5, zorder=1)
plt.tick_params(axis='both', labelsize=font_size)
plt.xlabel('Date', fontsize=font_size, labelpad=10) 
plt.ylabel('NO$_3^{-}$ (mg/L)', fontsize=font_size, labelpad=10) 


plt.subplot(3,1,3)
plt.plot(x,y_cha,label='Zone1', marker='o',markersize=4,
         linestyle='-',markerfacecolor='white',markeredgecolor=rgb_green_2,
         color='black',linewidth=1)
plt.grid(which="major", axis='x', color='#DAD8D7', alpha=0.5, zorder=1)
plt.grid(which="major", axis='y', color='#DAD8D7', alpha=0.5, zorder=1)
plt.tick_params(axis='both', labelsize=font_size)
plt.xlabel('Date', fontsize=font_size, labelpad=10) 
plt.ylabel('Chlorophyll a (μg/L)', fontsize=font_size, labelpad=10) 
# plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(output_folder,'output_Zone2.png'),dpi=300)
plt.show()



# # 年际季节变化柱状图，5，8，10月
# plt.figure(figsize=(10, 6))
# colors = rgb_green_2,rgb_red,rgb_blue
# bar_width = 0.7
# # 循环遍历每年
# # plt.grid(which="major", axis='x', color='#DAD8D7', alpha=0.5, zorder=1)
# # plt.grid(which="major", axis='y', color='#DAD8D7', alpha=0.5, zorder=1)
# for year in range(2016, 2021):
#     selected_data1 = nh[int(day_from_start(2016,1,1,year,4,20))*6:int(day_from_start(2016,1,1,year,5,10))*6,:]/1000
#     selected_data2 = nh[int(day_from_start(2016,1,1,year,7,20))*6:int(day_from_start(2016,1,1,year,8,10))*6,:]/1000
#     selected_data3 = nh[int(day_from_start(2016,1,1,year,10,20))*6:int(day_from_start(2016,1,1,year,11,10))*6,:]/1000
#     # 计算每个时间段的平均值和标准差
#     mean_value1, std_dev1 = np.mean(selected_data1, axis=0), np.std(selected_data1, axis=0)
#     mean_value2, std_dev2 = np.mean(selected_data2, axis=0), np.std(selected_data2, axis=0)
#     mean_value3, std_dev3 = np.mean(selected_data3, axis=0), np.std(selected_data3, axis=0)
    
#     positions = np.array([f'{year}-05', f'{year}-08', f'{year}-11'])
#     positions_numeric = np.arange(len(positions)) + year * (3 + bar_width)

#     # 绘制柱状图
#     plt.bar(positions_numeric,
#             [mean_value1[1], mean_value2[1],mean_value3[1]],
#             yerr=[std_dev1[1], std_dev2[1],std_dev3[1]],
#             capsize=5,
#             width=bar_width,
#             alpha=0.6,
#             color=[to_rgba(color, alpha=0.1) for color in colors],
#             edgecolor= colors,
#             ecolor='gray',
#             label=str(year)) 

# # 创建虚拟图例
# legend_handles=([Rectangle((0, 0), 1, 1, color=color) for color in colors])
# plt.legend(legend_handles, ['May', 'Aug', 'Nov'], loc='upper right',
#            frameon=False,fontsize=font_size) 
# plt.tick_params(axis='both', labelsize=font_size)
# plt.xlabel('Date', fontsize=font_size, labelpad=10) 
# plt.ylabel('NH$_4^{-}$ (mg/L)', fontsize=font_size, labelpad=10) 
# plt.xticks(np.arange(2016, 2021) * (3 + bar_width) + 1, [str(year) for year in range(2016, 2021)])
# plt.tight_layout()


#年际季节变化柱状图，2，5，8，10月
def plt_time_series(df,zone,ylabel):
    data0 = pd.DataFrame(df)
    for t in range(0,10961):        
        data0.loc[t,5]=date_from_start(2016,1,1,0)+pd.Timedelta(minutes=240*t)
    data0.set_index(5, inplace=True)
    data_daily_average = data0.resample('D').mean().reset_index()
    data_daily_average=data_daily_average.values
    data =data_daily_average[:,1:6]
    data=data.astype(np.float64)
    plt.figure(figsize=(10, 6))
    colors =rgb_orange,rgb_green_2,rgb_red,rgb_blue
    bar_width = 0.7
    for year in range(2016, 2021):
        selected_data1 = data[int(day_from_start(2016,1,1,year,1,20)):int(day_from_start(2016,1,1,year,2,10)),:]/1000
        selected_data2 = data[int(day_from_start(2016,1,1,year,4,20)):int(day_from_start(2016,1,1,year,5,10)),:]/1000
        selected_data3 = data[int(day_from_start(2016,1,1,year,7,20)):int(day_from_start(2016,1,1,year,8,10)),:]/1000
        selected_data4 = data[int(day_from_start(2016,1,1,year,10,20)):int(day_from_start(2016,1,1,year,11,10)),:]/1000
        # 计算每个时间段的平均值和标准差
        mean_value1, std_dev1 = np.mean(selected_data1, axis=0), np.std(selected_data1, axis=0)
        mean_value2, std_dev2 = np.mean(selected_data2, axis=0), np.std(selected_data2, axis=0)
        mean_value3, std_dev3 = np.mean(selected_data3, axis=0), np.std(selected_data3, axis=0)
        mean_value4, std_dev4 = np.mean(selected_data4, axis=0), np.std(selected_data4, axis=0)
        
        positions = np.array([f'{year}-02',f'{year}-05', f'{year}-08', f'{year}-11'])
        positions_numeric = np.arange(len(positions)) + year * (4 + bar_width)
    
        # 绘制柱状图
        plt.bar(positions_numeric,
                [mean_value1[zone], mean_value2[zone],mean_value3[zone],mean_value4[zone]],
                yerr=[std_dev1[zone], std_dev2[zone],std_dev3[zone],std_dev4[zone]],
                capsize=5,
                width=bar_width,
                alpha=0.6,
                color=[to_rgba(color, alpha=0.8) for color in colors],
                edgecolor= colors,
                ecolor='gray',
                label=str(year)) 
        
    # 创建虚拟图例
    legend_handles=([Rectangle((0, 0), 1, 1, color=color) for color in colors])
    plt.legend(legend_handles, ['Feb','May', 'Aug', 'Nov'], loc='upper right',
               bbox_to_anchor=(1, 1),frameon=False,fontsize=font_size) 
    plt.tick_params(axis='both', labelsize=font_size)
    plt.xlabel('Date', fontsize=font_size, labelpad=10) 
    plt.ylabel(f'{ylabel}', fontsize=font_size, labelpad=10) 
    plt.tight_layout()
    plt.xticks(np.arange(2016, 2021) * (4 + bar_width) + 1.5, [str(year) for year in range(2016, 2021)])
    plt.savefig(os.path.join(output_folder,f'output_Zone{zone}_nh.png'),dpi=300)
   


plt_time_series(nh,2,"NH$_4^{-}$ (mg/L)")
plt_time_series(no,2,"NO$_3^{-}$ (mg/L)")


#实际监测数据
data_real=pd.read_csv(r"original_data/real_data_1227_1.csv")
data_real =data_real[data_real["year"]!=2015]
# data_real=data_real[data_real["from"]=='haiyang']
data_real["day"] =1
data_real["date_new"] = pd.to_datetime(data_real[['year','month','day']])
data_real1 = data_real[["date_new",'zone_new','no','nh']]
data_real1.loc[data_real1['nh'] > 0.3, 'nh'] *= 0.1
        
font_size=14


#模拟值和监测值对比，2016-2018年
def plt_real(df,tp,zone,ylabel):
    # df=no;tp='no';zone=1;ylabel="NO$_3^{-}$ (mg/L)"
    data0 = pd.DataFrame(df)
    for t in range(0,10961):        
        data0.loc[t,5]=date_from_start(2016,1,1,0)+pd.Timedelta(minutes=240*t)
    data0.set_index(5, inplace=True)
    data_daily_average = data0.resample('D').mean().reset_index()
    data_daily_average=data_daily_average.values
    data =data_daily_average[:,1:6]
    data=data.astype(np.float64)
    colors =rgb_orange,rgb_green_2,rgb_red,rgb_blue
    bar_width = 0.7
    
    data1=data_real1[data_real1['zone_new'] == zone]
    agg_df = data1.groupby("date_new")[f'{tp}'].agg(['mean', 'std']).reset_index()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    for year in range(2016, 2019):
        selected_data1 = data[int(day_from_start(2016,1,1,year,1,20)):int(day_from_start(2016,1,1,year,2,10)),:]/1000
        selected_data2 = data[int(day_from_start(2016,1,1,year,4,20)):int(day_from_start(2016,1,1,year,5,10)),:]/1000
        selected_data3 = data[int(day_from_start(2016,1,1,year,7,20)):int(day_from_start(2016,1,1,year,8,10)),:]/1000
        selected_data4 = data[int(day_from_start(2016,1,1,year,10,20)):int(day_from_start(2016,1,1,year,11,10)),:]/1000
        # 计算每个时间段的平均值和标准差
        mean_value1, std_dev1 = np.mean(selected_data1, axis=0), np.std(selected_data1, axis=0)
        mean_value2, std_dev2 = np.mean(selected_data2, axis=0), np.std(selected_data2, axis=0)
        mean_value3, std_dev3 = np.mean(selected_data3, axis=0), np.std(selected_data3, axis=0)
        mean_value4, std_dev4 = np.mean(selected_data4, axis=0), np.std(selected_data4, axis=0)
        
        positions = np.array([f'{year}-02',f'{year}-05', f'{year}-08', f'{year}-11'])
        positions_numeric = np.arange(len(positions)) + year * (4 + bar_width)
    
        mean_value_real=agg_df.loc[agg_df['date_new'].dt.year == year, 'mean'].values
        std_dev_real=agg_df.loc[agg_df['date_new'].dt.year == year, 'std'].values
        
        # 绘制柱状图
        ax.bar(positions_numeric,
                [mean_value1[zone], mean_value2[zone],mean_value3[zone],mean_value4[zone]],
                yerr=[std_dev1[zone], std_dev2[zone],std_dev3[zone],std_dev4[zone]],
                capsize=5,
                width=bar_width,
                alpha=0.6,
                color=[to_rgba(color, alpha=0.8) for color in colors],
                edgecolor= colors,
                ecolor='gray',
                label=str(year)) 
        ax.errorbar(positions_numeric,
                   mean_value_real,
                   yerr=std_dev_real,
                   fmt='o',                   
                   color='black',
                   label=str(year)) 
        
    # 创建虚拟图例
    legend_handles=([Rectangle((0, 0), 1, 1, color=color) for color in colors])
    ax.legend(legend_handles, ['Feb','May', 'Aug', 'Nov'], loc='upper right',
               frameon=False,fontsize=font_size) 
    ax.tick_params(axis='both', labelsize=font_size)
    ax.set_xlabel(f'Zone{zone}', fontsize=font_size, labelpad=10) 
    ax.set_ylabel(f'{ylabel}', fontsize=font_size, labelpad=10) 
    ax.set_xticks(np.arange(2016, 2019) * (4 + bar_width) + 1.5, [str(year) for year in range(2016, 2019)])
    plt.tight_layout()
    # plt.savefig(os.path.join(output_folder,f'output_Zone{zone}_{tp}.png'),dpi=300)


#输出    
for i in range(1,5):
    plt_real(no,'no',i,"NO$_3^{-}$ (mg/L)")

for i in range(1,5):
    plt_real(nh,'nh',i,"NH$_4^{-}$ (mg/L)")
    
    