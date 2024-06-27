from datetime import timedelta
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
#from main import nh, no


output_folder = 'D:/yal/model_redesign2/output'


def date_from_start(start_year,start_mon,start_day,t):
    start_date=f'{start_year}-{start_mon}-{start_day}'
    end_date=pd.to_datetime(start_date)+timedelta(minutes=t)
    return end_date
# data_nh = np.genfromtxt('G:/py_all/nutrient model/4/5year_new/result/result_nh.csv', delimiter=',',skip_header=1)
start=10
end=1825
tp="no3"
# 提取x轴数据（第一列）
data_nh = pd.DataFrame(no)
for t in range(0,10961):        
    data_nh.loc[t,5]=date_from_start(2016,1,1,0)+pd.Timedelta(minutes=240*t)

data_nh.set_index(5, inplace=True)
data_nh_daily_average = data_nh.resample('D').mean().reset_index()

data_nh_daily_average=data_nh_daily_average.values

x = data_nh_daily_average[start:end, 0]

# 提取y轴数据（第2到5列）
y1_nh = data_nh_daily_average[start:end, 1]/1000
y2_nh = data_nh_daily_average[start:end, 2]/1000
y3_nh = data_nh_daily_average[start:end, 3]/1000
y4_nh = data_nh_daily_average[start:end, 4]/1000
y5_nh = data_nh_daily_average[start:end, 5]/1000
# y6 = data[:, 6]/1000
# y7 = data[:, 7]/1000
# y8 = data[:, 8]/1000
# y9 = data[:, 9]/1000
# y10 = data[:, 10]/1000
# y11 = data[:, 11]/1000

#创建多子图

fig,axes=plt.subplots(nrows=5,ncols=1,sharex=True,sharey=True,figsize=(8,10))
rgb_green=(138/255,209/255,199/255)
rgb_blue=(69/255,117/255,177/255)
rgb_blue_2=(123/255,178/255,212/255)
rgb_red=(216/255,54/255,43/255)
rgb_red_2=(194/255,109/255,88/255)
rgb_purple=(122/255,94/255,166/255)
rgb_yellow=(254/255,238/255,168/255)
rgb_orange=(243/255,124/255,72/255)
rgb_grey=(199/255,197/255,210/255)
rgb=rgb_blue
y_max=10
# label_text='$Phytoplankton nitrogen (mgN m^(−3))$'
# label_text='Phyto nitrogen (mgN/L)'
label_text='NO3-N (mg/L)'

# for i in range(0,5,1):  
#     axes[i].axvspan(1,366,color=rgb_yellow,alpha=0.2)
#     axes[i].axvspan(366,366+365,color=rgb_green,alpha=0.2)
#     axes[i].axvspan(366+365,366+365*2,color=rgb_grey,alpha=0.2)

for i in range(0,5,1):  
    axes[i].axvspan(pd.Timestamp("2016-1-1"),pd.Timestamp("2017-1-1"),color=rgb_yellow,alpha=0.2)
    axes[i].axvspan(pd.Timestamp("2017-1-1"),pd.Timestamp("2018-1-1"),color=rgb_green,alpha=0.2)
    axes[i].axvspan(pd.Timestamp("2018-1-1"),pd.Timestamp("2019-1-1"),color=rgb_grey,alpha=0.2) 
    axes[i].axvspan(pd.Timestamp("2019-1-1"),pd.Timestamp("2020-1-1"),color=rgb_orange,alpha=0.2)
    axes[i].axvspan(pd.Timestamp("2020-1-1"),pd.Timestamp("2020-12-31"),color=rgb_purple,alpha=0.2)
    
axes[0].scatter(x,np.clip(y1_nh,0,y_max),label='Zone1', marker='o',color=rgb,s=3,alpha=1)
# axes[0].set_title('Area1')
axes[1].scatter(x,np.clip(y2_nh,0,y_max),label='Zone2', marker='o',color=rgb,s=3,alpha=1)
axes[2].scatter(x,np.clip(y3_nh,0,y_max),label='Zone3', marker='o',color=rgb,s=3,alpha=1)
axes[3].scatter(x,np.clip(y4_nh,0,y_max),label='Zone4', marker='o',color=rgb,s=3,alpha=1)
axes[4].scatter(x,np.clip(y5_nh,0,y_max),label='Zone5', marker='o',color=rgb,s=3,alpha=1)
plt.legend(frameon=False)
real_data=pd.read_csv(r'.\original_data\real_5year_3.csv')
real_data["time"]=pd.to_datetime(real_data["time"])
real_data_1 = real_data.groupby(['num_new', "time"])[tp].min().reset_index()
real_data_1['year']=real_data_1["time"].dt.year
real_data_1['month']=real_data_1["time"].dt.month
real_data_1['day']=real_data_1["time"].dt.day
# real_data_1 = real_data.groupby(['num_new', "time"])['nh4'].min().reset_index()
# real_data_1=real_data_1.loc[real_data_1["year"]<2019].reset_index(drop=True)

# for i in range(0,5,1):  
#     axes[i].scatter(real_data_1.loc[real_data_1["num_new"]==i+1,"time"],real_data_1.loc[real_data_1["num_new"]==i+1,tp], marker='o',color=rgb_red,s=8,alpha=1)

for i in range(0,5,1):
    axes[i].set_ylabel(label_text,fontsize=10)
    axes[i].legend(loc='upper left')
    # axes.set_yticks(np.arange(0,0.06,0.01))

axes[4].set_xlabel('Date')
plt.savefig(os.path.join(output_folder,f'output_{tp}.png'),dpi=1000)
plt.tight_layout()
plt.show()

start=10
end=1825
tp="nh4"
# 提取x轴数据（第一列）
data_nh = pd.DataFrame(nh)
for t in range(0,10961):        
    data_nh.loc[t,5]=date_from_start(2016,1,1,0)+pd.Timedelta(minutes=240*t)

data_nh.set_index(5, inplace=True)
data_nh_daily_average = data_nh.resample('D').mean().reset_index()

data_nh_daily_average=data_nh_daily_average.values

x = data_nh_daily_average[start:end, 0]

# 提取y轴数据（第2到5列）
y1_nh = data_nh_daily_average[start:end, 1]/1000
y2_nh = data_nh_daily_average[start:end, 2]/1000
y3_nh = data_nh_daily_average[start:end, 3]/1000
y4_nh = data_nh_daily_average[start:end, 4]/1000
y5_nh = data_nh_daily_average[start:end,5]/1000
# y6 = data[:, 6]/1000
# y7 = data[:, 7]/1000
# y8 = data[:, 8]/1000
# y9 = data[:, 9]/1000
# y10 = data[:, 10]/1000
# y11 = data[:, 11]/1000

#创建多子图

fig,axes=plt.subplots(nrows=5,ncols=1,sharex=True,sharey=True,figsize=(8,10))
rgb_green=(138/255,209/255,199/255)
rgb_blue=(69/255,117/255,177/255)
rgb_blue_2=(123/255,178/255,212/255)
rgb_red=(216/255,54/255,43/255)
rgb_red_2=(194/255,109/255,88/255)
rgb_purple=(122/255,94/255,166/255)
rgb_yellow=(254/255,238/255,168/255)
rgb_orange=(243/255,124/255,72/255)
rgb_grey=(199/255,197/255,210/255)
rgb=rgb_blue
y_max=10
# label_text='$Phytoplankton nitrogen (mgN m^(−3))$'
# label_text='Phyto nitrogen (mgN/L)'
label_text='NH4-N (mg/L)'

# for i in range(0,5,1):  
#     axes[i].axvspan(1,366,color=rgb_yellow,alpha=0.2)
#     axes[i].axvspan(366,366+365,color=rgb_green,alpha=0.2)
#     axes[i].axvspan(366+365,366+365*2,color=rgb_grey,alpha=0.2)

for i in range(0,5,1):  
    axes[i].axvspan(pd.Timestamp("2016-1-1"),pd.Timestamp("2017-1-1"),color=rgb_yellow,alpha=0.2)
    axes[i].axvspan(pd.Timestamp("2017-1-1"),pd.Timestamp("2018-1-1"),color=rgb_green,alpha=0.2)
    axes[i].axvspan(pd.Timestamp("2018-1-1"),pd.Timestamp("2019-1-1"),color=rgb_grey,alpha=0.2) 
    axes[i].axvspan(pd.Timestamp("2019-1-1"),pd.Timestamp("2020-1-1"),color=rgb_orange,alpha=0.2)
    axes[i].axvspan(pd.Timestamp("2020-1-1"),pd.Timestamp("2020-12-31"),color=rgb_purple,alpha=0.2)
    
axes[0].scatter(x,np.clip(y1_nh,0,y_max),label='Zone1', marker='o',color=rgb,s=3,alpha=1)
# axes[0].set_title('Area1')
axes[1].scatter(x,np.clip(y2_nh,0,y_max),label='Zone2', marker='o',color=rgb,s=3,alpha=1)
axes[2].scatter(x,np.clip(y3_nh,0,y_max),label='Zone3', marker='o',color=rgb,s=3,alpha=1)
axes[3].scatter(x,np.clip(y4_nh,0,y_max),label='Zone4', marker='o',color=rgb,s=3,alpha=1)
axes[4].scatter(x,np.clip(y5_nh,0,y_max),label='Zone5', marker='o',color=rgb,s=3,alpha=1)

real_data=pd.read_csv(r'.\original_data\real_5year_3.csv')
real_data["time"]=pd.to_datetime(real_data["time"])
real_data_1 = real_data.groupby(['num_new', "time"])[tp].min().reset_index()
real_data_1['year']=real_data_1["time"].dt.year
real_data_1['month']=real_data_1["time"].dt.month
real_data_1['day']=real_data_1["time"].dt.day
# real_data_1 = real_data.groupby(['num_new', "time"])['nh4'].min().reset_index()
# real_data_1=real_data_1.loc[real_data_1["year"]<2019].reset_index(drop=True)

# for i in range(0,5,1):  
#     axes[i].scatter(real_data_1.loc[real_data_1["num_new"]==i+1,"time"],real_data_1.loc[real_data_1["num_new"]==i+1,tp], marker='o',color=rgb_red,s=8,alpha=1)

for i in range(0,5,1):
    axes[i].set_ylabel(label_text,fontsize=10)
    axes[i].legend(loc='upper left')
    # axes.set_yticks(np.arange(0,0.06,0.01))

axes[4].set_xlabel('Date')
plt.savefig(os.path.join(output_folder,f'output_{tp}.png'),dpi=1000)
plt.tight_layout()
plt.show()