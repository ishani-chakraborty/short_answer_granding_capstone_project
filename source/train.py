from __future__ import print_function

import argparse
import os
import pandas as pd
from source.utils import generate_data

from sklearn.externals import joblib
from keras.layers.core import Dropout
from keras.models import Sequential
from keras.layers import Dense, Embedding
from keras.layers import LSTM

from sklearn.linear_model import LinearRegression
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier


# Provided model load function
def model_fn(model_dir):
    """Load model from the model_dir. This is the same model that is saved
    in the main if statement.
    """
    print("Loading model.")

    # load using joblib
    model = joblib.load(os.path.join(model_dir, "model.joblib"))
    print("Done loading model.")

    return model


if __name__ == '__main__':
    # All of the model parameters and training parameters are sent as arguments
    # when this script is executed, during a training job

    # Here we set up an argument parser to easily access the parameters
    parser = argparse.ArgumentParser()

    # SageMaker parameters, like the directories for training data and saving models; set automatically
    # Do not need to change
    parser.add_argument('--output-data-dir', type=str, default=os.environ['SM_OUTPUT_DATA_DIR'])
    parser.add_argument('--model-dir', type=str, default=os.environ['SM_MODEL_DIR'])
    parser.add_argument('--data-dir', type=str, default=os.environ['SM_CHANNEL_TRAINING'])
    parser.add_argument('--epochs', type=int, default=200)
    parser.add_argument('--embedding_size', type=int, default=30)
    parser.add_argument('--lstm_size', type=int, default=100)
    parser.add_argument('--dropout', type=float, default=0.2)
    parser.add_argument('--optimizer', type=str, default='adam')


    # args holds all passed-in arguments
    args = parser.parse_args()

    print(f"epochs={args.epochs} embedding_size={args.embedding_size} lstm_size={args.lstm_size}")

    # Read in csv training file
    training_dir = args.data_dir
    train_data = pd.read_csv(os.path.join(training_dir, "train.csv"), header=None, names=None)

    # Labels are in the first column
    train_y = train_data.iloc[:, 0]
    train_x = train_data.iloc[:, 1:]

    # Build Model
    model = Sequential()
    model.add(Embedding(len(from_num_dict), 30, input_length=max_length))
    model.add(Dropout(0.2))
    model.add(LSTM(100, return_sequences=False, input_shape=(max_length,)))
    model.add(Dropout(0.2))
    model.add(Dense(1, activation="linear"))
    model.compile(optimizer='adam', loss='mean_squared_error', metrics=['acc'])


    # Train the model
    model.fit(train_x, train_y)

    ## --- End of your code  --- ##

    # Save the trained model
    joblib.dump(model, os.path.join(args.model_dir, "model.joblib"))