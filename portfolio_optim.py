# Script to optimise a finance portfolio using the Efficient Frontier Module

from pandas_datareader import data as web
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices

plt.style.use("fivethirtyeight")

# Getting stock ticker from portfolio
assets = ["FB", "AMZN", "AAPL", "NFLX", "GOOG"]

# Assign weights to tickers
weights = np.array([0.2, 0.2, 0.2, 0.2, 0.2])

# Get start date for portfolio
stock_start = "2013-01-01"

# Get end date
today = datetime.today().strftime("%Y-%m-%d")

# Creating dataframe ro store adjusted close price of stocks
df = pd.DataFrame()

# Store adjusted close price

for stock in assets:
    df[stock] = web.DataReader(stock, data_source="yahoo", start=stock_start, end=today)["Adj Close"]

# Visually showing portfolio
title = "Portfolio Adj Close Price History"
my_stocks = df
for c in my_stocks.columns.values:
    plt.plot(my_stocks[c], label=c)

plt.title(title)
plt.xlabel("Date", fontsize=18)
plt.ylabel("Adj Price $", fontsize=18)
plt.legend(my_stocks.columns.values, loc="upper left")
plt.show()

# Showing daily returns
returns = df.pct_change()

# Create annualised covariance matrix
covariance = returns.cov() * 252

# Calculate portfolio variance
variance = np.dot(weights.T, np.dot(covariance, weights))

# Calculate portfolio volatility (std dev)
volatility = np.sqrt(variance)

# Calculate annual portfolio return
annual_return = np.sum(returns.mean() * weights) * 252

# Show the expected annual return, volatility (risk) & variance
percent_var = str(round(variance, 2) * 100) + "%"
percent_vol = str(round(volatility, 2) * 100) + "%"
percent_return = str(round(annual_return, 2) * 100) + "%"

print("Expected annual return: " + percent_return)
print("Annual volatility/risk: " + percent_vol)
print("Annual variance: " + percent_var)

# Portfolio Optimisation

# Calculate expected returns and annualised sample covariance matrix
mu = expected_returns.mean_historical_return(df)
S = risk_models.sample_cov(df)

# Optimising for max sharpe ratio
ef = EfficientFrontier(mu, S)
weights = ef.max_sharpe()
cleaned_weights = ef.clean_weights()
for key in cleaned_weights:
    print(key, ":", cleaned_weights[key])
ef.portfolio_performance(verbose=True)

# Get the discrete allocation of each share per stock
latest_prices = get_latest_prices(df)
weights = cleaned_weights
da = DiscreteAllocation(weights, latest_prices,  total_portfolio_value=15000)
allocation, leftover = da.lp_portfolio()
print("Discrete allocation: ", allocation)
print("Funds remaining: ${:.2f}".format(leftover))
