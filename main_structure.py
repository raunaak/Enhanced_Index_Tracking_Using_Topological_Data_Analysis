"""
Run this file to generate output
"""

import numpy as np
import pandas as pd
import parameters
import metrics
import reader
import strategy


def main():
    """
    Main function for the computation engine
    """
    # Read data
    index_complete_data, constituent_complete_data = \
        reader.read_csv_or_excel_file(parameters.INPUT_FILENAME,
                                      index_col=parameters.INDEX_COLUMN_NAME)

    # Outsample Returns
    overall_outsample_returns, overall_index_outsample_returns = list([]), list([])
    overall_outsample_time = list([])

    # Outsample Returns during 'UP' and 'DOWN' phases
    up_overall_outsample_returns, up_overall_index_outsample_returns = list([]), list([])
    down_overall_outsample_returns, down_overall_index_outsample_returns = list([]), list([])

    # Store previous weights
    previous_weights = None

    # Rolling Window
    for i in range(parameters.TOTAL_PERIOD, constituent_complete_data.shape[0], parameters.OUTSAMPLE_PERIOD):
        # Current Period Data
        current_data = constituent_complete_data.iloc[i - parameters.TOTAL_PERIOD:i]

        if parameters.STOCK_INDEX_COLUMN_NAME is not None:
            current_index_data = index_complete_data.iloc[i - parameters.TOTAL_PERIOD:i]

        overall_outsample_time.extend(constituent_complete_data.index.get_values()[i - parameters.OUTSAMPLE_PERIOD + 1:i])

        # Daily Returns
        daily_returns = current_data.div(current_data.shift(1))-1
        daily_returns.dropna(inplace=True, how='all')
        daily_returns.fillna(0.0, inplace=True)

        if parameters.STOCK_INDEX_COLUMN_NAME is not None:
            daily_index_returns = current_index_data.div(current_index_data.shift(1))-1.0
            daily_index_returns.dropna(inplace=True, how='all')
            daily_index_returns.fillna(0.0, inplace=True)

        # Portfolio Creation
        weights = strategy.create_my_strategy(pd.DataFrame(daily_returns.values[:parameters.INSAMPLE_PERIOD]),
                                              pd.DataFrame(daily_index_returns[:parameters.INSAMPLE_PERIOD]),
                                              previous_weights)

        overall_outsample_returns.extend(np.matmul(daily_returns.values[parameters.INSAMPLE_PERIOD:, :], weights))
        overall_index_outsample_returns.extend(daily_index_returns.values[parameters.INSAMPLE_PERIOD:, :].flatten())

        if parameters.STOCK_INDEX_COLUMN_NAME is not None:
            if current_index_data.iat[parameters.INSAMPLE_PERIOD, 0] / current_index_data.iat[0, 0] > 1:
                up_overall_outsample_returns.extend(np.matmul(daily_returns.values[parameters.INSAMPLE_PERIOD:, :], weights))
                up_overall_index_outsample_returns.extend(daily_index_returns.values[parameters.INSAMPLE_PERIOD:, :].flatten())
            else:
                down_overall_outsample_returns.extend(np.matmul(daily_returns.values[parameters.INSAMPLE_PERIOD:, :], weights))
                down_overall_index_outsample_returns.extend(daily_index_returns.values[parameters.INSAMPLE_PERIOD:, :].flatten())

        previous_weights = weights

    weights = np.sort(weights)
    pd.DataFrame(weights, columns=["Weights"]).to_csv(parameters.RESULT_DIRECTORY + "\\Weights.csv")

    # Generate graph containing time vs portfolio value to compare portfolio and index portfolio
    metrics.generate_graph_portfolio_values(
        overall_outsample_returns, overall_index_outsample_returns,
        xaxis=overall_outsample_time, title='D' + str(1+parameters.STOCK_NUMBER))

    # Calculate the metrics on a complete return series
    metrics.calculate_metrics_on_complete_data(overall_outsample_returns, overall_index_outsample_returns, colname="")
    metrics.calculate_metrics_on_complete_data(up_overall_outsample_returns, up_overall_index_outsample_returns, colname="_up")
    metrics.calculate_metrics_on_complete_data(down_overall_outsample_returns, down_overall_index_outsample_returns, colname="_down")

# Call main function
main()
