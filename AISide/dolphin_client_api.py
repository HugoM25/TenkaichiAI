'''
This file is used to communicate with the dolphin_server.py file. It contains various functions that can be used to send commands to the server.
'''

import json
import socket
from controller_class import GCInputs

HOST = 'localhost'
PORT = 12345


def reset() -> None : 
    '''
    Ask the server to reset the emulator
    '''
    send_message('{"action":"reset"}')


def get_observation() -> [float] :
    '''
    Ask the server for the current observation
    '''
    data_server = send_message('{"action":"get_observation"}')

    # Format data to JSON
    data_json = json.loads(data_server)

    # Get the observation
    observation = data_json['observation']

    # Convert the observation to a list of floats
    observation = [float(i) for i in observation]

    return observation

def send_inputs(inputs) -> None :
    '''
    Set the inputs of the emulator
    @param inputs: The inputs to set
    '''

    send_message('{"action":"set_inputs", "inputs":' + json.dumps(vars(inputs)) + '}')


def send_message(message):
    '''
    Send a message to the server
    @param message: The message to send
    '''
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    client_socket.connect((HOST, PORT))

    client_socket.sendall(message.encode())  # Send the message to the server
    data_server = client_socket.recv(1024)  # Receive data from the server

    # Close the client socket
    client_socket.close()

    return data_server.decode()