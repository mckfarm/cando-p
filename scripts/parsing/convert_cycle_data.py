# -*- coding: utf-8 -*-
"""
converting data from excel to csv for import into R
"""

import pandas as pd
import os
import glob

# %% in-cycle sampling
file_path = r"C:\Users\mckyf\Northwestern University\Wells Research Group - CANDO+P and N2O\CANDO+P Reactor\Operation and Logs\Performance logs"
os.chdir(file_path)

data_2021 = "cycle_results_2021.xlsx"
data_2022 = "cycle_results_2022.xlsx"

df_21 = pd.read_excel(data_2021, sheet_name=None)
df_21 = pd.concat(df_21,ignore_index=True)

df_22 = pd.read_excel(data_2022, sheet_name=None)
df_22 = pd.concat(df_22,ignore_index=True)

# phosphate, ammonia, nox, nitrite, nitrate, acetate
df_all = pd.concat([df_21,df_22],ignore_index=True)

columns_to_keep = ['date_time', 'phase', 'NO2+NO3_mgNL',
       'NO2_mgNL', 'NH3_mgNL', 'OP_mgPL', 'NO3_mgNL', 'Ace_mgCODL']

column_names = ["date_time","phase","nox","nitrite","ammonia","phosphate","nitrate","acetate"]

df_all = df_all[columns_to_keep]
df_all.columns = column_names

df_all["date_time"] = pd.to_datetime(df_all["date_time"], format="%Y-%m-%d %h:%m:%s")

# final export
df_all.to_csv("all_cycle_data.csv",index=False)


# %% cod and nutrients
data_daily = "performance_data_raw.xlsx"

df_nutrients = pd.read_excel(data_daily, sheet_name="Nutrients_skalar")
df_nutrients["date_time"] = pd.to_datetime(df_nutrients["date_time"], format="%Y-%m-%d %h:%m:%s")
df_nutrients.to_csv("all_nutrient_daily_data.csv",index=False)

df_cod = pd.read_excel(data_daily, sheet_name="COD")
df_cod["date_time"] = pd.to_datetime(df_cod["date_time"], format="%Y-%m-%d %h:%m:%s")
df_cod.to_csv("all_cod_daily_data.csv",index=False)

# %% solids
data_daily = "solids_data.xlsx"

df_nutrients = pd.read_excel(data_daily, sheet_name="solids")
df_nutrients["date_time"] = pd.to_datetime(df_nutrients["date_time"], format="%Y-%m-%d %h:%m:%s")
df_nutrients.to_csv("all_solids.csv",index=False)

# %% n2o sensors
file_path = r"C:\Users\mckyf\Northwestern University\Wells Research Group - CANDO+P and N2O\CANDO+P Reactor\Operation and Logs\Sensor logs\Unisense"
os.chdir(file_path)

data_n2o = pd.DataFrame()
for f in glob.glob("*.xlsx"):
    df = pd.read_excel(f)
    data_n2o = data_n2o.append(df,ignore_index=True)

columns_n2o_tokeep = ["date_time","N2O_mgNL_raw","temp"]
data_n2o = data_n2o[columns_n2o_tokeep]
data_n2o.columns = ["date_time","n2o","temp"]
# data_n2o_2021 = data_n2o[data_n2o["date_time"].dt.year == 2021]
data_n2o_2022 = data_n2o[data_n2o["date_time"].dt.year == 2022]

# data_n2o_2021.to_csv("all_n2o_2021.csv",index=False)
data_n2o_2022.to_csv("all_n2o_2022.csv",index=False)

del data_n2o
# del data_n2o_2021
del data_n2o_2022
del df

# %% hach sensors
file_path = r"C:\Users\mckyf\Northwestern University\Wells Research Group - CANDO+P and N2O\CANDO+P Reactor\Operation and Logs\Sensor logs\Hach"
os.chdir(file_path)

data_hach = pd.DataFrame()
for f in glob.glob("*.csv"):
    df = pd.read_csv(f)
    data_hach = data_hach.append(df,ignore_index=True)

columns_hach_tokeep = ["date_time","do_ppm","temp_c","orp","ph","temp"]
data_hach = data_hach[columns_hach_tokeep]
data_hach.columns = ["date_time","do","temp_sc1000","orp","ph","temp_sc200"]
data_hach.to_csv("all_hach.csv",index=False)
