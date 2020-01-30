"""
Initializes all the necessary parameters used in creating
and analysis portfolio performance relative to its index
"""

# Rolling Window parameters
MONTH_LENGTH = 21
INSAMPLE_PERIOD = 6 * MONTH_LENGTH
OUTSAMPLE_PERIOD = 1 * MONTH_LENGTH
TOTAL_PERIOD = INSAMPLE_PERIOD + OUTSAMPLE_PERIOD

# Days and months in a year
DAYS_IN_YEAR = 12 * MONTH_LENGTH  # for daily data
WEEKS_IN_YEAR = 52  # for weekly data

STOCK_INDICES = ['CNX50',
                 'DAX30',
                 'DOWJONES65',
                 'FTSE100',
                 'FTSE250',
                 'NIFTY500',
                 'S&P100',
                 'S&P500']

STOCK_INDEX_COLUMN_NAMES = ['CNX NIFTY (50) - PRICE INDEX',
                            'DAX 30 PERFORMANCE - PRICE INDEX',
                            'DOW JONES COMPOSITE 65 STOCK AVE - PRICE INDEX',
                            'FTSE 100 - PRICE INDEX',
                            'FTSE 250 - PRICE INDEX',
                            'NIFTY 500 - PRICE INDEX',
                            'S&P GLOBAL 100 - PRICE INDEX',
                            'S&P 500 COMPOSITE - PRICE INDEX']

# Parameters used for reading stock_index (filename)
# and stock_index_column_name (column containing index)
STOCK_NUMBER = 7
STOCK_INDEX = STOCK_INDICES[STOCK_NUMBER]
STOCK_INDEX_COLUMN_NAME = STOCK_INDEX_COLUMN_NAMES[STOCK_NUMBER]

# Directories for input and output data
RESULT_DIRECTORY = 'Super_Final_Results\\' + STOCK_INDEX
INPUT_DIRECTORY = 'Stock_Data'

# Input file details
INPUT_FILEEXTENSION = '.xlsx'
INPUT_FILENAME = STOCK_INDEX + INPUT_FILEEXTENSION
INDEX_COLUMN_NAME = 'Time'

# Strategy parameters
ALPHA_MULTIPLIER = 40
BETA_MULTIPLIER = 10
