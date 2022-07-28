import dataset

import numpy as np
import pandas as pd
import joblib
from plotly import graph_objects as go
from tensorflow import keras
from datetime import datetime

def pred():
    
    sc = joblib.load('scaler.sav')
    model = keras.models.load_model('mymodel.h5')
    custom_values = sc.transform(dataset.df.tail(60)[["Close"]]["Close"].values.reshape(-1, 1))
    for j in range(7):
        pred_cust = model.predict(custom_values[-60:, 0].reshape(1, 60, 1))
        print(custom_values[-60:, 0])
        print(pred_cust)
        custom_values = np.append(custom_values, pred_cust.reshape(1)).reshape(-1, 1)
        print(custom_values.shape)
        
    print(custom_values)
    ypred = sc.inverse_transform(custom_values[-60:, 0].reshape(-1, 1))
    print(ypred)
    return ypred

def plot_prediction(test_pred):

    fig = go.Figure()
    df = dataset.df.tail(60)["Date"].values
    fig.add_trace(go.Scatter(x = dataset[["Date"]].iloc[:-60, 0].values, y = dataset[["Close"]].iloc[:-60, 0].values))
    val = pd.to_datetime(dataset["Date"].iloc[-60])
    fig.add_trace(go.Scatter(x = [val + datetime.timedelta(days=idx) for idx in range(60)], y = test_pred[-60:, 0]))
    fig.update_layout(title = "Stock Price")
    fig.show()

def main():
    test_pred = pred()
    plot_prediction(test_pred)

if __name__ == "__main__":
    main()
