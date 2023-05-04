import backtrader as bt
import warnings
import pandas as pd

# Define the TEMA trading strategy
class TEMA(bt.Strategy):
    params = dict(ema1=16, ema2=39, ema3=41)

    def __init__(self):
        # Create the EMA indicators with given periods
        self.small_p = bt.indicators.EMA(self.data.close, period=self.p.ema1)
        self.medium_p = bt.indicators.EMA(self.data.close, period=self.p.ema2)
        self.large_p = bt.indicators.EMA(self.data.close, period=self.p.ema3)

        self.prev_signal = None  # Track the previous signal

    def next(self):
        # Check if the small period EMA is greater than the others and execute buy signal
        if self.small_p > self.medium_p and self.small_p > self.large_p:
            if self.prev_signal != 'buy':
                self.buy()
                self.prev_signal = 'buy'
        # Check if the small period EMA is less than the others and execute sell signal
        elif self.small_p < self.medium_p and self.small_p < self.large_p:
            if self.prev_signal != 'sell':
                self.sell()
                self.prev_signal = 'sell'

# Read the data file
def read_datafile(data_file):
    # Load data from file with error handling
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=UserWarning)
        df = pd.read_csv(data_file, index_col=1, parse_dates=True, dtype={'timestamp': 'object'}).sort_index()
        df.index = pd.to_datetime(pd.to_numeric(df.index), unit='s')
    return df[["open", "high", "low", "close"]].round(4)

# Perform backtesting
def backtest(data_file, plot=False, **strategy_params):

    data = read_datafile(data_file)

    cerebro = bt.Cerebro()

    data_feed = bt.feeds.PandasData(dataname=data)
    cerebro.adddata(data_feed)

    cerebro.broker.setcash(100.0)

    print(f"Starting Portfolio Value: {cerebro.broker.getvalue():,.2f}")

    cerebro.addstrategy(TEMA, **strategy_params)

    # Set the commission and add observers and analyzers to Cerebro
    cerebro.broker.setcommission(commission=0.02, margin=False)
    cerebro.addobserver(bt.observers.Trades)
    cerebro.addobserver(bt.observers.DrawDown)
    cerebro.addanalyzer(bt.analyzers.SharpeRatio)

    cerebro.run()
    final_portfolio_value = cerebro.broker.getvalue()
    print(f"Final Portfolio Value:    {final_portfolio_value:,.2f}")

    if plot:
        cerebro.plot(volume=False)

    return final_portfolio_value