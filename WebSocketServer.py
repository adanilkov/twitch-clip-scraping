import asyncio
import websockets
import json

async def echo(websocket, path):
    async for message in websocket:
        data = json.loads(message)
        print(f"Received message: {data}")
        if data.get('type') == 'stream.online':
            print(f"Streamer {data['event']['broadcaster_user_name']} is live!")

start_server = websockets.serve(echo, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
