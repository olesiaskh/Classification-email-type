def hour_day_month_utc(data):
    """Create hour, day, month and UTC features based on date.
    
    Parameters
    ----------
    data: dataframe
        Dataframe that includes 'date' column.
        
    Returns
    -------
    dataframe
        Dataframe with 4 new columns: 'Hour', 'Day', 'Month', 'UTC'.
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
    """Create weekend, month features based on date.
    
    Parameters
    ----------
    data: dataframe
        Dataframe that includes 'date' column.
        
    Returns
    -------
    dataframe
        Dataframe with 2 new columns: 'weekend', 'month'.
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
    """Define sets of organization types.
    
    Parameters
    ----------
    data: dataframe
        Dataframe that includes 'label' and 'org' columns.
        
    Returns
    -------
    org_update: set
        The organizations the belong to set 'update'.
    org_personal: set
        The organizations the belong to set 'personal'.
    org_promo: set
        The organizations the belong to set 'promotions'.
    org_prof: set
        The organizations the belong to set 'professional'.
    org_com: set
        The organizations the belong to set 'commercial'.
    org_travel: set
        The organizations the belong to set 'travel'.
    org_spam: set
        The organizations the belong to set 'spam'. 
    org_social: set
        The organizations the belong to set 'social'.
        
    Notes
    -------
    The type is based on target value that appears with a specific organization.
    If an organization is associated with multiple target values, the organization is
    assigned to the type that is least common in the dataset overall 
    (neither 'update', nor 'personal').
    """
    label_0 = set(data[data['label']==0]['org'].unique())
    label_1 = set(data[data['label']==1]['org'].unique())
    label_2 = set(data[data['label']==2]['org'].unique())
    label_3 = set(data[data['label']==3]['org'].unique())
    label_4 = set(data[data['label']==4]['org'].unique())
    label_5 = set(data[data['label']==5]['org'].unique())
    label_6 = set(data[data['label']==6]['org'].unique())
    label_7 = set(data[data['label']==7]['org'].unique())
    
    org_update = label_0 - set.intersection(label_0,label_2) -  set.intersection(label_0,label_3) -  set.intersection(label_0,label_4)- set.intersection(label_0,label_5)- set.intersection(label_0,label_6)- set.intersection(label_0,label_7)
    org_personal = label_1 - set.intersection(label_0, label_1) - set.intersection(label_1,label_2) -  set.intersection(label_1,label_3) -  set.intersection(label_1,label_4)- set.intersection(label_1,label_5)- set.intersection(label_1,label_6)- set.intersection(label_1,label_7)
    org_promo = label_2 - set.intersection(label_2,label_4)
    org_prof = label_3 
    org_com = label_4 
    org_travel = label_5 - set.intersection(label_5, label_3)
    org_spam = label_6 - set.intersection(label_6, label_4)
    org_social = label_7 

    return org_update, org_personal, org_promo, org_prof, org_com, org_travel, org_spam, org_social
    
def org_encode(data, org_update, org_personal, org_promo, org_prof, org_com, org_travel, org_spam, org_social):
    """Assign organization type to each email.
    
    Parameters
    ----------
    data: dataframe
        Dataframe that includes 'label' and 'org' columns.
    org_update: set
        The organizations the belong to set 'update'.
    org_personal: set
        The organizations the belong to set 'personal'.
    org_promo: set
        The organizations the belong to set 'promotions'.
    org_prof: set
        The organizations the belong to set 'professional'.
    org_com: set
        The organizations the belong to set 'commercial'.
    org_travel: set
        The organizations the belong to set 'travel'.
    org_spam: set
        The organizations the belong to set 'spam'. 
    org_social: set
        The organizations the belong to set 'social'.  
        
    Returns
    -------
    dataframe
        Dataframe with 8 new columns: 'org_update', 'org_personal', 
        'org_promo', 'org_prof', 'org_com', 'org_travel', 'org_spam', 
        'org_social' (all boolean).
    """
    for index, row in data.iterrows():
        if data.loc[index,'org'] == data.loc[index,'org']:
            if data.loc[index,'org'] in org_update:
                data.loc[index,'org_update']=1
            else:
                data.loc[index,'org_update']=0
                
            if data.loc[index,'org'] in org_personal:
                data.loc[index,'org_personal']=1
            else:
                data.loc[index,'org_personal']=0
                
            if data.loc[index,'org'] in org_promo:
                data.loc[index,'org_promo']=1
            else:
                data.loc[index,'org_promo']=0
                
            if data.loc[index,'org'] in org_prof:
                data.loc[index,'org_prof']=1
            else:
                data.loc[index,'org_prof']=0    
                
            if data.loc[index,'org'] in org_com:
                data.loc[index,'org_com']=1
            else:
                data.loc[index,'org_com']=0   
                
            if data.loc[index,'org'] in org_travel:
                data.loc[index,'org_travel']=1
            else:
                data.loc[index,'org_travel']=0
                
            if data.loc[index,'org'] in org_spam:
                data.loc[index,'org_spam']=1
            else:
                data.loc[index,'org_spam']=0
                
            if data.loc[index,'org'] in org_social:
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
