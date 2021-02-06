#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 18:08:05 2020

@author: olesiakhrapunova
"""

import pandas as pd

def resampling(train, times):
    # Class count
    count_label_1, count_label_0, count_label_3, count_label_2, count_label_7, count_label_4, count_label_6, count_label_5 = train.label.value_counts()

    # Divide by class
    train_label_0 = train[train['label'] == 0]
    train_label_1 = train[train['label'] == 1]
    train_label_2 = train[train['label'] == 2]
    train_label_3 = train[train['label'] == 3]
    train_label_4 = train[train['label'] == 4]
    train_label_5 = train[train['label'] == 5]
    train_label_6 = train[train['label'] == 6]
    train_label_7 = train[train['label'] == 7]
    
    #resample the training dataset to make it more balanced in terms of labels

    #undersample 1,0,3
    #label_1_under = train_label_1.sample(count_label_0)
    #label_0_under = train_label_0.sample(count_label_2)
    #label_3_under = train_label_3.sample(count_label_2)

    #oversample 7,6,5,4
    #label_7_over = train_label_7.sample(count_label_2, replace=True)
    label_6_over = train_label_6.sample(count_label_6*times, replace=True)
    label_5_over = train_label_5.sample(count_label_5*times, replace=True)
    label_4_over = train_label_4.sample(count_label_4*times, replace=True)

    train_sample = pd.concat([train_label_0, train_label_1, train_label_2, train_label_3, label_4_over, label_5_over, label_6_over, train_label_7], axis=0)

    return train_sample