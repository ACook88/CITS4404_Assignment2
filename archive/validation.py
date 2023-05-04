import pandas as pd
import datetime

# Here is for the trading strategy, after we generate it, we can fill this part
class TEMA(bt.Strategy):
    params = dict(ema1=12,ema2=26,ema3=48)

    def __init__(self):

        self.small_p = bt.indicators.EMA(self.data.close, period=self.p.ema1)
        self.medium_p = bt.indicators.EMA(self.data.close, period=self.p.ema2)
        self.large_p = bt.indicators.EMA(self.data.close, period=self.p.ema3)
        
    def next(self):
        if self.small_p > self.medium_p and self.small_p > self.large_p:
            self.buy()
        elif self.small_p < self.medium_p and self.small_p < self.large_p:
            self.sell()


def read_datafile(data_file):
    df = pd.read_csv(data_file, index_col=1, parse_dates=True).sort_index()
    df.index = pd.to_datetime(df.index, unit='s')
    return df[["open","high","low","close"]].round(4)



def backtest(data_file,**strategy_params):
    # Read the data, here the 'data_file' would be the path of the csv file
    #data = pd.read_csv(data_file,index_col=1,parse_dates=True)
    test=read_datafile(data_file)
    # may need to do some data selection
    # create a Backtrader engine
    #print(data['unixtimestap'])
    cerebro = bt.Cerebro()

    # add the data into the engine
    data_feed = bt.feeds.PandasData(dataname=test)

    cerebro.adddata(data_feed)

    cerebro.broker.setcash(100.0)

    # Print out the starting conditions
    print(f"Starting Portfolio Value: {cerebro.broker.getvalue():,.2f}")

    # add the trading strategy into the engine
    cerebro.addstrategy(TEMA, **strategy_params)

    # set the handling fee, it will be 2%
    cerebro.broker.setcommission(commission=0.0025,margin=False)
    cerebro.addobserver(bt.observers.Trades)
    cerebro.addobserver(bt.observers.DrawDown)
    cerebro.addanalyzer(bt.analyzers.SharpeRatio)

    # set the initial cash
    #cerebro.broker.setcash(initial_cash)

    # run the engine
    strats = cerebro.run()

    print(f"Final Portfolio Value:    {cerebro.broker.getvalue():,.2f}")
    cerebro.plot(volume=False)


STRATEGY_PARAMS = dict(ema1=2, ema2=6, ema3=10)
back = backtest('data/kraken_data.csv',**STRATEGY_PARAMS)
