
'''
This file is the server that will be used to communicate with the emulator.
'''

import asyncio
import socket
import threading
import queue
from dolphin import event, memory, controller, savestate 
import json

'''
Global variables
----------------
'''

input_action_queue = queue.Queue()
current_inputs = controller.get_gc_buttons(0)
'''
Functions activable from the server
-----------------------------------
'''
def reset() :
    '''
    Load the save state in slot 1 (the one that is used for the training)
    '''
    savestate.load_from_slot(1)
    print("Resetting the emulator")

def get_observation() -> [float] :
    '''
    Get the current observation
    @return: The observation
    '''
    try : 
        return [
            memory.read_u8(0x92343BEF), # Timer 
            memory.read_u16(0x92334CA2), # Health Player 1
            memory.read_u16(0x92336D42), # Health Player 2
            memory.read_f32(0x90F9A570), # X Player 1
            memory.read_f32(0x90F9A004), # Y Player 1
            memory.read_f32(0x90F99F48), # Z Player 2
            memory.read_f32(0x90F9B5D0), # X Player 2
            memory.read_f32(0x90F9B694), # Y Player 2
            memory.read_f32(0x90F9B608), # Z Player 2
            memory.read_u8(0x9233501F), # Attack base cnt P1
            memory.read_u8(0x923370BF), # Attack base cnt P2
            memory.read_u8(0x923350A3), # Attack ki cnt P1,
            memory.read_u8(0x92337143), # Attack ki cnt P2,
            memory.read_u32(0x92344C9C), # Damage combo taken by P1
            memory.read_u32(0x9233709C), # Damage combo taken by P2
            ]
    except :
        return []
    

def change_current_inputs(new_inputs) -> None:
    '''
    Execute the given input
    @param new_inputs: The input to execute as json
    '''

    # Change the curr input to the new inputs map
    current_inputs["A"] = new_inputs["A"]
    current_inputs["B"] = new_inputs["B"]
    current_inputs["X"] = new_inputs["X"]
    current_inputs["Y"] = new_inputs["Y"]
    current_inputs["Z"] = new_inputs["Z"]
    current_inputs["L"] = new_inputs["L"]
    current_inputs["R"] = new_inputs["R"]
    current_inputs["Start"] = new_inputs["Start"]
    current_inputs["StickX"] = new_inputs["StickX"]
    current_inputs["StickY"] = new_inputs["StickY"]
    current_inputs["CStickX"] = new_inputs["CStickX"]
    current_inputs["CStickY"] = new_inputs["CStickY"]
    current_inputs["TriggerLeft"] = new_inputs["TriggerLeft"]
    current_inputs["TriggerRight"] = new_inputs["TriggerRight"]

    controller.set_gc_buttons(0, current_inputs)

def apply_input() -> None:
    '''
    Apply the current input
    '''
    controller.set_gc_buttons(0, current_inputs)
    
async def handle_client(reader, writer):
    while True:
        data = await reader.read(1024)
        if not data:
            break
        message = data.decode()
        
        # Handle the message here
        print("Message received !")

        req_json = json.loads(message)

        if req_json["action"] == "reset" :
            reset()
            server_response = '{"status":"ok"}'

        elif req_json["action"] == "get_observation" :
            obs = get_observation()
            server_response = '{"observation":' + json.dumps(obs) + '}'
        
        elif req_json["action"] == "set_inputs" :
            # Add the input to the queue (to be processed at the next frame)
            input_action_queue.put(req_json["inputs"])
            server_response = '{"status":"ok"}'

        writer.write(server_response.encode())
        await writer.drain()
    writer.close()


def start_server():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    server_coro = asyncio.start_server(handle_client, 'localhost', 12345)
    server = loop.run_until_complete(server_coro)
    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()

    

def execute_input_queue():
    
    # If there is new inputs to execute change the current inputs
    if not input_action_queue.empty():
        change_current_inputs(input_action_queue.get())
    
    # Apply the current inputs
    apply_input()


if __name__ == "__main__":

    threading.Thread(target=start_server).start()

    while True :
        # Wait for the next frame
        await event.frameadvance()
        # Handle the inputs
        execute_input_queue()

    