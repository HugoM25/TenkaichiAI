import asyncio
import threading
import json
from dolphin import savestate, controller, memory


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
    


async def handle_client(reader, writer):
    while True:
        data = await reader.read(1024)
        if not data:
            break
        message = data.decode()
        print("Received:", message)

        # Format data to JSON
        req_json = json.loads(message)
        response = ""
        if req_json['action'] == 'reset':
            # Reset the emulator
            reset()
            response = "{'status':'ok'}"
        elif req_json['action'] == 'get_observation':
            # Get the observation
            observations = get_observation()
            print(observations)
            if len(observations) == 0 :
                response = "{'status':'error'}"
            else :
                response = "{'status':'ok', 'observation':" + json.dumps(observations) + "}}"
        else :
            # Invalid action
            print('Invalid action')
            response = "{'status':'error'}"

        writer.write(response.encode())
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

if __name__ == "__main__":
    threading.Thread(target=start_server).start()
