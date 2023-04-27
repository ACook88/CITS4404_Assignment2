import backtrader as bt
import pandas as pd

# Here is for the trading strategy, after we generate it, we can fill this part
class MyStrategy(bt.Strategy):
    ...


def backtest(data_file, strategy_class, commission_rate=0.02, initial_cash=100):
    # Read the data, here the 'data_file' would be the path of the csv file
    data = pd.read_csv(data_file, parse_dates=['unixtimestap'], index_col='unixtimestap')
    # may need to do some data selection

    # create a Backtrader engine
    cerebro = bt.Cerebro()

    # add the data into the engine
    data_feed = bt.feeds.PandasData(dataname=data)
    cerebro.adddata(data_feed)

    # add the trading strategy into the engine
    cerebro.addstrategy(strategy_class, ...)

    # set the handling fee, it will be 2%
    cerebro.broker.setcommission(commission=commission_rate)

    # set the initial cash
    cerebro.broker.setcash(initial_cash)

    # run the engine
    result = cerebro.run()

    return result[0]


def analyze_backtest(result):
    # print the validation result
    final_value = result.broker.getvalue()
    initial_value = result.broker.startingcash
    profit = (final_value - initial_value) / initial_value
    print(f"Initial Value: {initial_value:.2f} AUD")
    print(f"Final Value: {final_value:.2f} AUD")
    print(f"Profit: {profit:.2%}")

    # plot the candle chart
    cerebro.plot(style='candle')

    # Print the trading details
    for trade in result.trade_history:
        print(trade)

    # Print other result like trading times and winning rate
    trade_count = len(result.trade_history)
    win_count = len([t for t in result.trade_history if t.pnlcomm > 0])
    win_rate = win_count / trade_count
    print(f"Trading times: {trade_count}")
    print(f"Winning rate: {win_rate:.2%}")
