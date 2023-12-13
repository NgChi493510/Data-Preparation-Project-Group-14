import pandas as pd
from IPython.display import display
import matplotlib.pyplot as plt
import seaborn as sns

def __get_df_name(df):
    name = name =[x for x in globals() if globals()[x] is df][0]
    return name

def first_sight(df:pd.DataFrame, name:str):
    print('-'*30)
    print(f'\033[1m{name}\033[0m')
    print('-'*30)
    print(f'\tShape:{df.shape}')
    print(f'\tDuplicate values:{df.shape[0]-df.duplicated().shape[0]}')
    print('\tFirst 5 rows:')
    display(df.head(5))
    print("\tFeatures' datatype:")
    col_info = pd.DataFrame()
    col_info.index = df.columns
    col_info['Datatype'] = df.dtypes
    display(col_info)
    print("\tFeatures' descriptive statistics:")
    display(df.describe().T)
    print("\tFeatures' NaN values::")
    col_info['Number of Missing Values'] = df.isnull().sum()
    col_info['Percent of Missing Values'] = col_info['Number of Missing Values'] / df.shape[0] * 100
    print(f"Number of columns having NaN values: {col_info[col_info['Number of Missing Values'] != 0].shape[0]} columns")
    display(col_info[col_info['Number of Missing Values']!=0].sort_values(by='Number of Missing Values', ascending=False)[['Number of Missing Values','Percent of Missing Values']])