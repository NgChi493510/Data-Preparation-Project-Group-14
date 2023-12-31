import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

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
    ord = df[[feature,'TARGET']].value_counts().unstack().fillna(0)
    ord['total'] = ord.sum(axis = 1)
    ord.sort_values('total',ascending = False,inplace=True)
    hue_order = ord.index.tolist()
    #ord.drop('order',axis= 1,inplace=True)
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
    sns.barplot(pd.Series([100]*df[feature].nunique(),index=df[feature].value_counts(sort=True).index),\
                orient='h',ax=axnew2,color= 'red',width = 0.5,alpha=0.2, label='1')   
    sns.barplot(df[df['TARGET']==0][feature].value_counts() / df[feature].value_counts() *100,\
                orient='h',ax=axnew2,color= 'red',width = 0.5,alpha = 0.4, label='0')
    axnew2.spines[['top','bottom','left','right']].set_visible(False)
    axnew2.xaxis.tick_top() 
    axnew2.tick_params(left=False, bottom = False,top = False)

    axnew2.grid(axis = 'x')
    axnew2.set_xlabel('percent')
    axnew2.set_ylabel('')
    axnew2.set_yticklabels('')
    axnew2.legend(loc = 'upper right')

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
