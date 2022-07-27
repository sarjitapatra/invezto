import streamlit as st
from pypfopt.expected_returns import mean_historical_return
from pypfopt.risk_models import CovarianceShrinkage
from pypfopt.efficient_frontier import EfficientFrontier, EfficientCVaR
from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices
from pypfopt import HRPOpt

def main():
    tab1, tab2, tab3 = st.tabs(["Mean Variance", "HRP Method", "mCVAR Method"])

    if st.session_state["portfolio"] is None:
        with tab1:
            st.error("Please build a portfolio in the 'Build' tab first 😊")
        with tab2:
            st.error("Please build a portfolio in the 'Build' tab first 😊")
        with tab3:
            st.error("Please build a portfolio in the 'Build' tab first 😊")

    else:
        with tab1:
            option1 = st.selectbox('Start optimizing', ('No', 'Yes'))
            if option1 == 'Yes':
                amt1 = st.number_input('Enter the total amount of investment', min_value = 0.01, value = 100.00)
                portfolio = st.session_state["portfolio"]
                mu = mean_historical_return(portfolio)
                S = CovarianceShrinkage(portfolio).ledoit_wolf()
                ef = EfficientFrontier(mu, S)
                weights = ef.max_sharpe()
                cleaned_weights = ef.clean_weights()
                st.write("Cleaned weights : ", dict(cleaned_weights))
                info1 = ef.portfolio_performance(verbose=True)
                st.write("Expected annual return : ", info1[0], " %")
                st.write("Annual volatility : ", info1[1], " %")
                st.write("Sharpe ratio : ", info1[2])
                latest_prices = get_latest_prices(portfolio)
                da = DiscreteAllocation(weights, latest_prices, total_portfolio_value = amt1)
                allocation, leftover = da.greedy_portfolio()
                st.write("Discrete allocation : ", allocation)
                st.write("Funds remaining after building minimum volatility portfolio : $", leftover)
            else:
                pass

        with tab2:
            option2 = st.selectbox('Start optimizing for me', ('No', 'Yes'))
            if option2 == 'Yes':
                amt2 = st.number_input('Enter total amount of investment', min_value = 0.01, value = 100.00)
                portfolio = st.session_state["portfolio"]
                returns = portfolio.pct_change().dropna()
                hrp = HRPOpt(returns)
                hrp_weights = hrp.optimize()
                st.write("Cleaned weights : ", hrp_weights)
                info2 = hrp.portfolio_performance(verbose = True)
                st.write("Expected annual return : ", info2[0], " %")
                st.write("Annual volatility : ", info2[1], " %")
                st.write("Sharpe ratio : ", info2[2])           
                da_hrp = DiscreteAllocation(hrp_weights, latest_prices, total_portfolio_value = amt2)
                allocation, leftover = da_hrp.greedy_portfolio()
                st.write("Discrete allocation : ", allocation)
                st.write("Funds remaining after building minimum volatility portfolio : $", leftover)
            else:
                pass

        with tab3:
            option3 = st.selectbox('Start optimizing my portfolio', ('No', 'Yes'))
            if option3 == 'Yes':
                amt3 = st.number_input('Enter your total amount of investment', min_value = 0.01, value = 100.00)
                portfolio = st.session_state["portfolio"]
                S = portfolio.cov()
                ef_cvar = EfficientCVaR(mu, S)
                cvar_weights = ef_cvar.min_cvar()
                cleaned_weights = ef_cvar.clean_weights()
                st.write("Cleaned weights : ", dict(cleaned_weights))
                # st.write(ef.portfolio_performance(verbose=True))
                da_cvar = DiscreteAllocation(cvar_weights, latest_prices, total_portfolio_value = amt3)
                allocation, leftover = da_cvar.greedy_portfolio()
                st.write("Discrete allocation : ", allocation)
                st.write("Funds remaining after building minimum volatility portfolio : $", leftover)
            else:
                pass

if __name__ == "__main__":
    main()