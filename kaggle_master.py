#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 17:40:51 2020

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
from sklearn.impute import SimpleImputer


from data_clean import tld_clean, mailtype_clean
from new_features import hour_day_month_utc, orgtype, org_encode
from resampling import resampling
from encoder import encode_train_test


#load the data
data_train = pd.read_csv('train.csv', index_col=0)
data_test = pd.read_csv('test.csv', index_col=0)
print('Data loaded')

#remove duplicates in train and reset index
data_train = data_train.drop_duplicates()
data_train = data_train.reset_index(drop=True)
print('Full duplicates removed')


#clean the data
data_train = mailtype_clean(tld_clean(data_train))
data_test = mailtype_clean(tld_clean(data_test))
print('Data cleaned')

#create new features
data_train = hour_day_month_utc(data_train)
data_test = hour_day_month_utc(data_test)

org_0, org_1, org_2, org_3, org_4, org_5, org_6, org_7 = orgtype(data_train)
data_train=org_encode(data_train, org_0, org_1, org_2, org_3, org_4, org_5, org_6, org_7)
data_test=org_encode(data_test, org_0, org_1, org_2, org_3, org_4, org_5, org_6, org_7)
print('Features created')

#resample the data
data_sampled = resampling(data_train, 5)
data_sampled = data_sampled.reset_index(drop=True)
print('Data resampled')

#choose numerical features to include
train_x = data_sampled[['chars_in_subject','images', 'urls', 'ccs', 'org_update','org_personal','org_promo','org_prof','org_com','org_travel','org_spam','org_social', 'salutations']]
test_x = data_test[['chars_in_subject','images', 'urls', 'ccs', 'org_update','org_personal','org_promo','org_prof','org_com','org_travel','org_spam','org_social','salutations']]
print('Numerical features selected')

#choose categorical features to include
train_x_cat = data_sampled[['org','mail_type']]
train_x_cat = train_x_cat.fillna(value='None')
test_x_cat = data_test[['org','mail_type']]
test_x_cat = test_x_cat.fillna(value='None')
print('Categorical features selected')

#replace null values in numerical with mean
imp = SimpleImputer(missing_values=np.nan, strategy='mean')
train_x = pd.DataFrame(imp.fit_transform(train_x),columns=['chars_in_subject','images', 'urls', 'ccs','org_update','org_personal','org_promo','org_prof','org_com','org_travel','org_spam','org_social', 'salutations'])
test_x = pd.DataFrame(imp.transform(test_x),columns=['chars_in_subject','images', 'urls', 'ccs','org_update','org_personal','org_promo','org_prof','org_com','org_travel','org_spam','org_social', 'salutations'])
print('Nulls replaced on numerical')

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


#create interaction features
train_x['org_updateXsalut']=train_x['org_update']*train_x['salutations']
train_x['org_personalXsalut']=train_x['org_personal']*train_x['salutations']
train_x['org_promoXsalut']=train_x['org_promo']*train_x['salutations']
train_x['org_profXsalut']=train_x['org_prof']*train_x['salutations']
train_x['org_comXsalut']=train_x['org_com']*train_x['salutations']
train_x['org_travelXsalut']=train_x['org_travel']*train_x['salutations']
train_x['org_spamXsalut']=train_x['org_spam']*train_x['salutations']
train_x['org_socialXsalut']=train_x['org_social']*train_x['salutations']

test_x['org_updateXsalut']=test_x['org_update']*test_x['salutations']
test_x['org_personalXsalut']=test_x['org_personal']*test_x['salutations']
test_x['org_promoXsalut']=test_x['org_promo']*test_x['salutations']
test_x['org_profXsalut']=test_x['org_prof']*test_x['salutations']
test_x['org_comXsalut']=test_x['org_com']*test_x['salutations']
test_x['org_travelXsalut']=test_x['org_travel']*test_x['salutations']
test_x['org_spamXsalut']=test_x['org_spam']*test_x['salutations']
test_x['org_socialXsalut']=test_x['org_social']*test_x['salutations']

#drop rows with null values
#train_x=train_x.dropna()
#print('Rows with NAs dropped')


#get labels
train_y = data_sampled['label'].values
#train_x = train_x.drop(['label'], axis=1)
print('Train datasets for x and y created')
 
#perform feature selection
#train_x_new = SelectKBest(chi2, k=1000).fit_transform(train_x, train_y)
#print('Feature selection completed')

#perform PCA
#pca = PCA(svd_solver='auto')
#train_x_pca = pca.fit_transform(train_x_new)
#print('PCA completed')

#fit your model and perform cross-validation
clf = DecisionTreeClassifier(max_depth=11)
clf.fit(train_x, train_y)
scores = cross_val_score(clf, train_x, train_y, cv = 5)
print('Model trained')
print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std() * 2))


#make predictions from the given model
pred_y = clf.predict(test_x)
# Save results to submission file
pred_df = pd.DataFrame(pred_y, columns=['label'])
pred_df.to_csv("unilabel_submission.csv", index=True, index_label='Id')


