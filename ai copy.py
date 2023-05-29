import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from arch import arch_model
import os

# This will be changed through the constructor. 
folder_path = 'Trading Data/DODO Feb Pump/'

# Empty dataframe
df_main = pd.DataFrame()
file_list = [] # Without .csv

# Loop through each file in the folder
for file_name in os.listdir(folder_path):
    file = file_name[:-4]
    file_list.append(file)

# Sort the list
file_list.pop(0)
file_list.sort()

for file in file_list: 
    file_path = os.path.join(folder_path, file + ".csv")
    df = pd.read_csv(file_path)
    df_main = pd.concat([df_main, df], axis = 0)

df = df_main
df = df.set_index('agg_trade_id')

# Cleaning the dataframe
df = df[['price', 'quantity', 'transact_time', 'is_buyer_maker']]

print(df)

# Cleaning up the data
df2 = df