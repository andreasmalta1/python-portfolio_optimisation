# python-portfolio_optimisation

# A script to optimise a finance portfolio using the Efficient Frontier Module.

The script receives the tickers of your portfolio, the portfolio weight distribution and its start date.

In the first part of the program a chart showing the adjusted close price history of the portfolio is displayed. The program returns the expected annual return, annual volatility/risk and annual variance.

In the second part, the program optimises the portfolio by using the max sharpe method. The programs returns the optimised weights for each ticker as well  the expected annual return, volatility and sharpe ratio for the optimised portfolio. 

Finally after entering your portfolio value in USD ($) the program retuns how much of each stock one should buy and the remaining fund allocation.

To personalise your portolio: the following changes are to be made:

- line 15: enter the tickers in the assets list
- line 18: enter the weights for each stocks in the weights list (total of all values should equal 1 (one))
- line 21: enter the start date of your portfolio
- line 77: enter the funds available for your portfolio in USD ($)

# THIS IS NOT INVESTMENT ADVICE
