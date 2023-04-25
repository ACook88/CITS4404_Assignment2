import os
import json
import pandas as pd
import requests

# Code modified from GTP output
def get_kraken_data(pair='XBTAUD', interval=1440, since=1609430400):
    # retrieve data
    url = f"https://api.kraken.com/0/public/OHLC?pair={pair}&since={since}&interval={interval}"
    resp = requests.get(url)
    data = resp.json()['result'][pair]

    # create pandas DataFrame
    df = pd.DataFrame(data, columns=['unixtimestap', 'open', 'high', 'low', 'close', 'vwap', 'volume', 'count'])
    df = df.astype(float)

    # create data directory if it doesn't exist
    if not os.path.exists('data'):
        os.mkdir('data')

    # save data as JSON and CSV
    df.to_json('data/kraken_data.json', orient='records', indent=2)
    df.to_csv('data/kraken_data.csv')

    return df
