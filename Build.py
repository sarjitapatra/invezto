import streamlit as st
import pandas as pd
import pandas_datareader.data as web
import datetime
from functools import reduce

@st.experimental_memo(show_spinner = False)
def combine_return(start, end, opt):
    df = []
    for i in opt:
        data = web.DataReader(f'{i}', "yahoo", start, end)
        data[f'{i}'] = data["Adj Close"]
        data = data[[f'{i}']]
        df.append(data)
    df_merged = reduce(lambda left, right: pd.merge(left, right, on = ['Date'], how = 'outer'), df)
    return df_merged

def main():
    st.session_state["portfolio"] = None
    col1, col2 = st.columns(2)
    with col1:
        start = st.date_input('Enter the start date', 
                              value = datetime.date.today() - datetime.timedelta(days = 30),
                              min_value = datetime.date(2004, 1, 1), 
                              max_value = datetime.date.today() - datetime.timedelta(days = 30))
    with col2:
        end = st.date_input('Enter the end date',
                             value = datetime.date.today() - datetime.timedelta(days = 1),
                             min_value = datetime.date(2004, 1, 1), 
                             max_value = datetime.date.today() - datetime.timedelta(days = 1))
    options = st.multiselect('Select the companies', ["MRNA", "PFE", "JNJ", "GOOGL", 
          "FB", "AAPL", "COST", "WMT", "KR", "JPM", 
          "BAC", "HSBC"], 
          ["MRNA", "PFE", "JNJ", "GOOGL", 
          "FB", "AAPL", "COST", "WMT", "KR", "JPM", 
          "BAC", "HSBC"])
    if len(options) < 2:
        st.error("Please choose at least two options for portfolio building")
    else:
        with st.spinner('Please wait...'):
            portfolio = combine_return(start, end, options)
        st.session_state["portfolio"] = portfolio
        if st.session_state["portfolio"] is not None:
            if st.checkbox('Show me the portfolio'):
                if portfolio.shape[0] <= 1:
                    st.write("The first 1 row of your entered file is shown :")
                    st.write(portfolio.head(1)) 
                else:              
                    n = st.slider('How many rows do you want to see?', 1, portfolio.shape[0])
                    st.write("The first ", n, "rows of your entered file are shown :")
                    st.write(portfolio.head(n))
            else:
                pass
        else:
            pass

if __name__ == "__main__":
    main()