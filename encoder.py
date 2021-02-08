from sklearn.preprocessing import OneHotEncoder
import pandas as pd

def encode_train_test(train, test):
    """One-hot encodes train and test data
    
    Parameters
    ----------
    train: dataframe
        Dataframe with features from train data to be encoded.
    test: dataframe
        Dataframe with features from test data to be encoded.
        
    Returns
    -------
    train_x_featurized: dataframe
        Dataframe with encoded features from train data.
    test_x_featurized: dataframe
        Dataframe with encoded features from test data.
        
    Notes
    -----
    Features included in the two datasets should be identical.    
    """
    feat_enc = OneHotEncoder()
    both = pd.concat([train, test])
    feat_enc.fit(both)
    train_x_featurized = pd.DataFrame(feat_enc.transform(train).toarray())
    test_x_featurized = pd.DataFrame(feat_enc.transform(test).toarray())
    return train_x_featurized, test_x_featurized
