import numpy as np
import pandas as pd
import os
import parameters

# Separates index column and stock column
def read_csv_or_excel_file(filename, index_col):
    if(filename.endswith('xlsx')):
        df = pd.read_excel(os.path.join(parameters.INPUT_DIRECTORY, filename), index_col = index_col)
    else:
        df = pd.read_csv(os.path.join(parameters.INPUT_DIRECTORY, filename), index_col = index_col)

    if(parameters.STOCK_INDEX_COLUMN_NAME != None):
        df_index = df[[parameters.STOCK_INDEX_COLUMN_NAME]]
        return df_index, df.drop(columns = [parameters.STOCK_INDEX_COLUMN_NAME])
    return pd.DataFrame(), df