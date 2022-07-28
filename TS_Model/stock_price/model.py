import dataset

from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout, Bidirectional

# build model
regressor = Sequential()
# First LSTM layer with Dropout regularisation
regressor.add(LSTM(units = 60, return_sequences = True, input_shape = (dataset.X_train.shape[1], 1)))
regressor.add(Dropout(0.2))
# Second LSTM layer
regressor.add(LSTM(units = 60,return_sequences = True))
regressor.add(Dropout(0.2))
# Third LSTM layer
regressor.add(LSTM(units = 60,return_sequences = True))
regressor.add(Dropout(0.2))
# Fourth LSTM layer
regressor.add(LSTM(units = 60))
regressor.add(Dropout(0.2))
# The output layer
regressor.add(Dense(units = 1))

# print parameters
regressor.summary()

# optimizer
opt = keras.optimizers.Adam(learning_rate = 0.01)

regressor.compile(optimizer = opt, loss = 'mean_squared_error')
# Fitting to the training set
regressor.fit(dataset.X_train, dataset.y_train, epochs = 30, batch_size = 64)

# save the model
regressor.save('mymodel.h5')