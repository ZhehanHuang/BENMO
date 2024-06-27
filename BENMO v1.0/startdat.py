# subroutine startdat

# ~ ~ ~ PURPOSE ~ ~ ~
# this subroutine define the start data for the model

# ~ ~ ~ INCOMING VARIABLES ~ ~ ~
# name        |units         |definition
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# temp_data   |NA            |original data from csv file (envi_T_min.csv)
# years       |none          |years of the model
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

# ~ ~ ~ OUTGOING VARIABLES ~ ~ ~
# name        |units         |definition
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# v_s         |cm^3          |[shellfish] Biovolume growth
# e_s         |J             |[shellfish] Reserves
# e_r_s       |J             |[shellfish] Reproductive reserves
# v_f         |cm^3          |[fish] Biovolume growth
# e_f         |J             |[fish] Reserves
# e_r_f       |J             |[fish] Reproductive reserves
# son         |mg N/m^2      |[env] Sediment organic nitrogen
# soc         |mg C/m^2      |[env] Sediment organic carbon
# pon         |mg N/m^3      |[env] Pelagic non-plankton organic nitrogen
# poc         |mg C/m^3      |[env] Pelagic non-plankton organic carbon
# nh          |mg N/m^3      |[env] Ammonium nitrogen
# no          |mg N/m^3      |[env] Nitrate nitrogen
# don         |mg N/m^3      |[env] Dissolved organic nitrogen
# cp          |mg C/m^3      |[phyto] Phytoplankton carbon
# nph         |mg N/m^3      |[phyto] Phytoplankton nitrogen
# cz          |mg C/m^3      |[zoo] Zooplankton structure weight
# ez          |mg C/m^3      |[zoo] Zooplankton reserves
# st_seaweed  |NA            |[seaweed] reclassefied start data for seaweed
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ 

# ~ ~ ~ LOCAL DEFINITIONS ~ ~ ~
# name        |units         |definition
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~

# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ 

# ~ ~ ~ SUBROUTINES/FUNCTIONS CALLED ~ ~ ~
import numpy as np
import pandas as pd
import readcsv as rd
# ~ ~ ~ END SPECIFICATIONS ~ ~ ~

'''
Define start data
'''
# Shellfish
v_s = 0.6*np.ones(5)
e_s = 40*np.ones(5)
e_r_s = 10*np.ones(5)

# Fish
v_f = 5*np.ones(5)
e_f = 5*8500*np.ones(5)
e_r_f = 6000*np.ones(5)

# Seaweed
st_seaweed = {}
years = rd.seaweed_data['Year'].unique()
areas = rd.seaweed_data['Region'].unique()

for col in rd.seaweed_data.columns[1:3]:
    type_df = pd.DataFrame(index=years, columns=areas)  
    for year in years:
        for area in areas:
            quantity = rd.seaweed_data[(rd.seaweed_data['Year'] == year)\
                            & (rd.seaweed_data['Region'] == area)][col].values
            type_df.loc[year, area] = quantity[0] if len(quantity) > 0 else 0
    st_seaweed[col] = type_df

# Nitrogen
pon = 10*np.ones(5)
son = 10*np.ones(5)
soc = 10*np.ones(5)
poc = 10*np.ones(5)
nh = rd.start_n.loc["nh/mg/L"]*1000
no = rd.start_n.loc["no/mg/L"]*1000
don = rd.start_n.loc["don/mg/L"]*1000

# Phytoplankton
cp = 1*0.0435*1000*np.ones(5)
nph = 1*0.0435*0.16*1000*np.ones(5)

# Zooplankton
cz = 0.5*np.ones(5)
ez = 0.5*np.ones(5)

# Environment
r_river=1
r_point=1
r_pond=1