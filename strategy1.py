import numpy as np
import kmapper as km
import sklearn
import math

# Create your strategy here
def create_my_strategy(daily_returns, daily_index_returns, previous_weights):
    # A sample 1/n strategy has been created here
    weights = np.zeros(daily_returns.shape[0])
    for stock_index in current_portfolio:
        weights[stock_index] = 1
    weights = weights/np.sum(weights)

    return weights
