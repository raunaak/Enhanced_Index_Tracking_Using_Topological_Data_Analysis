import numpy as np
import pandas as pd
import os
import parameters

# Separates index column and stock column
def read_csv_or_excel_file(filename, index_col='Time', stock_index_column_name=None):
    if(filename.endswith('xlsx')):
        df = pd.read_excel(os.path.join(parameters.INPUT_DIRECTORY, filename), index_col=index_col)
    else:
        df = pd.read_csv(os.path.join(parameters.INPUT_DIRECTORY, filename), index_col=index_col)

    if(stock_index_column_name != None): df_index = df[stock_index_column_name]
    return df_index, df