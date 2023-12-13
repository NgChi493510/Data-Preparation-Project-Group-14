import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

file = ['dseb63_application_test','dseb63_application_train','dseb63_bureau',\
        'dseb63_bureau_balance', 'dseb63_credit_card_balance','dseb63_installments_payments',\
        'dseb63_POS_CASH_balance','dseb63_previous_application']
file_path = 'C:/Users/Dell/Documents/Data Preparation Project/dataset/'
# df = pd.read_csv(file_path + file[1]+'.csv',index_col='Unnamed: 0')



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
                ax.text(x= l/10, y =i+0.145, s = 'Correlate with TARGET')
            else:
                ax.text(x= t+l/13, y =i+0.145, s ='Correlate with TARGET')

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
def num_visual(df,feature, kde = False):
    """Visualize numeric, continuous feature"""
    f, ax = plt.subplots(2,3,figsize =(16,8)) #gridspec_kw={'width_ratios':[1,2,2,2]}
    # calculate upper and lower fence 
    l,u = fence(df, feature)

    # closer look in to quartile, skewness, kurtosis, median, outliner
    # distribution of feature
    v0 = df[(df[feature]<u) & (df[feature]>l)][feature]
    v1 = df[(df['TARGET']==1) & (df[feature]<u) & (df[feature]>l)][feature]
    v2 = df[(df['TARGET']==0) & (df[feature]<u) & (df[feature]>l)][feature]
    if df[feature].nunique()>10:
        if u!= l:
            if kde == False:
                ax[0][0].hist(v0)
            # cross_tabulation with Target variable
                ax[0][1].hist(v1,color ='red',alpha = 0.3,)
                ax[0][2].hist(v2,color ='green',alpha = 0.4)
            else:
                sns.histplot(v0,ax = ax[0][0],kde = True,bins=15,edgecolor ='white')    
            # cross_tabulation with Target variable
                sns.histplot(v1, color ='red',alpha = 0.3,ax = ax[0][1],kde = True,bins=15,edgecolor ='white') 
                sns.histplot(v2, color ='green',alpha = 0.4,ax = ax[0][2],kde = True,bins=15,edgecolor ='white') 
        else:
            ax[0][0].hist(df[feature],edgecolor ='white')
            # # cross_tabulation with Target variable
            ax[0][1].hist(df[(df['TARGET']==1)][feature],color ='red',alpha = 0.3,edgecolor ='white')
            ax[0][2].hist(df[(df['TARGET']==0)][feature],color ='green',alpha = 0.4,edgecolor ='white') 

    else:
        ax[0][0].bar(df[feature].value_counts().index,df[feature].value_counts().values,\
                     tick_label = df[feature].value_counts().index)

        ax[0][1].bar(df[(df['TARGET']==1)][feature].value_counts().index,\
                     df[(df['TARGET']==1)][feature].value_counts().values,color ='red',alpha = 0.3,\
                        tick_label = df[(df['TARGET']==1)][feature].value_counts().index)
        
        ax[0][2].bar(df[(df['TARGET']==0)][feature].value_counts().index,\
                     df[(df['TARGET']==0)][feature].value_counts().values,color ='green',alpha = 0.4,\
                     tick_label = df[(df['TARGET']==0)][feature].value_counts().index)

    ax[0][1].set_xlim(ax[0][0].get_xlim())
    ax[0][2].set_xlim(ax[0][0].get_xlim())
    ax[0][0].legend(['Both'])
    ax[0][1].legend(['Non-Defaulter'])
    ax[0][2].legend(['Defaulter'])

    # beautify
    for i in range(3):
            ax[0][i].spines[['top','bottom','left','right']].set_color('grey')
            ax[0][i].tick_params(left=False, bottom = False)
            ax[0][i].grid(axis = 'y')
            ax[0][i].set_xlabel('')
            ax[0][i].set_ylabel('')
    ax[0][1].set_title('_'*(len(feature)+12)+'\n\n'+'|| '+feature+' ||'+'\n'+'_'*140+'\n\n',fontweight = 'bold',fontsize=12)
    
    gs = plt.GridSpec(2,12,wspace = 0.3)
    for ax in ax[1,:]:
        ax.remove()
    axnew = f.add_subplot(gs[1,5:11])

    visual_corr(corr ,feature,5,axnew)
    axnew2 = f.add_subplot(gs[1,1:3])
    sns.boxplot(df[feature],ax=axnew2)
    axnew2.spines[['top','bottom','left','right']].set_color('grey')
    axnew2.tick_params(left=False, bottom = False)
    axnew2.set_ylabel('')
    f.tight_layout(h_pad=3)


def cat_visual2(df,feature):
    f, ax = plt.subplots(1,3,figsize = (5*3,4),gridspec_kw={'width_ratios':[1.5,2,2]})
    #1
    sns.barplot(df[feature].value_counts(dropna=False),orient='h',ax=ax[0],palette='Set2',width = 0.5)
    ax[0].spines[['top','bottom','left','right']].set_visible(False)
    ax[0].tick_params(left=False)
    ax[0].xaxis.tick_top() 
    ax[0].set_xlabel('')
    #2
    ax[1].pie(x=df[df['TARGET']==1][feature].value_counts(dropna=False),\
    labels=df[df['TARGET']==1][feature].value_counts(dropna=False).index,\
    startangle=90,autopct='%.2f%%') 
    #3
    ax[2].pie(x=df[df['TARGET']==0][feature].value_counts(dropna=False),\
    labels=df[df['TARGET']==0][feature].value_counts(dropna=False).index,\
    startangle=90,autopct='%.2f%%') 

    #beautify
    ax[0].set_ylabel(feature+'\n'+'_'*(len(feature)+10)+'\n\n',fontweight = 'bold',fontsize=12)

    plt.tight_layout(w_pad=2,h_pad=2)

def cat_visual(df,feature):
    if df[feature].nunique() < 3:
        f, ax = plt.subplots(2,3,figsize = (5*3,df[feature].nunique()*2.5))
    elif df[feature].nunique() < 5:
        f, ax = plt.subplots(2,3,figsize = (5*3,df[feature].nunique()*1.5))
    elif df[feature].nunique() < 20 :
        f, ax = plt.subplots(2,3,figsize = (5*3,df[feature].nunique()/1.2))
    else:
        f, ax = plt.subplots(2,3,figsize = (5*3,df[feature].nunique()/1.6))
    gs = plt.GridSpec(2,3)
    f.delaxes(ax[1][1])
    f.delaxes(ax[1][0])
    axnew = f.add_subplot(gs[:,0])
    axnew2 = f.add_subplot(gs[:,1])
    f.delaxes(ax[0][1])
    f.delaxes(ax[0][0])

    #1
    ord = df[[feature,'TARGET']].value_counts(normalize=True).unstack().fillna(0)
    ord['order'] = ord.sum(axis = 1)
    ord.sort_values('order',ascending = False,inplace=True)
    hue_order = ord.index.tolist()
    ord.drop('order',axis= 1,inplace=True)
    sns.heatmap(ord, annot = True, cmap = 'Greens',fmt = '.2f',ax =axnew,cbar = False)
    

# Create heatmap
    axnew.set_yticklabels(axnew.get_yticklabels(),rotation =360,horizontalalignment =  'center',fontweight='bold')
    axnew.tick_params(bottom = False, left = False,right = False)
    axnew.xaxis.tick_top() 
    axnew.yaxis.tick_right()
    axnew.tick_params(bottom = False, left = False,right = False)
    l,u = (axnew.get_xlim())
    axnew.set_xlim(l,u+(u-l)/2)
    axnew.set_ylabel('')
    axnew.set_xlabel('')

    #2
    sns.barplot(df[feature].value_counts(),\
                orient='h',ax=axnew2,width = 0.5,alpha=0.8)   
    sns.barplot(df[df['TARGET']==0][feature].value_counts(),\
                orient='h',ax=axnew2,color= 'red',width = 0.5,alpha = 0.8)
    axnew2.spines[['top','bottom','left','right']].set_visible(False)
    axnew2.xaxis.tick_top() 
    axnew2.tick_params(left=False, bottom = False,top = False)

    axnew2.grid(axis = 'x')
    axnew2.set_xlabel('')
    axnew2.set_yticklabels('')

    #3
    sns.countplot(data= df[df['TARGET']==1], x ='TARGET', hue = feature ,ax= ax[0][2],\
                  stat = 'percent',palette='Set3',edgecolor = 'white',hue_order=hue_order,legend=False)
    sns.countplot(data= df[df['TARGET']==0], x ='TARGET', hue = feature ,ax= ax[1][2],\
                  stat = 'percent',palette='Set3',edgecolor = 'white',hue_order=hue_order,legend=False)
    
    ax[0][2].legend(hue_order,loc = 'upper right')

    for i in range(2):
        ax[i][2].spines[['top','bottom','left','right']].set_color('grey')
        ax[i][2].tick_params(left=False, bottom = False,top = False)
        ax[i][2].set_xlabel('')
 
    #beautify
    # axnew.set_ylabel(feature+'\n'+'_'*30+'\n\n',fontweight = 'bold',fontsize=12)
    axnew2.set_title('_'*(len(feature)+12)+'\n\n'+'|| '+feature+' ||'+'\n'+'_'*140+'\n\n',fontweight = 'bold',fontsize=12)
    plt.tight_layout(w_pad=2)




def extract_mean(x,on,prefix):
    y = x.groupby(on, as_index=False).mean().add_prefix(prefix) 
    return y
# file_path = 'C:/Users/Dell/Documents/Data Preparation Project/dataset/' 


app_train = pd.read_csv(file_path + "dseb63_application_train.csv", index_col='Unnamed: 0')
app_test = pd.read_csv(file_path + "dseb63_application_test.csv", index_col='Unnamed: 0')
bureau = pd.read_csv(file_path + "dseb63_bureau.csv")
bureau_balance = pd.read_csv(file_path + "dseb63_bureau_balance.csv")
POS_CASH_balance = pd.read_csv(file_path + "dseb63_POS_CASH_balance.csv")
previous_application = pd.read_csv(file_path + "dseb63_previous_application.csv")
credit_card_balance = pd.read_csv(file_path + "dseb63_credit_card_balance.csv")
installments_payments = pd.read_csv(file_path + "dseb63_installments_payments.csv")

data = pd.concat([app_train,app_test], ignore_index=True)


previous_loan_counts = bureau.groupby('SK_ID_CURR', as_index=False)['SK_ID_BUREAU'].count().rename(columns = {'SK_ID_BUREAU': 'PREVIOUS_LOANS_COUNT'})
data = data.merge(previous_loan_counts, on = 'SK_ID_CURR', how = 'left')


bureau_bal_mean = extract_mean(bureau_balance,'SK_ID_BUREAU','BUR_BAL_MEAN_')
bureau_bal_mean = bureau_bal_mean.rename(columns = {'BUR_BAL_MEAN_SK_ID_BUREAU' : 'SK_ID_BUREAU'})
bureau = bureau.merge(bureau_bal_mean, on = 'SK_ID_BUREAU', how = 'left')
bureau.drop('SK_ID_BUREAU', axis = 1, inplace = True)


bureau_mean_values = extract_mean(bureau,'SK_ID_CURR','PREV_BUR_MEAN_')
bureau_mean_values = bureau_mean_values.rename(columns = {'PREV_BUR_MEAN_SK_ID_CURR' : 'SK_ID_CURR'})
data = data.merge(bureau_mean_values, on = 'SK_ID_CURR', how = 'left')

credit_card_balance.drop('SK_ID_CURR', axis = 1, inplace = True)
installments_payments.drop('SK_ID_CURR', axis = 1, inplace = True)
POS_CASH_balance.drop('SK_ID_CURR', axis = 1, inplace = True)

previous_application_counts = previous_application.groupby('SK_ID_CURR', as_index=False)['SK_ID_PREV'].count().rename(columns = {'SK_ID_PREV': 'PREVIOUS_APPLICATION_COUNT'})
data = data.merge(previous_application_counts, on = 'SK_ID_CURR', how = 'left')

credit_card_balance_mean = extract_mean(credit_card_balance,'SK_ID_PREV','CARD_MEAN_')
credit_card_balance_mean = credit_card_balance_mean.rename(columns = {'CARD_MEAN_SK_ID_PREV' : 'SK_ID_PREV'})
previous_application = previous_application.merge(credit_card_balance_mean, on = 'SK_ID_PREV', how = 'left')


install_pay_mean = extract_mean(installments_payments,'SK_ID_PREV','INSTALL_MEAN_')
install_pay_mean = install_pay_mean.rename(columns = {'INSTALL_MEAN_SK_ID_PREV' : 'SK_ID_PREV'})
previous_application = previous_application.merge(install_pay_mean, on = 'SK_ID_PREV', how = 'left')

POS_mean = extract_mean(POS_CASH_balance,'SK_ID_PREV','POS_MEAN_')
POS_mean = POS_mean.rename(columns = {'POS_MEAN_SK_ID_PREV' : 'SK_ID_PREV'})
previous_application = previous_application.merge(POS_mean, on = 'SK_ID_PREV', how = 'left')


prev_appl_mean = extract_mean(previous_application,'SK_ID_CURR','PREV_APPL_MEAN_')
prev_appl_mean = prev_appl_mean.rename(columns = {'PREV_APPL_MEAN_SK_ID_CURR' : 'SK_ID_CURR'})

prev_appl_mean = prev_appl_mean.drop('PREV_APPL_MEAN_SK_ID_PREV', axis = 1) # we don't need this intermediate column any more
data = data.merge(prev_appl_mean, on = 'SK_ID_CURR', how = 'left')

corr = pd.DataFrame(data.corr()).fillna(0)
