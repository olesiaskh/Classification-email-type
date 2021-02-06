#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 21 13:07:10 2020

@author: olesiakhrapunova
"""


def tld_clean(data):
    #update org and tld elements
    ex_org=[]
    exceptions = ['org','co','gov','ac','net']
    for index,row in data.iterrows():
        element = row['tld']
        if type(element) != float:
            splitted = element.split(".")
            if len(splitted) == 2:
                if splitted[0] not in exceptions:
                    data.loc[index,'tld'] = splitted[1]
                    first_org=row['org']
                    ex_org.append(first_org)
                    data.loc[index,'org']=splitted[0]
                else:
                    ex_org.append(None)
      
            elif len(splitted) > 2:
                if splitted[-2] not in exceptions:
                    data.loc[index,'tld'] = splitted[-1]
                    first_org=row['org']
                    ex_org.append(first_org)
                    merged_org = '.'.join(splitted[:-2])
                    data.loc[index,'org'] = merged_org
                else:
                     merged_tld = '.'.join(splitted[-2:-1])
                     data.loc[index,'tld'] = merged_tld
                     first_org=row['org']
                     ex_org.append(first_org)
                     merged_org = '.'.join(splitted[:-3])
                     data.loc[index,'org'] = merged_org
            else:
                ex_org.append(None)
        else:
            data.loc[index,'tld']=None
            ex_org.append(None)
         
    #insert the new column
    data.insert(2,"ex_org",ex_org)
    
    return data


def mailtype_clean(df):
    df['mail_type'] = df['mail_type'].replace(['Multipart/Alternative'],'multipart/alternative')
    df['mail_type'] = df['mail_type'].replace(['Multipart/Mixed'],'multipart/mixed')
    df['mail_type'] = df['mail_type'].replace(['Text/Html'],'text/html')
    df['mail_type'] = df['mail_type'].replace(['text/html '],'text/html')
    
    return df




