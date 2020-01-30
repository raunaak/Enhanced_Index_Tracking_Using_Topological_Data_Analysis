"""
Initializes the metrics to be computed and performs all the calculations
Initializes the metrics to be computed and performs all the calculations
of the metrics defined above
Note: Always redefine portfolio metrics based on SIMPLE_STAT_FUNCS, COMPARITIVE_STAT_FUNCS
"""

import os
import scipy
import pandas as pd
from matplotlib import pyplot as plt
from empyrical import stats
import parameters
from metrics_utils import *

SIMPLE_STAT_FUNCS = ['Annual Return',
                     'Annual Volatility',
                     'Annual Sharpe Ratio',
                     'Annual Sortino Ratio',
                     'Omega Ratio',
                     'Calmar Ratio',
                     'Tail Ratio',
                     'Ssd',
                     'Skewness',
                     'Kurtosis',
                     'Turnover']

COMPARITIVE_STAT_FUNCS = ['Excess Sharpe Ratio',
                          'Excess Sortino Ratio',
                          'Excess Omega Ratio',
                          'Excess Calmar Ratio',
                          'Excess Tail Ratio',
                          'Excess Ssd',
                          'Alpha',
                          'Beta',
                          'Annual Tracking Error',
                          'Annual Information Ratio',
                          'Portfolio Size']


def portfolio_performance(weights, daily_returns, overall_returns=None, previous_weights=None):
    """
    Calculates performance of a portfolio
    """
    returns = np.matmul(daily_returns, weights)
    # Add statistics present in SIMPLE_STAT_FUNCS
    statistics = list([])
    statistics.append(stats.annual_return(returns))
    statistics.append(stats.annual_volatility(returns))
    statistics.append(nan_to_zero(stats.sharpe_ratio(returns)))
    statistics.append(stats.sortino_ratio(returns))
    statistics.append(stats.omega_ratio(returns))
    statistics.append(stats.calmar_ratio(returns))
    statistics.append(stats.tail_ratio(returns))
    statistics.append(ssd(returns))
    statistics.append(scipy.stats.skew(returns))
    statistics.append(scipy.stats.kurtosis(returns))
    statistics.append(turnover(weights, previous_weights))

    if overall_returns is not None:
        overall_returns.extend(returns)
    return statistics


def save_list_to_csv(performance, file_path, columns=None, index=None):
    """
    Save list of lists to csv
    """
    pd.DataFrame(performance, index=index, columns=columns).to_csv(file_path)


def generate_graph_portfolio_values(portfolio_returns, index_returns, xaxis, title):
    """
    Generate graph from returns and compare with index returns
    """
    portfolio_value = generate_portfolio_from_returns(portfolio_returns)
    xaxis.append(xaxis[-1])
    plt.plot(xaxis, portfolio_value)

    if parameters.STOCK_INDEX_COLUMN_NAME is not None:
        index_values = generate_portfolio_from_returns(index_returns)
        plt.plot(xaxis, index_values)
        plt.title(title)
        plt.savefig(parameters.RESULT_DIRECTORY + "\\" + title + '.png', bbox_inches='tight')
    else:
        plt.title(title)
        plt.show()


def generate_portfolio_from_returns(returns):
    """
    Generate portfolio from returns
    """
    portfolio = list([1.0])
    for curr_ret in returns:
        portfolio.append(portfolio[-1] * (1.0+curr_ret))
    return portfolio


def portfolio_performance_comparison_with_index(weights, daily_returns, index_weights,
                                                index_daily_returns, overall_returns=None,
                                                overall_index_returns=None, previous_weights=None):
    """
    Performance of a portfolio compared with index returns
    """
    statistics = portfolio_performance(weights, daily_returns, overall_returns,
                                       previous_weights=previous_weights)
    returns = np.matmul(daily_returns, weights)

    index_statistics = portfolio_performance(index_weights, index_daily_returns,
                                             overall_index_returns)
    index_returns = np.matmul(index_daily_returns, index_weights)
    index_returns = np.reshape(index_returns, returns.shape)

    # Add statistics present in COMPARATIVE_STAT_FUNCS
    comparative_statistics = list([])
    comparative_statistics.append(nan_to_zero(stats.sharpe_ratio(returns))
                                  - stats.sharpe_ratio(index_returns))
    comparative_statistics.append(nan_to_zero(stats.sortino_ratio(returns))
                                  - stats.sortino_ratio(index_returns))
    comparative_statistics.append(nan_to_zero(stats.omega_ratio(returns))
                                  - stats.omega_ratio(index_returns))
    comparative_statistics.append(nan_to_zero(stats.calmar_ratio(returns))
                                  - stats.calmar_ratio(index_returns))
    comparative_statistics.append(nan_to_zero(stats.tail_ratio(returns))
                                  - stats.tail_ratio(index_returns))
    comparative_statistics.append(nan_to_zero(ssd(returns))
                                  - nan_to_zero(ssd(index_returns)))
    comparative_statistics.append(stats.alpha(returns, index_returns))
    comparative_statistics.append(stats.beta(returns, index_returns))
    comparative_statistics.append(tracking_error(returns, index_returns)
                                  * np.sqrt(parameters.DAYS_IN_YEAR))
    comparative_statistics.append(stats.excess_sharpe(returns, index_returns)
                                  * np.sqrt(parameters.DAYS_IN_YEAR))
    comparative_statistics.append(np.count_nonzero(weights))
    statistics.extend(comparative_statistics)

    return statistics, index_statistics


def calculate_metrics_on_complete_data(overall_outsample_returns,
                                       overall_index_outsample_returns,
                                       colname=""):
    """
    Calculates metrics for concatenated series of outsample period returns
    and saves list of metrics to csv file
    """
    overall_outsample_statistics, overall_outsample_index_statistics = \
        portfolio_performance_comparison_with_index(
            np.array([1.0]),
            np.expand_dims(overall_outsample_returns, axis=1),
            np.array([1.0]),
            np.expand_dims(overall_index_outsample_returns, axis=1))

    save_list_to_csv(overall_outsample_statistics,
                     os.path.join(parameters.RESULT_DIRECTORY,
                                  parameters.STOCK_INDEX + colname + '_overall_outsample.csv'),
                     index=(SIMPLE_STAT_FUNCS + COMPARITIVE_STAT_FUNCS))

    save_list_to_csv(overall_outsample_index_statistics,
                     os.path.join(parameters.RESULT_DIRECTORY,
                                  parameters.STOCK_INDEX + colname + '_overall_index_outsample.csv'),
                     index=SIMPLE_STAT_FUNCS)
