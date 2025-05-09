
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime, date, time, timedelta
import json

def load_data(data):

    if data == "train":
        # Load data
        df_train = pd.read_csv("data/Train.csv")

        df_train["STA"] = df_train['STA'].str.replace(".", ":")
        df_train["STA"] = pd.to_datetime(df_train["STA"])
        df_train["STD"] = pd.to_datetime(df_train["STD"])
        df_train["DATOP"] = pd.to_datetime(df_train["DATOP"], format='%Y-%m-%d')

        df_train["airline_code"] = df_train['FLTID'].str.split(' ').str[0]
        df_train["flt_num"] = df_train['FLTID'].str.split(' ').str[1]
        df_train["AC_num"] = df_train['AC'].str.split(' ').str[1]
        df_train["STD_year"] = df_train['STD'].dt.year
        df_train["STD_month"] = df_train['STD'].dt.month
        df_train["STD_day"] = df_train['STD'].dt.day_of_week
        df_train["STD_hour"] = df_train['STD'].dt.hour
        df_train["STA_hour"] = df_train['STA'].dt.hour
        df_train["DURATION"] = (df_train.STA - df_train.STD) / timedelta(minutes = 1)
        df_train["plane"] = df_train['AC'].str.split(' ').str[1].str[:3]
        datop_dep_counts = df_train.groupby(['DATOP', 'DEPSTN']).size() # Group by DATOP and DEPSTN and calculate the occurrences
        df_train['DATOP_DEP_count'] = df_train.set_index(['DATOP', 'DEPSTN']).index.map(datop_dep_counts) # Map the counts to a new column in df_train

        datop_arr_counts = df_train.groupby(['DATOP', 'ARRSTN']).size() # Group by DATOP and ARRST and calculate the occurrences
        df_train['DATOP_ARR_count'] = df_train.set_index(['DATOP', 'ARRSTN']).index.map(datop_arr_counts) # Map the counts to a new column in df_train

        with open('Airports-master/airports.json', 'r') as f:
            data = json.load(f)

        airports = []
        for airport_code, details in data.items():
            record = {
                'iata': details.get('iata', ''),
                'country': details.get('country', ''),
                'lon': details.get('lon', None),
                'lat': details.get('lat', None)
            }
            airports.append(record)

        df_airports = pd.DataFrame(airports)

        df_train = df_train.merge(
            df_airports[['iata', 'lat', 'lon']],
            left_on='DEPSTN',
            right_on='iata',
            how='left'
        ).rename(columns={
            'lat': 'DEP_lat',
            'lon': 'DEP_lon',
        }).drop(columns=['iata'])  # Drop redundant 'iata' after merge

        df_train = df_train.merge(
            df_airports[['iata', 'lat', 'lon']],
            left_on='ARRSTN',
            right_on='iata',
            how='left'
        ).rename(columns={
            'lat': 'ARR_lat',
            'lon': 'ARR_lon',
        }).drop(columns=['iata'])  # Drop redundant 'iata' after second merge

        df_train.head()
        df_train.dropna(axis=0)

        # Define a function to categorize hours
        def categorize_hour(hour):
            if 6 <= hour < 12:
                return 'morning'
            elif 12 <= hour < 18:
                return 'noon'
            elif 18 <= hour < 24:
                return 'evening'
            else:
                return 'night'

        # Apply the function to categorize STD_hour and STA_hour
        df_train['STD_hour_category'] = df_train['STD_hour'].apply(categorize_hour)

        return df_train

    if data == "test":
        # Load data
        df_test = pd.read_csv("data/Test.csv")

        # Make dates numerical
        df_test.STD = pd.to_datetime(df_test.STD, format='%Y-%m-%d %H:%M:%S')
        df_test.STA = pd.to_datetime(df_test.STA, format='%Y-%m-%d %H.%M.%S')

        return df_test