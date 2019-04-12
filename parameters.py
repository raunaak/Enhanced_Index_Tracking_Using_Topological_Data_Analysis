# Rolling Window parameters
MONTH_LENGTH = 21
INSAMPLE_PERIOD = 6 * MONTH_LENGTH
OUTSAMPLE_PERIOD = MONTH_LENGTH
TOTAL_PERIOD = INSAMPLE_PERIOD + OUTSAMPLE_PERIOD

# Days and months in a year
DAYS_IN_YEAR = 12 * MONTH_LENGTH #for daily data
WEEKS_IN_YEAR = 52 #for weekly data

# Directories for input and output data
RESULT_DIRECTORY = 'Results'
INPUT_DIRECTORY = 'Stock_Data'

# Parameters used for reading stock_index (filename)
# and stock_index_column_name (column containing index)
STOCK_INDEX = 's&p500'
STOCK_INDEX_COLUMN_NAME = None