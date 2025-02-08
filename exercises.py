import requests
from datetime import datetime, timedelta
from collections import defaultdict
import pandas as pd

# Fetch top 10 cryptocurrencies by market cap
response = requests.get(
    "https://api.coingecko.com/api/v3/coins/markets",
    params={
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 10,
        "page": 1,
    },
)

top_coins = response.json()


# Function to fetch historical data
def fetch_historical_data(coin_id):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    response = requests.get(
        f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart/range",
        params={
            "vs_currency": "usd",
            "from": int(start_date.timestamp()),
            "to": int(end_date.timestamp()),
        },
    )
    return response.json()


# Fetch historical data for each top coin
historical_data = {}
for coin in top_coins:
    coin_id = coin["id"]
    historical_data[coin_id] = fetch_historical_data(coin_id)


# Function to process historical data
def process_historical_data(data):
    if "prices" not in data:
        return {}
    prices = data["prices"]
    daily_prices = defaultdict(list)
    for timestamp, price in prices:
        date = datetime.fromtimestamp(timestamp / 1000).date()
        daily_prices[date].append(price)
    daily_open_close = {
        date: {"open": prices[0], "close": prices[-1]}
        for date, prices in daily_prices.items()
    }
    return daily_open_close


# Process historical data for each coin
processed_data = {}
for coin_id, data in historical_data.items():
    processed_data[coin_id] = process_historical_data(data)


processed_data_df = pd.DataFrame(processed_data)
print(processed_data_df.head())
