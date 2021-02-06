from sklearn.preprocessing import OneHotEncoder
import pandas as pd



def encode_train_test(test, train):
    feat_enc = OneHotEncoder()
    both = pd.concat([test, train])
    feat_enc.fit(both)
    test_x_featurized = pd.DataFrame(feat_enc.transform(test).toarray())
    train_x_featurized = pd.DataFrame(feat_enc.transform(train).toarray())
    return test_x_featurized, train_x_featurized

def encode_train(train):
    feat_enc = OneHotEncoder(handle_unknown = 'ignore' )
    feat_enc.fit(train)
    train_x_featurized = pd.DataFrame(feat_enc.transform(train).toarray())
    return train_x_featurized
    
