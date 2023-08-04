import asyncio
import threading
import json
from dolphin import savestate


def reset() :
    '''
    Load the save state in slot 1 (the one that is used for the training)
    '''
    savestate.load_from_slot(1)
    print("Resetting the emulator")

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
