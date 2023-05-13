from scripts.kraken_data import get_kraken_data
from scripts.ema_optimiser import optimise_ema
from scripts.strategy import *
from scripts.split_krakendata  import *
from scripts.ema_optimiser import calculate_portfolio

# Set up parameters
pair = 'XBTAUD'  # BTC/AUD pair
interval = 1440  # Daily interval
since = 1609430400  # Timestamp for start date (January 1, 2021)

try:
    # Retrieve and save Kraken data
    kraken_data = get_kraken_data(pair, interval, since)
except Exception as e:
    print(f"Error retrieving Kraken data: {e}")

#Split function, must provide the date in the format %d-%m-%y
pd_split(kraken_data,'01-01-2022')

# Set parameters for optimization
ema_ranges = (range(1, 25), range(5, 50), range(10, 75))
population_size = 200
generations = 50
low_bound=[1,1,1]
up_bound=[25,50,75]

# Run the optimization
best_individual, best_fitness = optimise_ema(backtest, ema_ranges, population_size, generations,low_bound,up_bound)
print(f"Best individual: {best_individual}, best fitness: {best_fitness}")

# Run evaluation
#ema1, ema2, ema3 = best_individual
#backtest('data/kraken_train.csv', plot=True, ema1=ema1, ema2=ema2, ema3=ema3)
ema1, ema2, ema3 = best_individual
train_fit = calculate_portfolio('data/kraken_train.csv', ema1, ema2, ema3)


# Run evaluation
##ema1, ema2, ema3 = best_individual
#backtest('data/kraken_validation.csv', plot=True, ema1=ema1, ema2=ema2, ema3=ema3)
eval_fit = calculate_portfolio('data/kraken_validation.csv', ema1, ema2, ema3)
print(f"Train result: {train_fit}, Evaluation result: {eval_fit}")