#https://medium.com/@mariano.scandizzo/strategic-asset-allocation-with-python-c9afef392e90
#The aim of this file is to understand implementation of portfolio metrics in a rolling window scenario
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import parameters
import metrics
import reader
import os
#import seaborn as sns; sns.set()
#plt.style.use('ggplot')


# Read data
index_datos, datos = reader.read_csv_or_excel_file(parameters.STOCK_INDEX + '.xlsx', index_col ='Time', )


# Portfolio Metrics
insample_performance, insample_index_performance  = [], []
outsample_performance, outsample_index_performance = [], []

#Outsample Returns
overall_outsample_returns, overall_index_outsample_returns = [], []
overall_outsample_time = []

# Rolling Window
for i in range(parameters.TOTAL_PERIOD, datos.shape[0], parameters.OUTSAMPLE_PERIOD):

    # Current Period Data
    current_data = datos.iloc[i-parameters.TOTAL_PERIOD:i]

    if(parameters.STOCK_INDEX_COLUMN_NAME != None):
        current_index_data = datos.iloc[i-parameters.TOTAL_PERIOD:i]

    overall_outsample_time.extend(datos.index.get_values()[i-parameters.OUTSAMPLE_PERIOD:i])


    # Daily Returns
    daily_returns = np.log(
        current_data.div(current_data.shift(1)))
    daily_returns.dropna(inplace=True, how='all')
    daily_returns.fillna(0, inplace=True)

    if (parameters.STOCK_INDEX_COLUMN_NAME != None):
        daily_index_returns = np.log(
            current_index_data.div(current_index_data.shift(1)))
        daily_index_returns.dropna(inplace=True, how='all')
        daily_index_returns.fillna(0, inplace=True)


    # Portfolio Creation
    weights = np.random.rand(datos.shape[1])


    # Portfolio Metrics for every outsample window
    insample_performance.append(
        metrics.portfolio_performance(weights, daily_returns.values[:parameters.INSAMPLE_PERIOD,:]))
    outsample_performance.append(
        metrics.portfolio_performance(weights, daily_returns.values[parameters.INSAMPLE_PERIOD:, :]), overall_outsample_returns)

    if (parameters.STOCK_INDEX_COLUMN_NAME != None):
        insample_index_performance.append(
            metrics.portfolio_performance(np.array([1]), daily_index_returns.values[:parameters.INSAMPLE_PERIOD, :]))
        outsample_index_performance.append(
            metrics.portfolio_performance(np.array([1]), daily_index_returns.values[parameters.INSAMPLE_PERIOD:, :]), overall_index_outsample_returns)


# Average portfolio metrics
metrics.average_metrics(insample_performance)
metrics.average_metrics(outsample_performance)

metrics.average_metrics(insample_index_performance)
metrics.average_metrics(outsample_index_performance)


# Save metrics as csv
metrics.save_list_to_csv(insample_performance, os.path.join(parameters.RESULT_DIRECTORY, 'insample_' + parameters.STOCK_INDEX + '.csv'))
metrics.save_list_to_csv(outsample_performance, os.path.join(parameters.RESULT_DIRECTORY, 'outsample_' + parameters.STOCK_INDEX + '.csv'))

metrics.save_list_to_csv(insample_index_performance, os.path.join(parameters.RESULT_DIRECTORY, 'insample_index_' + parameters.STOCK_INDEX + '.csv'))
metrics.save_list_to_csv(outsample_index_performance, os.path.join(parameters.RESULT_DIRECTORY, 'outsample_index_' + parameters.STOCK_INDEX + '.csv'))


# Generate graph containing time vs portfolio value to compare portfolio and index portfolio
metrics.generate_graph_portfolio_values(
    overall_outsample_returns, overall_index_outsample_returns, xaxis = overall_outsample_time, title = parameters.STOCK_INDEX)