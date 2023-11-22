import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def stats_summary1(df):
    print(df.info())
    print("-----"*15)
    print(f"Shape of the dataframe is {df.shape} \n")
    print("-----"*15)
    print(f"Statistical summary of dataframe is :")
    print("-----"*15)
    print(f"Description of the dataframe:\n")
    print(df.describe()) 
    

def stats_summary2(df, df_name):   
    print(f"Description of the df continued for {df_name}:\n")
    print("-----"*15)
    print("Data type value counts: \n",df.dtypes.value_counts())
    print("\nReturn number of unique elements in the object. \n")
    print(df.select_dtypes('object').apply(pd.Series.nunique, axis = 0))

def missing_values_table(df, df_name):
    print(f"Check missing value for {df_name}:\n")
    print("-----"*15)
    count=df.isnull().sum().sort_values(ascending=False)
    percentage=(df.isnull().sum()/len(df))*100
    table=pd.concat([count,percentage],keys=['Total missing values','Percentage'],axis=1)
    miss_val_table = table[table.iloc[:, 1] != 0].sort_values('Percentage', ascending=False).round(2)
    print(df_name + 'has: ' + str(df.shape[1]) + ' columns.')
    print('There are '+ str(miss_val_table.shape[0]) + ' columns that have missing values.')
    return miss_val_table

def feature_datatypes_groups(df, df_name):
    df_dtypes = df.columns.to_series().groupby(df.dtypes).groups
    print("-----"*15)
    print(f"Categorical and Numerical(int + float) features  of {df_name}.")
    print("-----"*15)
    print()
    for k, v in df_dtypes.items():
        print({k.name: v})
        print("---"*10)
    print("\n \n")    

def visual_corr(df, feature,n,ax):
    pos = df.loc[feature].sort_values()[-(n+1):-1]
    neg = df.loc[feature].sort_values()[:n]
    t = df.loc['TARGET',feature]
                   
    new = pd.concat((pos,neg))
    new.loc['TARGET'] = t
    new = new.sort_values(ascending=False)
    # f, ax = plt.subplots(figsize=(8,5))
    sns.barplot(new.squeeze() ,orient='h',ax = ax,alpha=0.3,width=0.5)

    ax.spines[['top','bottom']].set_visible(False)
    ax.spines[['left','right']].set_color('grey')
    ax.xaxis.tick_top()
    ax.tick_params(left = False,top = False)
    ax.set_xticklabels('')
    l= ax.get_xlim()[1] - ax.get_xlim()[0]

    for p in ax.patches:
        x,y = p.get_xy()
        width = p.get_width()
        # height = p.get_height()
        if width <= 0:
            ax.annotate(xy = (x+l/30 , y+0.4 ), text = str(int(width*100))+'%')
        else:
            ax.annotate(xy = (x-l/16 , y+0.4 ), text = str(int(width*100))+'%')
    sns.barplot(new.tail(n).squeeze() ,orient='h',ax = ax,color ='red',alpha=0.3,width=0.5)
    sns.barplot(data = {'TARGET': t} ,orient='h',ax = ax,color ='lightgreen',alpha=1,width=0.5,\
                edgecolor= 'green')
    
    for i in range(len(new)):
        if new.index[i] == 'TARGET':
            ax.axhline(y=i,linewidth=25, color = 'grey', alpha = 0.2)
            if t <= 0:
                ax.text(x= l/10, y =i+0.14, s = feature + ' correlate with TARGET')
            else:
                ax.text(x= t+l/10, y =i+0.14, s = feature + ' correlate with TARGET')

    # ax.set_yticklabels(list(new.index), fontdict = {'horizontalalignment': 'left'})
    # ax.axvline(ax.get_xlim()[1]+l/30,color = 'grey',alpha = 0.2)
    ax.set_xlim(ax.get_xlim()[0]-l/24,ax.get_xlim()[1])
    # for i in range(len(new)):
        # ax.yaxis.get_majorticklabels()[i].set_x(0.7)
    ax.set_xlabel('')
    yticklabel = list(map(lambda x: x.replace('TARGET', ''), list(new.index)))
    ax.set_yticklabels(yticklabel)
    # print(xticklabel)

def fence(df, feature):
    q1 = df[feature].quantile(0.25)
    q3 = df[feature].quantile(0.75)
    upper = q3 + 1.5*(q3-q1)
    lower = q1 - 1.5*(q3-q1)
    return lower, upper

def cat_visual(df,feature):
    f, ax = plt.subplots(1,3,figsize = (5*3,4),gridspec_kw={'width_ratios':[1.5,2,2]})
    #1
    sns.barplot(df[feature].value_counts(),orient='h',ax=ax[0],palette='Set2',width = 0.5)
    ax[0].spines[['top','bottom','left','right']].set_visible(False)
    ax[0].tick_params(left=False)
    ax[0].xaxis.tick_top() 
    ax[0].set_xlabel('')
    #2
    ax[1].pie(x=df[df['TARGET']==1][feature].value_counts(),\
    labels=df[df['TARGET']==1][feature].value_counts().index,\
    startangle=90,autopct='%.2f%%') 
    #3
    ax[2].pie(x=df[df['TARGET']==0][feature].value_counts(),\
    labels=df[df['TARGET']==0][feature].value_counts().index,\
    startangle=90,autopct='%.2f%%') 
    
    #beautify
    ax[0].set_ylabel(feature+'\n'+'_'*30+'\n\n',fontweight = 'bold',fontsize=12)

    plt.tight_layout(w_pad=2,h_pad=2)


def num_visual(df,feature):
    """Visualize numeric, continuous feature"""
    corr = pd.DataFrame(df.corr()).fillna(0)
    f, ax = plt.subplots(2,3,figsize =(16,8)) #,gridspec_kw={'width_ratios':[1,2,2,2]}
    # calculate upper and lower fence 
    l,u = fence(df, feature)
    # closer look in to quartile, skewness, kurtosis, median, outliner
    # sns.boxplot(df[feature],ax=ax[1][0])
    # distribution of feature
    if u!= l:
        ax[0][0].hist(df[(df[feature]<u) & (df[feature]>l)][feature])
        # cross_tabulation with Target variable
        ax[0][1].hist(df[(df['TARGET']==1) & (df[feature]<u) & (df[feature]>l)][feature],color ='red',alpha = 0.3,)
        ax[0][2].hist(df[(df['TARGET']==0) & (df[feature]<u) & (df[feature]>l)][feature],color ='green',alpha = 0.4)
    else:
        ax[0][0].hist(df[feature])
        # cross_tabulation with Target variable
        ax[0][1].hist(df[(df['TARGET']==1)][feature],color ='red',alpha = 0.3,)
        ax[0][2].hist(df[(df['TARGET']==0)][feature],color ='green',alpha = 0.4)


    # beautify
    # ax[0].set_ylabel(feature+'\n'+'_'*35+'\n\n',fontweight = 'bold',fontsize=12)
    for i in range(3):
            ax[0][i].spines[['top','bottom','left','right']].set_color('grey')
            ax[0][i].tick_params(left=False, bottom = False)
            ax[0][i].grid(axis = 'y')

    gs = plt.GridSpec(2,12,wspace = 0.3)
    for ax in ax[1,:]:
        ax.remove()
    axnew = f.add_subplot(gs[1,5:11])
    visual_corr(corr,feature,5,axnew)
    axnew2 = f.add_subplot(gs[1,1:3])
    sns.boxplot(df[feature],ax=axnew2)
    axnew2.spines[['top','bottom','left','right']].set_color('grey')
    axnew2.tick_params(left=False, bottom = False)
    f.tight_layout(h_pad=3)