import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
import joblib

df = pd.read_csv('MSFT.csv', parse_dates=['Date'])
training_set = df[["Close"]].values[:-60, 0].reshape(-1, 1)
test_set = sample_test = df[["Close"]].values[-60:, 0].reshape(-1, 1)

sc = StandardScaler()
training_set_scaled = sc.fit_transform(training_set)
joblib.dump(sc, 'scaler.sav')
test_set_scaled = sc.transform(test_set)

X_train = []
y_train = []
for i in range(60,training_set_scaled.shape[0]):
    X_train.append(training_set_scaled[i-60:i,0])
    y_train.append(training_set_scaled[i,0])
X_train, y_train = np.array(X_train), np.array(y_train)
X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)
