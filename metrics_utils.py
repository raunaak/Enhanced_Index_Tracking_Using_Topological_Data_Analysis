"""
Contains all the utility functions used to calculate metrics
"""

import math
from empyrical import cum_returns_final
from empyrical.utils import nanmean, nanstd
import numpy as np


def return_calculation(returns):
    """
    Calculates cumulative returns of a portfolio without any annualization
    """
    ending_value = cum_returns_final(returns, starting_value=1)
    return ending_value - 1


def nan_to_zero(num):
    """
    Converts nan to 0
    """
    if math.isnan(num):
        return 0
    return num


def tracking_error(returns, factor_returns):
    """
    Calculate standard deviation of portfolio return - index return and annualize it
    """
    active_return = returns - factor_returns
    tracking_err = np.nan_to_num(nanstd(active_return, ddof=1, axis=0))
    return tracking_err


def ssd(returns):
    """
    Calculate semi standard deviation of returns
    """
    ret = np.copy(returns)
    mean_ret = nanmean(ret)
    ret[ret > nanmean(ret)] = mean_ret
    std = 0
    for curr_ret in ret:
        std += (curr_ret-mean_ret)*(curr_ret-mean_ret)
    std /= (ret.shape[0]-1)
    return np.sqrt(std)


def turnover(weights, previous_weights):
    """
    Calculate turnover of weights
    """
    if previous_weights is None:
        return 0
    return np.sum(np.abs(previous_weights-weights))
