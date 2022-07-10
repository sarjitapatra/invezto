import pandas as pd

df = pd.read_csv('MSFT.csv')
df['Close'].asfreq('M').interpolate()