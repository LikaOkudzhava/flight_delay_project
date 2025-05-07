
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime, date, time, timedelta

def load_data(data):

    if data == "train":
        # Load data
        df_train = pd.read_csv("data/Train.csv")

        # Make dates numerical
        df_train.STD = pd.to_datetime(df_train.STD, format='%Y-%m-%d %H:%M:%S')
        df_train.STA = pd.to_datetime(df_train.STA, format='%Y-%m-%d %H.%M.%S')

        return df_train
    
    if data == "test":
        # Load data
        df_test = pd.read_csv("data/Test.csv")

        # Make dates numerical
        df_test.STD = pd.to_datetime(df_test.STD, format='%Y-%m-%d %H:%M:%S')
        df_test.STA = pd.to_datetime(df_test.STA, format='%Y-%m-%d %H.%M.%S')

        return df_test