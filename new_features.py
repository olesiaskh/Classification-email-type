
import pandas as pd
#create day of the week, hour, and month elements



def weekend_month(data):
    weekend = ['Sat,','Sun,']
    month = []
    for index,row in data.iterrows():
        element = data.loc[index,'date']
        splited = element.split(" ")
        if splited[0] in weekend:
            data.loc[index,'weekend'] = 1
        else:
            data.loc[index,'weekend'] = 0
        if len(splited)>=3:
            if len(splited[2])==3:
                month.append(splited[2])
            else: 
                month.append('None')
        else:
          month.append('None')
      
    data.insert(2,"month", month)

    return data

def extra(data):
    values = ['email', 'news', 'accounts', 'notifications', 'kaggle']
    for value in values:
        for index,row in data.iterrows():
            if data.loc[index,'ex_org'] == value:
                data.loc[index,value] = 1
            else:
                data.loc[index,value] = 0
    return data


def orgtype(train_df):
    
    #define org belonings
    label_0 = set(train_df[train_df['label']==0]['org'].unique())
    label_1 = set(train_df[train_df['label']==1]['org'].unique())
    label_2 = set(train_df[train_df['label']==2]['org'].unique())
    label_3 = set(train_df[train_df['label']==3]['org'].unique())
    label_4 = set(train_df[train_df['label']==4]['org'].unique())
    label_5 = set(train_df[train_df['label']==5]['org'].unique())
    label_6 = set(train_df[train_df['label']==6]['org'].unique())
    label_7 = set(train_df[train_df['label']==7]['org'].unique())
    
    org_0 = label_0 - set.intersection(label_0,label_2) -  set.intersection(label_0,label_3) -  set.intersection(label_0,label_4)- set.intersection(label_0,label_5)- set.intersection(label_0,label_6)- set.intersection(label_0,label_7)
    org_1 = label_1 - set.intersection(label_0, label_1) - set.intersection(label_1,label_2) -  set.intersection(label_1,label_3) -  set.intersection(label_1,label_4)- set.intersection(label_1,label_5)- set.intersection(label_1,label_6)- set.intersection(label_1,label_7)
    org_2 = label_2 - set.intersection(label_2,label_4)
    org_3 = label_3 
    org_4 = label_4 
    org_5 = label_5 - set.intersection(label_5, label_3)
    org_6 = label_6 - set.intersection(label_6, label_4)
    org_7 = label_7 


    return org_0, org_1, org_2, org_3, org_4, org_5, org_6, org_7
    
def org_encode(train_df,org_0, org_1, org_2, org_3, org_4, org_5, org_6, org_7):
    
    for index, row in train_df.iterrows():
        if train_df.loc[index,'org'] == train_df.loc[index,'org']:
            if train_df.loc[index,'org'] in org_0:
                train_df.loc[index,'org_update']=1
            else:
                train_df.loc[index,'org_update']=0
            if train_df.loc[index,'org'] in org_1:
                train_df.loc[index,'org_personal']=1
            else:
                train_df.loc[index,'org_personal']=0
            if train_df.loc[index,'org'] in org_2:
                train_df.loc[index,'org_promo']=1
            else:
                train_df.loc[index,'org_promo']=0
            if train_df.loc[index,'org'] in org_3:
                train_df.loc[index,'org_prof']=1
            else:
                train_df.loc[index,'org_prof']=0      
            if train_df.loc[index,'org'] in org_4:
                train_df.loc[index,'org_com']=1
            else:
                train_df.loc[index,'org_com']=0      
            if train_df.loc[index,'org'] in org_5:
                train_df.loc[index,'org_travel']=1
            else:
                train_df.loc[index,'org_travel']=0
            if train_df.loc[index,'org'] in org_6:
                train_df.loc[index,'org_spam']=1
            else:
                train_df.loc[index,'org_spam']=0
            if train_df.loc[index,'org'] in org_7:
                train_df.loc[index,'org_social']=1
            else:
                train_df.loc[index,'org_social']=0
        else:
            train_df.loc[index,'org_update']=0
            train_df.loc[index,'org_personal']=0
            train_df.loc[index,'org_promo']=0 
            train_df.loc[index,'org_prof']=0  
            train_df.loc[index,'org_com']=0 
            train_df.loc[index,'org_travel']=0 
            train_df.loc[index,'org_spam']=0
            train_df.loc[index,'org_social']=0
    return train_df        



def date_utc(df):
    hours=[]
    day=[]
    month=[]
    utc=[]
    dates = df[['date']].date
    for element in dates:
        splited = element.split(" ")
        if len(splited)>=6:
            hrs = splited[4].split(":")
            hr= hrs[0]
            u = splited[5]
            utc.append(u)
            if len(hr)==2:
              hours.append(hr)
            else: 
              hours.append(None)
        elif len(splited)>=4:
            utc.append(None)
            hrs = splited[3].split(":")
            hr= hrs[0]
            if len(hr)==2:
              hours.append(hr)
            else: 
              hours.append(None)
        else:
            hours.append(None)
            utc.append(None)
  
        d = splited[0]
        if len(d)==4:
            day.append(d[:-1])
        else:
            day.append(None)
        
        if len(splited)>=3:
            if len(splited[2])==3:
              month.append(splited[2])
            else: 
              month.append(None)
        else:
            month.append(None)
        #insert the new columns

        df.insert(2,"Hour",hours)
        df.insert(3,"Day",day)
        df.insert(4,"Month",month)
        df.insert(5,"UTC",utc)
        
        
        df['UTC'] = df['UTC'].replace(['GMT'],'+0000')
        df['UTC'] = df['UTC'].replace(['-0000'],'+0000')
    return df

