import os
import json
import pandas as pd
import mplfinance as mpf
import ta

def generate_metrics_and_chart(filepath, sma1=20, sma2=50):
    # load Kraken data from JSON file
    df = pd.read_json(filepath)

    # set column names and data types
    df.columns = ['unixtimestap', 'open', 'high', 'low', 'close', 'vwap', 'volume', 'count']
    df['close'] = df['close'].astype(float)
    df['unixtimestap'] = pd.to_datetime(df['unixtimestap'], unit='s')
    df.set_index('unixtimestap', inplace=True)
    df = df.apply(pd.to_numeric)

    # calculate technical analysis indicators
    df['sma1'] = ta.trend.SMAIndicator(df['close'], window=sma1).sma_indicator()
    df['sma2'] = ta.trend.SMAIndicator(df['close'], window=sma2).sma_indicator()
    df['rsi'] = ta.momentum.RSIIndicator(df['close']).rsi()

    # plot the chart and save it as an image
    if not os.path.exists('graphs'):
        os.mkdir('graphs')
    mpf.plot(df, type='candle', style='charles', mav=(sma1, sma2), volume=True,
            title='BTC/AUD', ylabel='Price (AUD)', ylabel_lower='Volume',
            figratio=(12, 8), addplot=[mpf.make_addplot(df['sma1']),
                                    mpf.make_addplot(df['sma2']),
                                    mpf.make_addplot(df['rsi'], panel=1)],
            savefig='graphs/btc-aud.png')
