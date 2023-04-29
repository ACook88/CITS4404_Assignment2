from scripts.kraken_data import get_kraken_data
from scripts.generate_ta_metrics import generate_metrics_and_chart


# Set up parameters
pair = 'XBTAUD'  # BTC/AUD pair
interval = 1440  # Daily interval
since = 1609430400  # Timestamp for start date (January 1, 2021)

try:
    # Retrieve and save Kraken data
    kraken_data = get_kraken_data(pair, interval, since)
except Exception as e:
    print(f"Error retrieving Kraken data: {e}")

# Set up TA window sizes
sma1 = 20
sma2 = 50

try:
    # Create chart in /graphs
    generate_metrics_and_chart('data/kraken_data.json', sma1, sma2)

except Exception as e:
    print(f"Error generating chart: {e}")