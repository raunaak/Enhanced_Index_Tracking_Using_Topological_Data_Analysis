"""
This script creates the core strategy used to allocate and update weights in portfolio
"""

import math
import sklearn
import numpy as np
import kmapper as km
import parameters


def create_my_strategy(daily_returns, daily_index_returns, previous_weights):
    """
    Creates the core strategy using Topological Data Analysis
    """
    epsilon = 1.0 / (2 * daily_returns.shape[1])
    threshold = epsilon
    alpha = parameters.ALPHA_MULTIPLIER * epsilon
    beta = parameters.BETA_MULTIPLIER * epsilon
    daily_returns = np.transpose(daily_returns.values)
    mapper = km.KeplerMapper(verbose=0)
    lens1 = mapper.fit_transform(daily_returns, projection='mean')
    lens2 = mapper.fit_transform(daily_returns, projection='std')

    simplicial_complex = mapper.map(np.c_[lens1, lens2],
                                    X=daily_returns,
                                    clusterer=sklearn.cluster.DBSCAN(eps=0.5,
                                                                     min_samples=3),
                                    cover=km.Cover(n_cubes=np.ceil(np.power(daily_returns.shape[0], 0.25)),
                                                   perc_overlap=0.1))
    if create_my_strategy.counter == 0 or create_my_strategy.counter == 79 or create_my_strategy.counter == 158:
        mapper.visualize(simplicial_complex,
                         path_html=parameters.RESULT_DIRECTORY + "\\" +
                         parameters.STOCK_INDEX + "_simplex_" +
                         str(create_my_strategy.counter)+ ".html")

    create_my_strategy.counter += 1

    if previous_weights is None:
        current_portfolio = _get_max_sortino_ratios(daily_returns, simplicial_complex['nodes']).values()
        weights = np.zeros(daily_returns.shape[0])
        for stock_index in current_portfolio:
            weights[stock_index] = 1.0
        weights /= np.sum(weights)
        return weights
    else:
        weights = previous_weights
        alpha_weights = np.zeros(weights.shape)
        beta_weights = np.zeros(weights.shape)
        current_champion_stocks = _get_max_sortino_ratios(daily_returns,
                                                          simplicial_complex['nodes'])
        for cluster, stock_index in current_champion_stocks.items():
            if stock_index != -1:
                previous_weight_sum = np.sum(previous_weights[i]
                                             for i in simplicial_complex['nodes'][cluster])
                alpha_weights[stock_index] = alpha * previous_weight_sum

                links_dict = simplicial_complex['links']
                for curr_neighbour in links_dict[cluster]:
                    neighbour_stock_index = current_champion_stocks[curr_neighbour]
                    if neighbour_stock_index != -1:
                        beta_weights[neighbour_stock_index] += beta * previous_weight_sum

        weights = weights + alpha * alpha_weights + beta * beta_weights
        weights[weights / np.sum(weights) < threshold] = 0
        weights /= np.sum(weights)
        return weights


def _get_max_sortino_ratios(daily_returns, cluster_stock_dict):
    """
    Returns the best stock based on sortino ratio in the current cluster
    """
    current_champion_stocks = {}
    for cluster, stock_indices in cluster_stock_dict.items():
        index = -1
        max_sortino_ratio = 0
        for stock_index in stock_indices:
            curr_sortino_ratio = _get_sortino_ratio(daily_returns[stock_index, :])
            if curr_sortino_ratio > max_sortino_ratio and curr_sortino_ratio != -1:
                max_sortino_ratio = curr_sortino_ratio
                index = stock_index
        current_champion_stocks[cluster] = index
    return current_champion_stocks


def _get_sortino_ratio(returns):
    """
    Calculates sortino ratio of any stock based on its returns
    """
    num = np.mean(returns)
    den = np.std((returns - np.abs(returns))/2)
    if den == 0 or math.isnan(den):
        return -1
    return num / den

# Variable for iteration number
create_my_strategy.counter = 0
