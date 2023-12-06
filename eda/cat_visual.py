import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

file = ['dseb63_application_test','dseb63_application_train','dseb63_bureau',\
        'dseb63_bureau_balance', 'dseb63_credit_card_balance','dseb63_installments_payments',\
        'dseb63_POS_CASH_balance','dseb63_previous_application']
file_path = 'D:\\Năm 3 - HK1\\Visualize\\Ex\\final_project\\dseb63_final_project_DP_dataset\\dseb63_final_project_DP_dataset\\'


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
file_path = 'D:\\Năm 3 - HK1\\Visualize\\Ex\\final_project\\dseb63_final_project_DP_dataset\\dseb63_final_project_DP_dataset\\'

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
