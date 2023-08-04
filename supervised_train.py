import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split


def load_data_from_csv(csv_path) :
    ''' 
    Load the data from the csv file
    @param csv_path [str] : path to the csv file
    @return data [numpy.array] : data loaded from the csv file
    '''
    data = pd.read_csv(csv_path)
    data = data.values
    return np.array(data)


def main() :

    # Load data from CSV files
    X_train = load_data_from_csv('data/train/input.csv')
    y_train = load_data_from_csv('data/train/output.csv')

    X_test = load_data_from_csv('data/test/input.csv')
    y_test = load_data_from_csv('data/test/output.csv')

    X_val = load_data_from_csv('data/validation/input.csv')
    y_val = load_data_from_csv('data/validation/output.csv')

    # Normalize the data (optional but can be helpful for some models)
    X_train = X_train / np.max(X_train)
    X_test = X_test / np.max(X_train)  # Normalize using training data max value
    X_val = X_val / np.max(X_train)  # Normalize using training data max value

    # Define the model
    model = tf.keras.models.Sequential([
        tf.keras.layers.Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
        tf.keras.layers.Dense(32, activation='relu'),
        tf.keras.layers.Dense(y_train.shape[1])  
    ])

    # Compile the model
    model.compile(optimizer='adam', loss='mean_squared_error')

    # Train the model
    history = model.fit(X_train, y_train, epochs=100, batch_size=32, validation_split=0.2)

    # Evaluate the model
    loss = model.evaluate(X_test, y_test)
    print("Test Loss:", loss)

    # Save the model
    model.save("trained_model")

    # Evaluate the model using the validation set
    loss = model.evaluate(X_val, y_val)
    print("Validation Loss:", loss)


if __name__ == "__main__":
    main()