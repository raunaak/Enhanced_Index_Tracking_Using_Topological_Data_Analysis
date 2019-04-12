import numpy as np
from empyrical import stats
import scipy
import pandas as pd

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
def portfolio_performance(weights, daily_returns):
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

    return statistics


# Average Metrics over all the rolling windows
def average_metrics(performance):
    performance.append(np.mean(np.array(performance), axis=0).tolist())


# Save list of lists to csv
def save_list_to_csv(performance, filepath):
    pd.DataFrame(performance, columns=SIMPLE_STAT_FUNCS).to_csv(filepath)
