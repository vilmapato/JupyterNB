import yfinance as yf
import pandas as pd
import json

# Fetch stock data from Yahoo Finance AMD
amd = yf.Ticker("AMD")
print(type(amd.info))

amd_country = amd.info["country"]
amd_sector = amd.info["sector"]
print(amd_country)
print(amd_sector)


amd_historic_prices = amd.history(period="max")
amd_volume_first_day = amd_historic_prices.iloc[0]["Volume"]
print(amd_volume_first_day)

amd_historic_prices.reset_index(inplace=True)
print(amd_historic_prices.head(5))

amd_historic_prices.plot(x="Date", y="Close", title="AMD Stock Price")
