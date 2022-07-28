import numpy as np 
import pandas as pd
import pandas_datareader.data as web
import datetime
from functools import reduce

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

#start and end dates
start = datetime.datetime(2019, 9, 15)
end = datetime.datetime(2021, 9, 15)

#for pulling stocks
def get_stock(ticker):
    data = web.DataReader(f"{ticker}", "yahoo", start, end)
    data[f'{ticker}'] = data["Adj Close"]
    data = data[[f'{ticker}']] 
    return data 

def combine_returns(tickers):
    data_frames = []
    for i in tickers:
        data_frames.append(get_stock(i))
        
    df_merged = reduce(lambda left, right: pd.merge(left, right, on = ['Date'], how = 'outer'), data_frames)
    return df_merged

#pulling stocks for different industries
stocks = ["MRNA", "PFE", "JNJ", "GOOGL", 
          "FB", "AAPL", "COST", "WMT", "KR", "JPM", 
          "BAC", "HSBC"]
portfolio = combine_returns(stocks)

nullin_df = pd.DataFrame(portfolio, columns = stocks)
print(nullin_df.isnull().sum())

portfolio.to_csv("portfolio.csv", index = False)
portfolio = pd.read_csv("portfolio.csv")