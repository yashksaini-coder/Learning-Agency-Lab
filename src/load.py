import pandas as pd

class PATHS:
    train_path = 'data/train.csv'
    test_path = 'data/test.csv'
    sub_path = 'data/sample_submission.csv'
    
def load_train():
    train = pd.read_csv(PATHS.train_path)
    return train

def load_test():
    test = pd.read_csv(PATHS.test_path)
    return test

def load_submission():
    submission = pd.read_csv(PATHS.sub_path)
    return submission