import pandas as pd
from pypfopt import HRPOpt
from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices

portfolio = pd.read_csv('portfolio.csv')
returns = portfolio.pct_change().dropna()

hrp = HRPOpt(returns)
hrp_weights = hrp.optimize()

hrp.portfolio_performance(verbose=True)
print(dict(hrp_weights))

#allocation
latest_prices = get_latest_prices(portfolio)
da_hrp = DiscreteAllocation(hrp_weights, latest_prices, total_portfolio_value = 100000)

allocation, leftover = da_hrp.greedy_portfolio()
print("Discrete allocation (HRP):", allocation)
print("Funds remaining after building HRP portfolio : ${:.2f}".format(leftover))