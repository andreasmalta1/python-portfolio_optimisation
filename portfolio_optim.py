# A script to optimise a finance portfolio using the Efficient Frontier Module

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

# In the assets variable enter the tickers of your portfolio
assets = ["FB", "AMZN", "AAPL", "VOO", "GOOG"]

# In the weights variable assign the weights for each ticker, The total of all weights amount to 0 (zero)
weights = np.array([0.2, 0.2, 0.2, 0.2, 0.2])

# Enter the portfolio start date
stock_start = "2013-01-01"

# The end day is set as the present day
today = datetime.today().strftime("%Y-%m-%d")

# Creating dataframe to store the adjusted close price of stocks. The prices are retrieved from Yahoo
df = pd.DataFrame()
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

# Working the daily returns, covariance, volatility & annual for current portfolio
returns = df.pct_change()
covariance = returns.cov() * 252
variance = np.dot(weights.T, np.dot(covariance, weights))
volatility = np.sqrt(variance)
annual_return = np.sum(returns.mean() * weights) * 252

# Show the expected annual return, volatility (risk) & variance as a percentile
percent_var = str(round(variance, 2) * 100) + "%"
percent_vol = str(round(volatility, 2) * 100) + "%"
percent_return = str(round(annual_return, 2) * 100) + "%"

print("Expected annual return: " + percent_return)
print("Annual volatility/risk: " + percent_vol)
print("Annual variance: " + percent_var)

# Optimising the portfolio

# Calculate expected returns and annualised sample covariance matrix
mu = expected_returns.mean_historical_return(df)
S = risk_models.sample_cov(df)

# Optimising for max sharpe ratio
ef = EfficientFrontier(mu, S)
weights = ef.max_sharpe()
cleaned_weights = ef.clean_weights()
print("Optimised portfolio")
print("{:<8} {:<15}".format('Ticker', 'Weight'))
for key in cleaned_weights:
    print("{:<8} {:<15}".format(key, cleaned_weights[key]))
ef.portfolio_performance(verbose=True)

# Getting the discrete allocation of each share per
# Enter the funds available in USD in the funds variable
funds = 15000
latest_prices = get_latest_prices(df)
weights = cleaned_weights
da = DiscreteAllocation(weights, latest_prices,  total_portfolio_value=funds)
allocation, leftover = da.lp_portfolio()
print("Discrete allocation")
print("{:<8} {:<15}".format('Ticker', 'No. of Shares'))
for key in allocation:
    print("{:<8} {:<15}".format(key, allocation[key]))
print("Funds remaining: ${:.2f}".format(leftover))
