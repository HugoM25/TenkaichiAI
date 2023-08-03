'''
Format the data to be used for the suêrvised training of the model
--> Read the data from the json file
--> Preprocess the data if necessary
--> Split the data into input and output arrays
--> Split the data into training and testing sets (80% training, 10% testing, 10% validation)
'''

import json
import numpy as np
import argparse


def save_header_and_data(filename, data_header, data_arr, method) -> None : 
    '''
    Save the header and the data in the csv file
    @param data_header [list] : header of the data
    @param data_arr [numpy.array] : data to save
    @return : None
    '''
    open_mode = 'w'

    if method == 'add' :
        open_mode = 'a'
    

    with open(filename, open_mode) as file:
        header = ','.join(data_header)
        file.write(header + '\n')
        np.savetxt(file, data_arr, delimiter=',')


def main(filename, foldername, method) :

    # Read and preprocess the data
    with open(filename, 'r') as file:
        data = json.load(file)

    # Split the data into input and output arrays
    X = np.array([record['obs'] for record in data])
    Y = np.array([record['controller'] for record in data])

    # Clean the data, keep only the values of the features
    features_obs = [ key for key in data[0]['obs'].keys()]
    features_controller = [ key for key in data[0]['controller'].keys()]

    X = np.array([ [record['obs'][feature] for feature in features_obs] for record in data])
    Y = np.array([ [record['controller'][feature] for feature in features_controller] for record in data])

    # Split the data into training and testing sets (80% training, 10% testing, 10% validation)

    # Shuffle the data
    np.random.shuffle(X)
    np.random.shuffle(Y)

    # Split the data into training, testing and validation sets
    X_train = X[:int(len(X)*0.8)]
    Y_train = Y[:int(len(Y)*0.8)]

    X_test = X[int(len(X)*0.8):int(len(X)*0.9)]
    Y_test = Y[int(len(Y)*0.8):int(len(Y)*0.9)]

    X_val = X[int(len(X)*0.9):]
    Y_val = Y[int(len(Y)*0.9):]

    # Save the data in the folder in .csv files

    save_header_and_data(foldername + '/train/input.csv', features_obs, X_train, method)
    save_header_and_data(foldername + '/train/output.csv', features_controller, Y_train, method)

    save_header_and_data(foldername + '/test/input.csv', features_obs, X_test, method)
    save_header_and_data(foldername + '/test/output.csv', features_controller, Y_test, method)

    save_header_and_data(foldername + '/validation/input.csv', features_obs, X_val, method)
    save_header_and_data(foldername + '/validation/output.csv', features_controller, Y_val, method)

    print('Data saved in the folder' + foldername)



if __name__ == "__main__":

    # Parse the command line arguments to get the filename
    parser = argparse.ArgumentParser()

    # Get the filename
    parser.add_argument('--filename', type=str, default='raw_data.json', help='Name of the file containing the data')

    # Get the folder name
    parser.add_argument('--foldername', type=str, default='data', help='Name of the folder to save the data in')

    # Get the method to use (add - replace)
    parser.add_argument('--method', type=str, default='add', help='Method to use to format the data') 

    args = parser.parse_args()

    main(args.filename, args.foldername, args.method)
