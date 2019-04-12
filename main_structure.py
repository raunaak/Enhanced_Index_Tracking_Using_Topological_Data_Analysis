#https://medium.com/@mariano.scandizzo/strategic-asset-allocation-with-python-c9afef392e90
#The aim of this file is to understand implementation of portfolio metrics in a rolling window scenario
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import parameters
import metrics
#import seaborn as sns; sns.set()
#plt.style.use('ggplot')


# Read data
stock_index = 's&p500'
index_data = read_data(file_path)
datos = pd.read_excel('Stock_Data\\' + stock_index + '.xlsx', index_col='Time')


# Portfolio Metrics
insample_performance = []
outsample_performance = []


# Rolling Window
for i in range(parameters.TOTAL_PERIOD, datos.shape[0], parameters.OUTSAMPLE_PERIOD):
    # Current Period Data
    current_data = datos.iloc[i-parameters.TOTAL_PERIOD:i]

    # Daily Returns
    daily_returns = np.log(current_data.div(current_data.shift(1)))
    daily_returns.dropna(inplace=True, how='all')
    daily_returns.fillna(0, inplace=True)

    # Portfolio Creation
    weights = np.random.rand(datos.shape[1])

    # Portfolio Metrics for every outsample window
    insample_performance.append(metrics.portfolio_performance(weights, daily_returns.values[:parameters.INSAMPLE_PERIOD,:]))
    outsample_performance.append(metrics.portfolio_performance(weights, daily_returns.values[parameters.INSAMPLE_PERIOD:, :]))


# Average portfolio metrics
metrics.average_metrics(insample_performance)
metrics.average_metrics(outsample_performance)


#Save metrics as csv
metrics.save_list_to_csv(insample_performance, metrics.RESULT_DIRECTORY + '\\insample_' + stock_index + '.csv')
metrics.save_list_to_csv(outsample_performance, metrics.RESULT_DIRECTORY  + '\\outsample_' + stock_index + '.csv')