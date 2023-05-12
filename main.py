from scripts.kraken_data import get_kraken_data
from scripts.ema_optimiser import optimise_ema
from scripts.strategy import *

# Set up parameters
pair = 'XBTAUD'  # BTC/AUD pair
interval = 1440  # Daily interval
since = 1609430400  # Timestamp for start date (January 1, 2021)

try:
    # Retrieve and save Kraken data
    kraken_data = get_kraken_data(pair, interval, since)
except Exception as e:
    print(f"Error retrieving Kraken data: {e}")

# Set parameters for optimization
ema_ranges = (range(1, 25), range(5, 50), range(10, 75))
population_size = 100
generations = 20
low_bound=[1,5,10]
up_bound=[25,50,75]

# Run the optimization
best_individual, best_fitness = optimise_ema(backtest, ema_ranges, population_size, generations,low_bound,up_bound)
print(f"Best individual: {best_individual}, best fitness: {best_fitness}")

# Run evaluation
ema1, ema2, ema3 = best_individual
backtest('data/kraken_data.csv', plot=True, ema1=ema1, ema2=ema2, ema3=ema3)
