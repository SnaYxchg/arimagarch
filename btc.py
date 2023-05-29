import requests
import pandas as pd
import warnings
import json
import os
from datetime import *
import subprocess
import shutil
from time import sleep
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller
from arch import arch_model
import numpy as np
import matplotlib.pyplot as plt

warnings.filterwarnings("ignore")

minOneWeekGain = -10
minOneMonthGain = -30

print("\n Hi my name is CryptoWise and I'm your AI Crypto Investment Assistant!")
print("My goal is to help you make informed decisions on which coins to invest in, using the ARIMA and GARCH machine learning models.")
print("Let's get started by analyzing the market and finding the best opportunities for you.\n")
sleep(5)


url = "https://fapi.binance.com/fapi/v1/exchangeInfo"
response = requests.get(url)
data = response.json()
symbols = [symbol["symbol"] for symbol in data["symbols"] if symbol["quoteAsset"] == "USDT"]

# Initialize results DataFrame
results = pd.DataFrame(columns=["Pair", "Recent Gain %", "Uptrend"])

# Analyze each USDT-margined symbol
for symbol in symbols:
    klines_url = f"https://fapi.binance.com/fapi/v1/klines?symbol={symbol}&interval=1d&limit=31"
    klines_data = requests.get(klines_url).json()
    close_prices = [float(kline[4]) for kline in klines_data]

    # Check if there is enough data
    if len(close_prices) >= 31:
        # Calculate gains
        recent_gain = (close_prices[-1] - close_prices[-8]) / close_prices[-8] * 100
        monthly_gain = (close_prices[-1] - close_prices[-31]) / close_prices[-31] * 100

        # Check if pair meets the gain requirements
        if recent_gain >= minOneWeekGain and monthly_gain >= minOneMonthGain:
            # Check if pair is in an uptrend
            sma_short = sum(close_prices[-8:-1]) / 7
            sma_long = sum(close_prices[-31:-1]) / 30
            uptrend = sma_short > sma_long

            if uptrend:
                results = results.append({'Pair': symbol, 'Recent Gain %': recent_gain, 'Uptrend': uptrend}, ignore_index=True)

            print(results.tail(1))


def check_bitcoin_growth(weekly_threshold, monthly_threshold):
    url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=usd&days=30&interval=daily"
    response = requests.get(url)
    data = json.loads(response.text)
    
    prices = data['prices']
    latest_price = prices[-1][1]
    one_week_ago_price = prices[-8][1]
    one_month_ago_price = prices[0][1]
    
    percent_change_7d = ((latest_price - one_week_ago_price) / one_week_ago_price) * 100
    percent_change_30d = ((latest_price - one_month_ago_price) / one_month_ago_price) * 100
    
    if percent_change_7d >= weekly_threshold and percent_change_30d >= monthly_threshold:
        print(f"Bitcoin is up {percent_change_7d:.2f}% in the last week and {percent_change_30d:.2f}% in the last month.")
        return True
    else:
        print(f"Bitcoin did not meet the growth criteria. It is up {percent_change_7d:.2f}% in the last week and {percent_change_30d:.2f}% in the last month.")
        return False

weekly_growth_threshold = -20
monthly_growth_threshold = -20

market_condition = check_bitcoin_growth(weekly_growth_threshold, monthly_growth_threshold)

if market_condition:
    print(f"It's a suitable time to invest in crypto tokens. ")
    print("")
else:
    print("It isn't a suitable time to invest in the crypto markets as bitcoin is bearish. Please come back later!")
    exit()


valid_tickers = results.loc[:, 'Pair'].tolist()
print("Here are the best tokens to invest in, according to current market conditions:- ")
print(valid_tickers)


choice = input("Choose a ticker that you want to invest in: ")
timedays = int(input("Choose the lookback days: "))

# Running the binance library to download data
working_directory = 'binance/python'
script_name = 'downloadkline'

date = datetime.today() - timedelta(days=timedays)
date = date.strftime('%Y-%m-%d')

command = ['python3', '-m', script_name, '-t', 'spot', '-s', choice, '-i', '5m', '-startDate', date]
result = subprocess.run(command, cwd=working_directory, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

# Check the return code (0 means success)
if result.returncode == 0:
    print('Command succeeded with output:')
    print(result.stdout)
else:
    print('Command failed with error:')
    print(result.stderr)

# Next extract the files and drop them into a folder in the python directory. Go to the directory with the zips first. 

file_list = []
folder_path = f'binance/python/data/spot/daily/klines/{choice}/5m'

for file_name in os.listdir(folder_path):
    if file_name[-4:] == '.zip':
        # Extract it to folder
        unzip = ['unzip', file_name, '-d', choice]
        result = subprocess.run(unzip, cwd=folder_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if result.returncode == 0:
            print('Command succeeded with output:')
            print(result.stdout)
        else:
            print('Command failed with error:')
            print(result.stderr)

# Now move it to python folder

src = f'binance/python/data/spot/daily/klines/{choice}/5m/'
dest = 'binance/python/'

# If it's already there, it's deleted and updated with the new files. 
if os.path.exists(dest + choice):
    shutil.rmtree(dest + choice)

os.rename(src + choice, dest + choice)






# Analysis code
# !!!!
# !!!!!
# !!!!!!




ticker = choice
# ticker = "JASMYUSDT"
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

# ADF Test

print("")
result = adfuller(currentDf['Returns'])
print('p-value: ', result[1])

print("")

model = arch_model(currentDf['Returns'], mean='Zero', vol='GARCH', p=1, q=1)
results = model.fit()

print(results.summary())

print("")


num_rows = currentDf.shape[0]

forecast_horizon = int(num_rows / 10) # Forecasting a third of the total observations

garch_forecast = results.forecast(horizon=forecast_horizon)

# Calculate the conditional volatility
conditional_volatility = np.sqrt(garch_forecast.variance.dropna().values)


forecast_periods = conditional_volatility.shape[1]

plt.figure(figsize=(10, 6))
plt.plot(range(1, forecast_periods + 1), conditional_volatility[0])
plt.xlabel('Forecast Period')
plt.ylabel('Conditional Volatility')
plt.title('GARCH Conditional Volatility Forecast')
plt.grid(True)
plt.show()


df = currentDf

historical_std_dev = df['Returns'].std() # It's in percentage

print("Historical Standard Deviation", historical_std_dev)
print("\n")

# Assuming 'garch_model' is the fitted GARCH model
alpha = results.params['alpha[1]']
beta = results.params['beta[1]']
omega = results.params['omega']

alpha_pvalue = results.pvalues['alpha[1]']
beta_pvalue = results.pvalues['beta[1]']
omega_pvalue = results.pvalues['omega']

print(f"Alpha: {alpha:.4f} (p-value: {alpha_pvalue:.4f})")
print(f"Beta: {beta:.4f} (p-value: {beta_pvalue:.4f})")
print(f"Omega: {omega:.4f} (p-value: {omega_pvalue:.4f})")

print("\nExplanation:")
print("Alpha represents the ARCH effect or the impact of past shocks (returns) on future volatility.")
print("Beta represents the GARCH effect or the persistence of past volatility in predicting future volatility.")
print("Omega represents the long-run average volatility when there are no shocks.")
print("\nP-values indicate the significance of each parameter. Lower p-values (typically below 0.05) suggest that the corresponding parameter is statistically significant.")