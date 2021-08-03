'''
Project: CANDO+P
Purpose: parsing through Unisense log files
Output: csvs of N2O log
'''

# %% set up
import os
import numpy as np
import struct

file_path = "C:/Users/mckyf/Box/CANDO+P and N2O/CANDO+P Reactor 2021/Operation and Logs/Sensor logs/Raw reactor logs/Unisense/21.07.28"

os.chdir(file_path)
file_name = "AECCECIG.DAT"

with open(file_name,"rb") as f:
    buffer = f.readlines()
buffer[3].decode("latin-1")
# %%
