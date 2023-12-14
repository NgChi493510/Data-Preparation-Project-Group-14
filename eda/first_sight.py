import pandas as pd
from IPython.display import display
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.pyplot as plt

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
    print("\tFeatures' NaN values:")
    col_info['Number of Missing Values'] = df.isnull().sum()
    col_info['Percent of Missing Values'] = col_info['Number of Missing Values'] / df.shape[0] * 100
    nan_num = col_info[col_info['Number of Missing Values'] != 0].shape[0]
    print(f"Number of columns having NaN values: {nan_num} columns")
    if nan_num !=0:
        f, ax = plt.subplots(figsize=(16,nan_num/5))
        sns.barplot(col_info[col_info['Percent of Missing Values']!=0]['Percent of Missing Values'].sort_values(ascending=False),\
            orient='h',width=0.4,palette='ch:s=.6,r=-.2')
        #sns.barplot((df.isnull().sum()/df.shape[0]).sort_values(ascending=False).head(60),\
                    #orient='h',width=0.4,palette='ch:s=.6,r=-.2',)
        ax.spines[['right','top','bottom','left']].set_visible(False)
        ax.tick_params(left=False)
        ax.xaxis.tick_top() 
        ax.grid(axis='x')
    #display(col_info[col_info['Number of Missing Values']!=0].sort_values(by='Number of Missing Values', ascending=False)[['Number of Missing Values','Percent of Missing Values']])