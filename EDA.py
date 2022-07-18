import streamlit as st
import Dataset

# import pymongo

# import gspread
# from df2gspread import df2gspread as d2g
# from oauth2client.service_account import ServiceAccountCredentials

import numpy as np
import pandas as pd

import plotly.express as px
from plotly import graph_objects as go

from statsmodels.tsa.stattools import acf, pacf
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller

@st.experimental_singleton(suppress_st_warning=True, show_spinner = False)
def fetch_and_prepare_data():

    with st.spinner('Please wait while we fetch your dataset...'):

        db = Dataset.init_connection()
        name = st.session_state.name
        st.write(name)
        collection = db.get_collection(name)
        df = pd.DataFrame(list(collection.find({}))).astype({"_id": str})
        df_edited = df.drop(columns = ["_id"])

    # gc = gspread.service_account(filename = 'invezto-d11008a8055f.json')
    # sh = gc.open_by_url("https://docs.google.com/spreadsheets/d/1bvXxcvWTSxbVOBwoCGpxxgy_sPdFxs-YF12fMn4ej6A/edit#gid=0")
    # ws = sh.worksheet('init')
    # df = pd.DataFrame(ws.get_all_records())

    if df_edited is not None:
        st.success('File successfully fetched!')
        return df_edited
    else:
        st.write('Please upload a valid file in the "Dataset" page')
        return None

def main():

    df = fetch_and_prepare_data()
    # st.write(type(df["Date"][0]))
    # st.write(df.head())
    if df is not None:
        option = st.selectbox('Prepare colourful fun charts for my data', ['No', 'Yes'])
        if option == 'Yes':
        # if st.button('Prepare colourful fun charts for my data'):
        # monthwise opening and closing price
            with st.expander('Show me the monthly opening and closing trends of stock price'):
                monthwise = df.groupby(df["Date"].dt.strftime('%B'))[["Open", "Close"]].mean()
                new_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 
                            'September', 'October', 'November', 'December']
                monthwise_ordered = monthwise.reindex(new_order, axis = 0)
                fig = go.Figure()
                fig.add_trace(go.Bar(x = monthwise_ordered.index, 
                                    y = monthwise_ordered["Open"], 
                                    name = "Stock open price", 
                                    marker_color = "crimson"))
                fig.add_trace(go.Bar(x = monthwise_ordered.index, 
                                    y = monthwise_ordered["Close"], 
                                    name = "Stock close price", 
                                    marker_color = "lightsalmon"))
                fig.update_layout(barmode = "group", 
                                xaxis_title = "Month", 
                                yaxis_title="Stock Price", 
                                xaxis_tickangle = -45, 
                                title = "Monthwise comparison b/w stock opening & closing price", 
                                font_size = 15,autosize=True,
                                width=1200,
                                height=600)
                st.plotly_chart(fig)

            # monthwise high and low price
            with st.expander('Show me monthwise high and low price'):
                new_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 
                            'September', 'October', 'November', 'December']
                monthwise_high = df.groupby(df["Date"].dt.strftime('%B'))[["High"]].max()
                monthwise_high_ordered = monthwise_high.reindex(new_order, axis = 0)
                monthwise_low = df.groupby(df["Date"].dt.strftime('%B'))[["Low"]].min()
                monthwise_low_ordered = monthwise_low.reindex(new_order, axis = 0)
                fig = go.Figure()
                fig.add_trace(go.Bar(x = monthwise_high_ordered.index, 
                                    y = monthwise_high_ordered["High"], 
                                    name = "Monthwise high price", 
                                    marker_color = "rgb(0, 153, 204)"))
                fig.add_trace(go.Bar(x = monthwise_low_ordered.index, 
                                    y = monthwise_low_ordered["Low"], 
                                    name = "Monthwise low price", 
                                    marker_color = "rgb(255, 128, 0)"))
                fig.update_layout(barmode = "group", 
                                xaxis_title = "Month",
                                yaxis_title = "Stock Price",
                                plot_bgcolor = "rgb(255, 255, 200)", 
                                xaxis_tickangle = -45, 
                                title = "Monthwise high and low price",
                                autosize=True,
                                width=1200,
                                height=600)
                st.plotly_chart(fig)

            # closing_trends_stock_price(df)
            with st.expander('Show me the monthly closing trends of stock price'):
                fig = px.line(df, x = df["Date"], y = df["Close"], labels = {"Date" : "Date", "Close" : "Closing price"})
                fig.update_layout(title = "Stock Closing Price", 
                                plot_bgcolor = "rgb(255, 255, 200)", 
                                font_size = 15,
                                autosize=True,
                                width=1200,
                                height=600)
                fig.update_xaxes(showgrid = False)
                fig.update_yaxes(showgrid = False)
                st.plotly_chart(fig)

            # monthly_volume_of_company(df)
            with st.expander('Show me the monthly volume of company'):
                fig = px.line(df, x = df["Date"], y = df["Volume"], labels = {"Date" : "Date", "Close" : "Volume"})
                fig.update_layout(title = "Monthly volume of company",
                                plot_bgcolor = "rgb(255, 255, 200)", 
                                font_size = 15,
                                autosize=True,
                                width=1200,
                                height=600)
                fig.update_xaxes(showgrid = False)
                fig.update_yaxes(showgrid = False)
                st.plotly_chart(fig)

            #high_price(df)
            with st.expander('Show me the high price of company over time'):
                df["Change"] = df["High"].div(df["High"].shift())
                fig = go.Figure()
                fig.add_trace(go.Scatter(x = df["Date"], y = df["Change"]))
                fig.update_layout(title = 'Change in high price of company', 
                                xaxis_title = "Date",
                                yaxis_title = "Stock High Price",
                                plot_bgcolor = "rgb(255, 255, 200)", 
                                font_size = 15,
                                autosize=True,
                                width=1200,
                                height=600)
                st.plotly_chart(fig)

            # change_in_monthly_volume(df)
            with st.expander('Show me the change in company volume over time'):
                df["Change"] = df["Volume"].div(df["High"].shift())
                fig = go.Figure()
                fig.add_trace(go.Scatter(x = df["Date"], y = df["Change"]))
                fig.update_layout(title = 'Change in company volume', 
                                xaxis_title = "Date",
                                yaxis_title = "Change in Company Volume",
                                plot_bgcolor = "rgb(255, 255, 200)", 
                                font_size = 15,
                                autosize=True,
                                width=1200,
                                height=600)
                st.plotly_chart(fig)

            # daily_percentage_return(df)
            with st.expander('Show me the daily percentage return'):
                df["Daily Return"] = df["Adj Close"].pct_change()
                fig = go.Figure()
                fig.add_trace(go.Scatter(x = df["Date"], y = df["Daily Return"]))
                fig.update_layout(title = 'Daily percentage return', 
                                xaxis_title = "Date",
                                yaxis_title = "Daily return in percentage",
                                plot_bgcolor = "rgb(255, 255, 200)", 
                                font_size = 15, 
                                autosize=True,
                                width=1200,
                                height=600)
                st.plotly_chart(fig)

            # return_based_on_high_price(df)
            with st.expander('Show me the return based on high price change of the company'):
                df['Change'] = df["High"].div(df["High"].shift())
                df["Return"] = df["Change"].sub(1).mul(100)
                fig = go.Figure()
                fig.add_trace(go.Scatter(x = df["Date"], y = df["Return"]))
                fig.update_layout(title = 'Return based on high price change', 
                                xaxis_title = "Date",
                                yaxis_title = "Return Based on High Price",
                                plot_bgcolor = "rgb(255, 255, 200)", 
                                font_size = 15,
                                autosize=True,
                                width=1200,
                                height=600)
                st.plotly_chart(fig)

            # difference_in_high_price_change(df)
            with st.expander('Show me the difference in high price change of the company'):
                fig = go.Figure()
                fig.add_trace(go.Scatter(x = df["Date"], y = df["High"].diff()))
                fig.update_layout(title = 'Difference in high price change', 
                                xaxis_title = "Date",
                                yaxis_title = "Difference in High Price Change",
                                plot_bgcolor = "rgb(255, 255, 200)", 
                                font_size = 15,
                                autosize=True,
                                width=1200,
                                height=600)
                st.plotly_chart(fig)

            # comparison_of_high_and_rolling_high(df)
            with st.expander('Show me the comparison of high price and rolling high price'):
                fig = go.Figure()
                fig.add_trace(go.Scatter(x = df["Date"], y = df["High"], name = 'High price'))
                fig.add_trace(go.Scatter(x = df["Date"], y = df["High"].rolling(90).mean(), name = 'Rolling high price'))
                fig.update_layout(title = 'Comparison of high price and rolling high price', 
                                xaxis_title = "Date",
                                plot_bgcolor = "rgb(255, 255, 200)", 
                                font_size = 15,
                                autosize=True,
                                width=1200,
                                height=600)
                st.plotly_chart(fig)

            # ohlc chart
            with st.expander('Show me the OHLC chart of a particular year'):
                years = np.sort(df["Date"].dt.strftime('%Y').unique())
                option = st.radio('Select the year to show OHLC chart', years)
                fig = go.Figure()
                fig.add_trace(go.Ohlc(x = df[df["Date"].dt.strftime('%Y') == option]["Date"], 
                                    open = df[df["Date"].dt.strftime('%Y') == option]["Open"],
                                    high = df[df["Date"].dt.strftime('%Y') == option]["High"],
                                    low = df[df["Date"].dt.strftime('%Y') == option]["Low"],
                                    close = df[df["Date"].dt.strftime('%Y') == option]["Close"]))
                title = f'OHLC chart of {option}'
                fig.update_layout(title = title, 
                                xaxis_title = "Month",
                                plot_bgcolor = "rgb(255, 255, 200)", 
                                font_size = 15,
                                autosize=True,
                                width=1200,
                                height=600)
                st.plotly_chart(fig)

            # candlestick chart
            with st.expander('Show me the Candlestick chart of a particular year'):
                years = np.sort(df["Date"].dt.strftime('%Y').unique())
                option = st.radio('Select the year to show Candlestick chart', years)
                fig = go.Figure()
                fig.add_trace(go.Candlestick(x = df[df["Date"].dt.strftime('%Y') == option]["Date"], 
                                            open = df[df["Date"].dt.strftime('%Y') == option]["Open"],
                                            high = df[df["Date"].dt.strftime('%Y') == option]["High"],
                                            low = df[df["Date"].dt.strftime('%Y') == option]["Low"],
                                            close = df[df["Date"].dt.strftime('%Y') == option]["Close"]))
                title = f'Candlestick chart of {option}'
                fig.update_layout(title = title, 
                                xaxis_title = "Month",
                                plot_bgcolor = "rgb(255, 255, 200)", 
                                font_size = 15,
                                autosize=True,
                                width=1200,
                                height=600)
                st.plotly_chart(fig)

            # comparison_of_high_price_and_mean_and_std_of_it(df)
            with st.expander('Show me the comparison of high price, expanding mean, and expanding stdev of high price'):
                fig = go.Figure()
                fig.add_trace(go.Scatter(x = df["Date"], y = df["High"], name = 'High price'))
                fig.add_trace(go.Scatter(x = df["Date"], y = df["High"].expanding().mean(), name = 'Mean of expanding high price'))
                fig.add_trace(go.Scatter(x = df["Date"], y = df["High"].expanding().std(), name = 'Stdev of expanding high price'))
                fig.update_layout(title = 'Comparison of high price, expanding mean, and expanding stdev of high price', 
                                xaxis_title = "Date",
                                plot_bgcolor = "rgb(255, 255, 200)", 
                                font_size = 15,
                                autosize=True,
                                width=1200,
                                height=600)
                st.plotly_chart(fig)

            # autocorrelation plot
            with st.expander('Show me the autocorrelation chart'):
                df_acf = acf(df["Close"], nlags = 25)
                fig = go.Figure()
                fig.add_trace(go.Scatter(x= np.arange(len(df_acf)), y= df_acf, name= 'ACF'))
                fig.update_xaxes(rangeslider_visible=True)
                fig.update_layout(title="Autocorrelation", 
                                xaxis_title="Lag", 
                                yaxis_title="Autocorrelation",
                                plot_bgcolor = "rgb(255, 255, 200)", 
                                font_size = 15,
                                autosize=True,
                                width=1200,
                                height=600)
                st.plotly_chart(fig)

            # partial autocorrelation plot
            with st.expander('Show me the partial autocorrelation chart'):
                df_pacf = pacf(df["Close"], nlags = 25)
                fig = go.Figure()
                fig.add_trace(go.Scatter(x= np.arange(len(df_pacf)), y= df_pacf, name= 'PACF'))
                fig.update_xaxes(rangeslider_visible=True)
                fig.update_layout(title="Partial Autocorrelation", 
                                xaxis_title="Lag", 
                                yaxis_title="Partial Autocorrelation",
                                plot_bgcolor = "rgb(255, 255, 200)", 
                                font_size = 15,
                                autosize=True,
                                width=1200,
                                height=600)
                st.plotly_chart(fig)

            # decomposition_plot(df)
            with st.expander('Show me the series decomposition plot'):
                decomposed_data_close = seasonal_decompose(df["Close"], model='additive', period=365)

                fig = go.Figure()
                fig.add_trace(go.Scatter(x = df["Date"], y = decomposed_data_close.trend))
                fig.update_layout(title = 'Trend', 
                                xaxis_title = "Date",
                                yaxis_title = "Trend",
                                plot_bgcolor = "rgb(255, 255, 200)", 
                                font_size = 15,
                                autosize=True,
                                width=1200,
                                height=600)
                st.plotly_chart(fig)

                fig = go.Figure()
                fig.add_trace(go.Scatter(x = df["Date"], y = decomposed_data_close.seasonal))
                fig.update_layout(title = 'Seasonality', 
                                xaxis_title = "Date",
                                yaxis_title = "Seasonality",
                                plot_bgcolor = "rgb(255, 255, 200)", 
                                font_size = 15,
                                autosize=True,
                                width=1200,
                                height=600)
                st.plotly_chart(fig)

                fig = go.Figure()
                fig.add_trace(go.Scatter(x = df["Date"], y = decomposed_data_close.resid))
                fig.update_layout(title = 'Residuality', 
                                xaxis_title = "Date",
                                yaxis_title = "Residuality",
                                plot_bgcolor = "rgb(255, 255, 200)", 
                                font_size = 15,
                                autosize=True,
                                width=1200,
                                height=600)
                st.plotly_chart(fig)

                adf = adfuller(df["Volume"])
                st.write("p-value of company: ",float(adf[1]))
                if(float(adf[1])<=0.05):
                    st.info("Data is stationary")
                else:
                    st.info("Data is not stationary")


if __name__ == "__main__":
    main()
