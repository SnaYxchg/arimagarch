import pandas as pd
import numpy as np

from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller
# from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from arch import arch_model
import os

# Choose your ticker! :) 

ticker = "IDUSDT"

# This will be changed through the constructor. 
folder_path = f'binance/python/{ticker}/'

# Empty dataframe
df_main = pd.DataFrame()
file_list = [] # Without .csv

# Loop through each file in the folder
for file_name in os.listdir(folder_path):
    file = file_name[:-4]
    file_list.append(file)


# Sort the list
file_list.sort()
file_list.pop(0)

print(file_list)

for file in file_list: 
    file_path = os.path.join(folder_path, file + ".csv")
    df = pd.read_csv(file_path)
    df.columns = ['Open Time', 'Open Price', 'H', 'L', 'C', 'Volume', 'Close Time', 'Quote Vol', 'No. Of Trades', 'Taker Buy Vol', 'Taker Buy Quote Vol', 'Faltu']

    df_main = pd.concat([df_main, df], axis = 0)


df = df_main

currentDf = df

# Working on the current dataframe

currentDf = currentDf.drop(['H', 'L', 'C', 'Volume', 'Close Time', 'Quote Vol', 'No. Of Trades', 'Taker Buy Vol', 'Taker Buy Quote Vol', 'Faltu'], axis=1)
currentDf['Open Time'] = pd.to_datetime(currentDf['Open Time'], unit='ms')
currentDf = currentDf.set_index('Open Time')


array = df['Open Price'].values
log_returns = np.diff(np.log(array))*100 # Times 100, so in %
print(log_returns)

arr = np.concatenate((np.array([0]), log_returns))

currentDf['Returns'] = arr
currentDf['Cumulative Returns'] = np.cumsum(arr)


currentDf.to_csv(f"{ticker}.csv")

print("")
result = adfuller(currentDf['Returns'])
print('ADF Statistic: ', result[0])
print('p-value: ', result[1])

print("")

model = arch_model(currentDf['Returns'], mean='Zero', vol='GARCH', p=1, q=1)
results = model.fit()

print(results.summary())


df = currentDf
print(df)



# # Testing for stationarity with the ADF test. 

# # Cleaning up the data first
# df2 = df

# df2['transact_time'] = pd.to_datetime(df2['transact_time'], unit='us') # Re-doing the df with transact time as the index
# df2 = df2.set_index('transact_time')

# # Check if the index is unique and drop any duplicate index values
# if not df2.index.is_unique:
#     df2 = df2[~df2.index.duplicated(keep='first')]

# resampled = df2.asfreq('100L', method='ffill')
# resampled['price'] = resampled['price'].fillna(method='ffill', limit=1, inplace=False)

# print(resampled)

# df2['price'].plot(figsize=(12,6), title='DODOBUSD.P', xlabel='Time', ylabel='Price')
# plt.show()