import streamlit as st
import Stock_Price
import Portfolio

st.set_page_config(
     page_title="Invezto",
     page_icon="📈",
     layout="wide",
     initial_sidebar_state="auto",
 )

def main():
    option = st.selectbox('Menu', ['Stock Price Prediction', 'Portfolio Optimization'])
    if option == 'Stock Price Prediction':
        Stock_Price.main()
    if option == 'Portfolio Optimization':
        Portfolio.main()

if __name__ == "__main__":
    main()