import bs4 as bs
import requests
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Fetch info from url tesla Revenue
url = " https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm"
response = requests.get(url)
soup = bs.BeautifulSoup(response.content, "html.parser")


table_tesla_revenue = soup.find("table")
# print(table_tesla_revenue)

# Extract the table headers
table_headers = table_tesla_revenue.find_all("th")

table_headers_text = [header.text for header in table_headers]
# print(table_headers_text)

# Extract the table rows
table_rows = table_tesla_revenue.find_all("tr")
for row in table_rows:
    row_data = row.find_all("td")
    row_text = [data.text for data in row_data]

# add data to table_data
table_data = []
for row in table_rows:
    row_data = row.find_all("td")
    row_text = [data.text for data in row_data]
    table_data.append(row_text)

# change format to year and revenue float
formatted_table_data = []
for row in table_data[1:]:
    year = row[0]
    revenue = row[1].replace("$", "").replace(",", "")
    formatted_table_data.append([year, float(revenue)])

table_data = formatted_table_data


# Create a Pandas DataFrame
revenue_df_tesla = pd.DataFrame(table_data, columns="Year Rev(USDMillions)".split())
print(revenue_df_tesla.head())

## Fetch stock data from yfinance TSLA

tesla = yf.Ticker("TSLA")
tesla_stock_price = tesla.history(period="max")
tesla_stock_price.reset_index(inplace=True)
print(tesla_stock_price.head(5))


#######################################

# fetch revenue from GME (Game Stop)
URL = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html"
res = requests.get(URL)
soup = bs.BeautifulSoup(res.content, "html.parser")


# Extract the table rows
table_gme_revenue = soup.find("table")
# print(table_gme_revenue)
table_rows = table_gme_revenue.find_all("tr")
table_data_gme = []
for row in table_rows:
    row_data = row.find_all("td")
    row_text = [data.text for data in row_data]
    table_data_gme.append(row_text)


# change format to year and revenue float
formatted_table_data_gme = []
for row in table_data_gme[1:]:
    year = row[0]
    revenue = row[1].replace("$", "").replace(",", "")
    formatted_table_data_gme.append([year, float(revenue)])

# Create a Pandas DataFrame
revenue_df_gme = pd.DataFrame(
    formatted_table_data_gme, columns="Year Rev(USDMillions)".split()
)
print(revenue_df_gme.tail(5))

# Fetch stock data from yfinance GME
gamestop = yf.Ticker("GME")
gamestop_stock_price = gamestop.history(period="max")
gamestop_stock_price.reset_index(inplace=True)
print(gamestop_stock_price.head(5))


####################################################################


# function to plot stock price and revenue
def plot_stock_price_revenue(stock_price_df, revenue_df, stock_ticker):
    # Create subplot with secondary y-axis
    fig = make_subplots(
        rows=1,
        cols=1,
        shared_xaxes=True,
        subplot_titles=(f"{stock_ticker} Stock Price and Revenue",),
        specs=[[{"secondary_y": True}]],  # Enable secondary y-axis
    )

    # Add stock price trace (Primary Y-axis)
    fig.add_trace(
        go.Scatter(
            x=stock_price_df["Date"],
            y=stock_price_df["Close"],
            name="Stock Price",
            line=dict(color="blue"),
        ),
        row=1,
        col=1,
        secondary_y=False,  # Stock price on primary y-axis
    )

    # Add revenue trace (Secondary Y-axis)
    fig.add_trace(
        go.Scatter(
            x=revenue_df["Year"],
            y=revenue_df["Rev(USDMillions)"],
            name="Revenue",
            line=dict(color="green"),
        ),
        row=1,
        col=1,
        secondary_y=True,  # Revenue on secondary y-axis
    )

    # Update axes labels
    fig.update_yaxes(title_text="Price (USD)", row=1, col=1, secondary_y=False)
    fig.update_yaxes(
        title_text="Revenue (USD Millions)", row=1, col=1, secondary_y=True
    )

    # Update layout
    fig.update_layout(
        title=f"{stock_ticker} Stock Price and Revenue", xaxis_title="Date"
    )

    # Show plot
    fig.show()


plot_stock_price_revenue(tesla_stock_price, revenue_df_tesla, "TSLA")
plot_stock_price_revenue(gamestop_stock_price, revenue_df_gme, "GME")
