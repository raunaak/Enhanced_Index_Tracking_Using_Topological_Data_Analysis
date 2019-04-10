#https://medium.com/@mariano.scandizzo/strategic-asset-allocation-with-python-c9afef392e90
#The aim of this file is to understand implementation of portfolio metrics in a rolling window scenario
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
plt.style.use('ggplot')
number_of_days = 240 #for daily data
number_of_weeks = 52 #for weekly data

#Read data
datos = pd.read_excel('s&p500.xlsx',index_col='Time')


#Normalize data
normalized_series = (datos/datos.iloc[0])


#Rolling Window parameters
month = 20
insample_period = 6 * 20
outsample_period = 20
total_period = insample_period + outsample_period


#Portfolio Metrics
stats = pd.DataFrame()
'''
stats['Annualized Returns(%)'] = daily_returns.mean() * number_of_days * 100
stats['Annualized Volatility(%)'] = daily_returns.std() * np.sqrt(number_of_days) * 100
stats['Sharpe Ratio'] = stats['Annualized Returns(%)'] / stats['Annualized Volatility(%)']
print(82 * '-')
print('Assets Classes Annualized Statistics - full observation period')
stats.style.bar(color=['red', 'green'], align='zero')
'''

#Rolling Window
for i in range(total_period, datos.shape[0], outsample_period):
    #current period data
    current_data = current_data[i-total_period:total_period]
    # Daily Returns
    daily_returns = np.log(current_data / current_data.shift(1))
    daily_returns.dropna(inplace=True)
    