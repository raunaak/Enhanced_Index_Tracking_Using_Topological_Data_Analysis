import numpy as np
from empyrical import stats
import scipy
import pandas as pd
import math
from matplotlib import pyplot as plt

SIMPLE_STAT_FUNCS = [
    'annual_return',
    'annual_volatility',
    'sharpe_ratio',
    'calmar_ratio',
    #'stability_of_timeseries',
    #'max_drawdown',
    'omega_ratio',
    'sortino_ratio',
    'stats.skew',
    'stats.kurtosis',
    'tail_ratio',
    'cagr'
]

# Performance of a portfolio
def portfolio_performance(weights, daily_returns, overall_returns = None):
    returns = np.matmul(daily_returns, weights)

    statistics = []
    statistics.append(stats.annual_return(returns))
    statistics.append(stats.annual_volatility(returns))
    statistics.append(stats.sharpe_ratio(returns))
    statistics.append(stats.calmar_ratio(returns))
    #statistics.append(stats.stability_of_timeseries(returns))
    #statistics.append(stats.max_drawdown(returns))
    statistics.append(stats.omega_ratio(returns))
    statistics.append(stats.sortino_ratio(returns))
    statistics.append(scipy.stats.skew(returns))
    statistics.append(scipy.stats.kurtosis(returns))
    statistics.append(stats.tail_ratio(returns))
    statistics.append(stats.cagr(returns))

    if(overall_returns!=None):
        overall_returns.extend(returns)
    return statistics


# Average Metrics over all the rolling windows
def average_metrics(performance):
    performance.append(np.mean(np.array(performance), axis=0).tolist())


# Save list of lists to csv
def save_list_to_csv(performance, filepath):
    pd.DataFrame(performance, columns=SIMPLE_STAT_FUNCS).to_csv(filepath)


# Generate graph from returns and compare with index returns
def generate_graph_portfolio_values(portfolio_returns, index_returns, xaxis, title):
    portfolio_value = generate_portfolio_from_returns(portfolio_returns)
    xaxis.append(xaxis[-1])
    plt.plot(xaxis, portfolio_value)

    if(index_returns != None):
        index_values = generate_portfolio_from_returns(index_returns)
        plt.plot(xaxis, index_values)
        plt.legend(['Portfolio Value', 'Index Value'])
        plt.title(title)
        plt.show()
    else:
        plt.legend(['Portfolio Value'])
        plt.title(title)
        plt.show()


# Generate portfolio from returns
def generate_portfolio_from_returns(returns):
    portfolio = [1]
    for x in returns:
        portfolio.append(portfolio[-1] * math.exp(x))
    return portfolio