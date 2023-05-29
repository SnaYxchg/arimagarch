import ai

# Plotting the line series
priceDF = df
priceDF = priceDF.set_index('transact_time')

priceDF['price'].plot(figsize=(12,6), title='DODOBUSD.P', xlabel='Time', ylabel='Price')

plt.show()