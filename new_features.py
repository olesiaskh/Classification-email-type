def hour_day_month_utc(data):
    """
    Create new categorical features based on the date - hour, day, month and UTC timezone
    """
    hours=[]
    day=[]
    month=[]
    utc=[]
    dates = data[['date']].date
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

        data.insert(2,"Hour",hours)
        data.insert(3,"Day",day)
        data.insert(4,"Month",month)
        data.insert(5,"UTC",utc)
        
        
        data['UTC'] = data['UTC'].replace(['GMT'],'+0000')
        data['UTC'] = data['UTC'].replace(['-0000'],'+0000')
        
    return data


def weekend_month(data):
    """
    Create new features based on the date - month and weekend flag
    """
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



def orgtype(data):
    """
    Define which organizations fall within each organization type
    The assignment of type is based on which  
    """
    label_0 = set(data[data['label']==0]['org'].unique())
    label_1 = set(data[data['label']==1]['org'].unique())
    label_2 = set(data[data['label']==2]['org'].unique())
    label_3 = set(data[data['label']==3]['org'].unique())
    label_4 = set(data[data['label']==4]['org'].unique())
    label_5 = set(data[data['label']==5]['org'].unique())
    label_6 = set(data[data['label']==6]['org'].unique())
    label_7 = set(data[data['label']==7]['org'].unique())
    
    org_0 = label_0 - set.intersection(label_0,label_2) -  set.intersection(label_0,label_3) -  set.intersection(label_0,label_4)- set.intersection(label_0,label_5)- set.intersection(label_0,label_6)- set.intersection(label_0,label_7)
    org_1 = label_1 - set.intersection(label_0, label_1) - set.intersection(label_1,label_2) -  set.intersection(label_1,label_3) -  set.intersection(label_1,label_4)- set.intersection(label_1,label_5)- set.intersection(label_1,label_6)- set.intersection(label_1,label_7)
    org_2 = label_2 - set.intersection(label_2,label_4)
    org_3 = label_3 
    org_4 = label_4 
    org_5 = label_5 - set.intersection(label_5, label_3)
    org_6 = label_6 - set.intersection(label_6, label_4)
    org_7 = label_7 

    return org_0, org_1, org_2, org_3, org_4, org_5, org_6, org_7
    
def org_encode(data,org_0, org_1, org_2, org_3, org_4, org_5, org_6, org_7):
    
    for index, row in data.iterrows():
        if data.loc[index,'org'] == data.loc[index,'org']:
            if data.loc[index,'org'] in org_0:
                data.loc[index,'org_update']=1
            else:
                data.loc[index,'org_update']=0
            if data.loc[index,'org'] in org_1:
                data.loc[index,'org_personal']=1
            else:
                data.loc[index,'org_personal']=0
            if data.loc[index,'org'] in org_2:
                data.loc[index,'org_promo']=1
            else:
                data.loc[index,'org_promo']=0
            if data.loc[index,'org'] in org_3:
                data.loc[index,'org_prof']=1
            else:
                data.loc[index,'org_prof']=0      
            if data.loc[index,'org'] in org_4:
                data.loc[index,'org_com']=1
            else:
                data.loc[index,'org_com']=0      
            if data.loc[index,'org'] in org_5:
                data.loc[index,'org_travel']=1
            else:
                data.loc[index,'org_travel']=0
            if data.loc[index,'org'] in org_6:
                data.loc[index,'org_spam']=1
            else:
                data.loc[index,'org_spam']=0
            if data.loc[index,'org'] in org_7:
                data.loc[index,'org_social']=1
            else:
                data.loc[index,'org_social']=0
        else:
            data.loc[index,'org_update']=0
            data.loc[index,'org_personal']=0
            data.loc[index,'org_promo']=0 
            data.loc[index,'org_prof']=0  
            data.loc[index,'org_com']=0 
            data.loc[index,'org_travel']=0 
            data.loc[index,'org_spam']=0
            data.loc[index,'org_social']=0
            
    return data        
