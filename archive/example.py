import matplotlib.pyplot as plt
import mplfinance as mpf
import pandas as pd
import requests
import ta

# set up parameters
pair = 'XBTAUD'  # BTC/AUD pair
interval = 1440  # daily interval
since = 1609430400  # timestamp for start date (January 1, 2021)

# retrieve data
url = f"https://api.kraken.com/0/public/OHLC?pair={pair}&since={since}&interval={interval}"
resp = requests.get(url)
df = pd.DataFrame(resp.json()['result']['XBTAUD'])
df.columns = ['unixtimestap', 'open', 'high', 'low', 'close', 'vwap', 'volume', 'count']
df['close'] = df['close'].astype(float)
df['unixtimestap'] = pd.to_datetime(df['unixtimestap'], unit='s')
df = df.set_index('unixtimestap')
df = df.apply(pd.to_numeric)

# calculate technical analysis indicators
df['sma1'] = ta.trend.SMAIndicator(df['close'], window=1).sma_indicator()
df['sma2'] = ta.trend.SMAIndicator(df['close'], window=17).sma_indicator()
df['sma3'] = ta.trend.SMAIndicator(df['close'], window=58).sma_indicator()

# determine buy/sell flags
df['flag'] = ''
for i in range(1, len(df)):
    if df['sma1'][i] > df['sma2'][i] and df['sma1'][i-1] > df['sma3'][i-1]:
        df['flag'][i] = 'buy'
    elif df['sma1'][i] < df['sma2'][i] and df['sma1'][i-1] < df['sma3'][i-1]:
        df['flag'][i] = 'sell'

# create a copy of the dataframe with only the records that have a buy or sell flag
df_with_flags = df[df['flag'].isin(['buy', 'sell'])]

# write the new dataframe to a JSON file
df_with_flags.to_json('btc_aud_data.json', orient='records')

# plot the chart
mpf.plot(df, type='candle', style='charles', mav=(20, 50), volume=True,
         title='BTC/AUD', ylabel='Price (AUD)', ylabel_lower='Volume',
         figratio=(12, 8), addplot=[mpf.make_addplot(df['sma1']),
                                   mpf.make_addplot(df['sma2']),
                                   mpf.make_addplot(df['sma3'], panel=1)])

plt.show()
