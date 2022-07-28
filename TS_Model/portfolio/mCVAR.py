import pandas as pd
from pypfopt.expected_returns import mean_historical_return
from pypfopt.efficient_frontier import EfficientCVaR
from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices

portfolio = pd.read_csv('portfolio.csv')

mu = mean_historical_return(portfolio)
S = portfolio.cov()
ef_cvar = EfficientCVaR(mu, S)
cvar_weights = ef_cvar.min_cvar()

cleaned_weights = ef_cvar.clean_weights()
print(dict(cleaned_weights))

#allocation
latest_prices = get_latest_prices(portfolio)
da_cvar = DiscreteAllocation(cvar_weights, latest_prices, total_portfolio_value = 100000)

allocation, leftover = da_cvar.greedy_portfolio()
print("Discrete allocation (CVAR):", allocation)
print("Funds remaining after building CVAR portfolio): ${:.2f}".format(leftover))