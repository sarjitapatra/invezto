import joblib
import streamlit as st
import EDA
import io
import datetime
import numpy as np
import pandas as pd
from plotly import graph_objects as go
import plotly.express as px
from sklearn.preprocessing import StandardScaler
from tensorflow import keras

@st.experimental_memo(show_spinner = False)
def predict(data, days):

    sc = joblib.load('scaler.sav')
    model = keras.models.load_model('mymodel.h5')
    custom_values = sc.transform(data.tail(60)[["Close"]]["Close"].values.reshape(-1, 1))
    i = 0
    for j in range(days):
        pred_cust = model.predict(custom_values[-60:, 0].reshape(1, 60, 1))
        custom_values = np.append(custom_values, pred_cust.reshape(1)).reshape(-1, 1)
        
    ypred = sc.inverse_transform(custom_values[-(days):, 0].reshape(-1, 1))
    pred = pd.DataFrame(ypred, columns = ["Close"])
    return pred

def display_result(df, days, result):

    st.subheader("Prediction")
    col1, col2 = st.columns(2)

    st.write(result)
    st.write("The predicted table has ", result.shape[0], " rows and ", result.shape[1], " column")
    with col1:
        fig = go.Figure()
        res = [df["Date"].iloc[-1] + datetime.timedelta(days = idx + 1) for idx in range(days)]
        fig.add_trace(go.Scatter(x = res, y = result[["Close"]].values[-(days):, 0], line=dict(color="#ff0000")))
        fig.update_layout(title = "Future Prices",
                            xaxis_title = "Date",
                            yaxis_title = "Stock Price",
                            plot_bgcolor = "rgb(255, 255, 200)", 
                            font_size = 15,
                            autosize=True,)
        st.plotly_chart(fig)
    with col2:
        fig = go.Figure()
        yearwise = df.loc[df["Date"] > datetime.datetime(2019, 12, 31)]
        fig.add_trace(go.Scatter(x = yearwise["Date"], y = yearwise["Close"], name = "Historic Price"))
        fig.add_trace(go.Scatter(x = res, y = result[["Close"]].values[-(days):, 0], name = "Future Price"))
        fig.update_layout(title = "Historic and Future Prices",
                            xaxis_title = "Date",
                            yaxis_title = "Stock Price",
                            plot_bgcolor = "rgb(255, 255, 200)", 
                            font_size = 15,
                            autosize=True,)
        st.plotly_chart(fig)

def main():

    op = st.radio('Predict for next:', ('None', '1 week', '2 weeks', '3 weeks', '1 month', '2 months', '3 months'))
    if op != 'None':

        df = EDA.fetch_and_prepare_data()
        if op == '1 week':
            with st.spinner('Sit tight while we predict'):
                result = predict(df, 7)
                display_result(df, 7, result)
        elif op == '2 weeks':
            with st.spinner('Sit tight while we predict'):
                result = predict(df, 14)
                display_result(df, 14, result)
        elif op == '3 weeks':
            with st.spinner('Sit tight while we predict'):
                result = predict(df, 21)
                display_result(df, 21, result)
        elif op == '1 month':
            with st.spinner('Sit tight while we predict'):
                result = predict(df, 30)
                display_result(df, 30, result)
        elif op == '2 months':
            with st.spinner('Sit tight while we predict'):
                result = predict(df, 60)
                display_result(df, 60, result)
        elif op == '3 months':
            with st.spinner('Sit tight while we predict'):
                result = predict(df, 90)
                display_result(df, 90, result)

        format = st.radio("How do you want to save your result?", ('.xlsx', '.csv'))
        if format == ".csv":
            dat_csv = result.to_csv(index = False).encode('utf-8')
            st.download_button( 
                label = "Download data as .csv",
                data = dat_csv,
                file_name = 'Result.csv',
                mime = 'text/csv',
            )
        else:
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                result.to_excel(writer, sheet_name = "Sheet1", index=False)
            st.download_button( 
                label = "Download data as .xlsx",
                data = buffer,
                file_name = 'Result.xlsx',
                mime = "application/vnd.ms-excel"
            )
    else:
        st.error("Please select a timeframe to predict")

if __name__ == "__main__":
    main()