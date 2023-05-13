import pandas as pd
import datetime

def pd_split(df,date_string):
    
    date_object = datetime.datetime.strptime(date_string, "%d-%m-%Y").replace(hour=8, minute=0, second=0)

    split_threshold = int(date_object.timestamp())

    # Split the DataFrame based on the "unixtimestamp" column
    df1 = df[df['unixtimestap'] < split_threshold]
    df2 = df[df['unixtimestap'] >= split_threshold]

    df1.to_csv('data/kraken_train.csv')
    df2.to_csv('data/kraken_validation.csv')
