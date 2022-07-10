import time
import os
import copy
import io

import streamlit as st
import numpy as np
import pandas as pd

import plotly
from plotly import graph_objects as go
from plotly import figure_factory as ff

# take csv input
st.header("Choose the .csv file")

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
     # Can be used wherever a "file-like" object is accepted:
     st.subheader("The first five rows of your entered file are shown :")
     dataframe = pd.read_csv(uploaded_file, index_col = "Date", parse_dates=["Date"])
    #  dataframe_edited = pd.read_csv(uploaded_file)
     st.write(dataframe.head())
else:
    st.write("Please upload a valid .csv file")

if uploaded_file is not None:
    option = st.selectbox('Do you want to see the monthly closing trends of stock price?', ['No', 'Yes'])
    if option == 'Yes':
        # data = dataframe[["Date", "Close"]]
        trace1 = go.Scatter(x = dataframe.index, y = dataframe["Close"].asfreq('M').interpolate(), name = 'monthly closing price trend')
        trace2 = go.Scatter(x = dataframe.index, y = dataframe["Close"].asfreq('M').interpolate().shift(10), name = 'monthly closing price trend - lagged')
        layout = go.Layout(title = 'Monthly closing price trend - Raw and Lagged')
        fig = go.Figure(data = [trace1, trace2], layout = layout)
        st.plotly_chart(fig, use_container_width=True)