import numpy as np
from empyrical import stats
import scipy
import pandas as pd
import math
from matplotlib import pyplot as plt
import parameters

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
    'cagr',
]

COMPARITIVE_STAT_FUNCS = [
    'excess_sharpe',
    'alpha',
    'beta'
]

CUMULATIVE_STAT_FUNCS = [
    'value_at_risk',
    'conditional_value_at_risk'
]

# Performance of a portfolio
def portfolio_performance(weights, daily_returns, overall_returns = None):
    returns = np.matmul(daily_returns, weights)
    # Add statistics present in SIMPLE_STAT_FUNCS
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
def save_list_to_csv(performance, filepath, columns):
    pd.DataFrame(performance, columns=columns).to_csv(filepath)


# Generate graph from returns and compare with index returns
def generate_graph_portfolio_values(portfolio_returns, index_returns, xaxis, title):
    portfolio_value = generate_portfolio_from_returns(portfolio_returns)
    xaxis.append(xaxis[-1])
    plt.plot(xaxis, portfolio_value)

    if(parameters.STOCK_INDEX_COLUMN_NAME != None):
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


# Performance of a portfolio compared with index returns
def portfolio_performance_comparison_with_index(weights, daily_returns, index_weights, index_daily_returns, overall_returns = None, overall_index_returns = None):
    statistics = portfolio_performance(weights, daily_returns, overall_returns)
    returns = np.matmul(daily_returns, weights)

    index_statistics = portfolio_performance(index_weights, index_daily_returns, overall_index_returns)
    index_returns = np.matmul(index_daily_returns, index_weights)

    # Add statistics present in COMPARATIVE_STAT_FUNCS
    comparative_statistics = []
    comparative_statistics.append(stats.excess_sharpe(returns, index_returns))
    comparative_statistics.append(stats.alpha(returns, index_returns))
    comparative_statistics.append(stats.beta(returns, index_returns))

    statistics.extend(comparative_statistics)

    return statistics, index_statistics