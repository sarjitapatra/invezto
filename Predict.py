import joblib
import streamlit as st
import EDA

import io

import numpy as np
import pandas as pd

from sklearn.preprocessing import MinMaxScaler
from tensorflow import keras

def prepare_time_series_data(df):
    df = df[["Close"]].values.reshape(-1, 1)
    scaler = joblib.load('scaler.sav')
    df_scaled = scaler.fit_transform(df)
    df_test = []

    for i in range(60, df_scaled.shape[0]):
        df_test.append(df_scaled[i - 60 : i, 0])

    df_test = np.array(df_test)
    df_test = df_test.reshape(df_test.shape[0], df_test.shape[1], 1)

    return df_test

@st.experimental_memo(show_spinner = False)
def predict(data):
    model = keras.models.load_model('mymodel.h5')
    pred = model.predict(data)
    scaler = joblib.load('scaler.sav')
    pred = scaler.inverse_transform(pred)
    pred = pd.DataFrame(pred, columns = ["Close"])
    return pred

def main():

    option = st.selectbox('Start predicting future prices for my stock', ['No', 'Yes'])
    if option == 'Yes':
        df = EDA.fetch_and_prepare_data()
        df_test = prepare_time_series_data(df)
        with st.spinner('Sit tight while we predict'):
            result = predict(df_test)
        st.subheader("Prediction")
        st.write(result)
        st.write("The predicted table has ", result.shape[0], " rows and ", result.shape[1], " column")

        format = st.radio("How do you want to save your result?", ('.csv', '.xlsx'))
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

if __name__ == "__main__":
    main()