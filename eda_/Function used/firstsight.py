import pandas as pd
from IPython.display import display

def __get_df_name(df):
    name = name =[x for x in globals() if globals()[x] is df][0]
    return name

def firstsight(df:pd.DataFrame, name:str):
    print('-'*30)
    print(f'\033[1m{name}\033[0m')
    print('-'*30)
    print(f'\tShape:{df.shape}')
    print('\tFirst 5 rows:')
    display(df.head(5))
    print("\tFeatures' datatype and null count:")
    col_info = pd.DataFrame()
    col_info.index = df.columns
    col_info['Datatype'] = df.dtypes
    col_info['Number of Missing Values'] = df.isnull().sum()
    col_info['Percent of Missing Values'] = col_info['Number of Missing Values'] / df.shape[0] * 100
    display(col_info)
    print("\tFeatures' descriptive statistics:")
    display(df.describe().T)

