# subroutine readall

# ~ ~ ~ PURPOSE ~ ~ ~
# this subroutine reads the parameters for all species from the corresponding 
# csv file (bio_coe.csv) and rename them into the form required by the model

# ~ ~ ~ INCOMING VARIABLES ~ ~ ~
# name        |units         |definition
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# bio_data    |NA            |original data from csv file (bio_coe.csv)
# d_to_min    |min/d         |number of minutes in a day
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ 

# ~ ~ ~ OUTGOING VARIABLES ~ ~ ~
# name        |units         |definition
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
# p           |g wet W/cm^3  |[all] Biovolume density of cultured animals
# u_cj        |J/mg C        |[all] Ratio of carbon to energy content
# s_r         |1/min         |[all] Natural mortality of shellfish/seaweed
# s_h         |1/min         |[all] Harvest mortality of shellfish/seaweed
# ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ 

# ~ ~ ~ SUBROUTINES/FUNCTIONS CALLED ~ ~ ~
import readcsv as rd
# ~ ~ ~ END SPECIFICATIONS ~ ~ ~
    
'''
Parameters for all species
'''
p = rd.bio_data[0]
u_cj = rd.bio_data[1]
s_r = rd.bio_data[2]/rd.d_to_min
s_h = rd.bio_data[3]/rd.d_to_min
