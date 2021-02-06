#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 29 17:14:14 2020

@author: olesiakhrapunova
"""

import pandas as pd
import numpy as np

from sklearn.preprocessing import OneHotEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report, f1_score
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.decomposition import PCA


from data_clean import tld_clean, mailtype_clean
from new_features import hour_day_month_utc, extra
from resampling import resampling
from encoder import encode_train_test


#load the data
data_train = pd.read_csv('train.csv', index_col=0)
data_test = pd.read_csv('test.csv', index_col=0)
print('Data loaded')

#get only the values without duplicates and first instance of a duplicate
data_test_nodupl = data_test.drop_duplicates(keep = False)
data_test_dupl = data_test.merge(data_test_nodupl,indicator = True, how='left').loc[lambda x : x['_merge']!='both']
data_test_dupl = data_test_dupl.drop('_merge', axis=1)
data_test_dupl = data_test_dupl.sort_values('date')
data_test_dupl_s = data_test_dupl.reset_index()



#remove duplicates and reset index
data_train = data_train.drop_duplicates()
data_train = data_train.reset_index()
print('Full duplicates removed')


#combine duplicates and encode labels
labels = data_train[['label']]
feat_enc = OneHotEncoder()
labels_featurized = pd.DataFrame(feat_enc.fit_transform(labels).toarray(), columns = ['Label-0', 'Label-1', 'Label-2', 'Label-3', 'Label-4', 'Label-5', 'Label-6', 'Label-7'])
data_train = data_train.join(labels_featurized)
grouped = data_train.groupby(['date','org','tld', 'ccs', 'bcced', 'mail_type', 'images', 'urls', 'salutations', 'designation', 'chars_in_subject', 'chars_in_body'], as_index=False)
data_train = grouped.sum()
print('Feature duplictaes combined, labels encoded')


#clean the data
data_train = mailtype_clean(tld_clean(data_train))
data_test_dupl_s = mailtype_clean(tld_clean(data_test_dupl_s))
print('Data cleaned')

#create new features
data_train = hour_day_month_utc(data_train)
data_train = extra(data_train)
data_test_dupl_s = hour_day_month_utc(data_test_dupl_s)
data_test_dupl_s = extra(data_test_dupl_s)
print('Features created')

#resample the data
#data_sampled = resampling(data_train, 5)
#print('Data resampled')
data_sampled = data_train

#choose numerical features to include
train_x = data_sampled[['chars_in_subject','images', 'urls', 'ccs']]
test_x = data_test_dupl_s[['chars_in_subject','images', 'urls', 'ccs']]
print('Numerical features selected')

#choose categorical features to include
train_x_cat = data_sampled[['org','mail_type']]
train_x_cat = train_x_cat.fillna(value='None')
test_x_cat = data_test_dupl_s[['org','mail_type']]
test_x_cat = test_x_cat.fillna(value='None')
print('Categorical features selected')



#encode categorical variables
test = test_x_cat
train= train_x_cat
both = pd.concat([test, train])
feat_enc2 = OneHotEncoder()
feat_enc2.fit(both)
test_x_featurized = pd.DataFrame(feat_enc2.transform(test).toarray())
train_x_featurized = pd.DataFrame(feat_enc2.transform(train).toarray())
print('Categorical features encoded')

#merge numerical and categorical data
train_x = train_x.join(train_x_featurized)
test_x = test_x.join(test_x_featurized)
print('Data merged')


#get labels
train_y = data_train[['Label-0', 'Label-1', 'Label-2', 'Label-3', 'Label-4', 'Label-5', 'Label-6', 'Label-7']]
print('Y values specified')


#fit your model and perform cross-validation
clf = DecisionTreeClassifier(max_depth=13)
clf.fit(train_x, train_y)
scores = cross_val_score(clf, train_x, train_y, cv = 5)
print('Model trained')
print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))


#make predictions from the given model
pred_y = clf.predict(test_x)
pred_df = pd.DataFrame(pred_y)
#adjust for final submission
for index, row in pred_df.iterrows():
    if index % 2 == 0:
        for column in pred_df:
            if pred_df.loc[index,column]==1:
                pred_df.loc[index,'label']=column
                break
    else:
        for column in reversed(pred_df.columns):
            if pred_df.loc[index,column]==1:
                pred_df.loc[index,'label']=column
                break

#get original indexes
merged=data_test_dupl_s.merge(pred_df, left_index=True, right_index=True)
merged_final=merged[['index','label']]
merged_final=merged_final.fillna(value=1)
merged_final=merged_final.set_index('index',drop=True)
merged_final= merged_final.fillna(value=1)
# Save results to submission file
merged_final.to_csv("multilabel_submission.csv", index=True, index_label='Id')


