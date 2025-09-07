import asyncio
import json
import requests
import websockets

clients = set()  # Track connected clients

# ... Bus class and other code remains unchanged ...

async def handler(websocket):  # Remove 'path' argument
    clients.add(websocket)
    try:
        async for message in websocket:
            data = json.loads(message)
            # Update bus details etc.
            choice.long = data.get('longitude', choice.long)
            choice.lat = data.get('latitude', choice.lat)

            stops = [[choice.long, choice.lat], [76.3922, 30.33625], [76.41, 30.35], [76.6073, 30.4693], [76.75, 30.55]]

            distances = get_distances(stops)

            speed = data.get('speed')
            if not speed or speed == 0:
                speed = 30

            distance_to_end = distances[-1]
            eta_minutes = (distance_to_end / speed) * 60 if speed else None

            broadcast_data = {
                "latitude": choice.lat,
                "longitude": choice.long,
                "speed": speed,
                "eta": round(eta_minutes, 1) if eta_minutes else None,
                "timestamp": data.get('timestamp')
            }

            # Broadcast to all clients (excluding sender if desired)
            for client in clients:
                if client != websocket and not client.closed:
                    await client.send(json.dumps(broadcast_data))

    except websockets.ConnectionClosed:
        pass
    finally:
        clients.remove(websocket)

async def main():
    async with websockets.serve(handler, "0.0.0.0", 8765):  # handler takes only websocket now
        print("WebSocket Server listening on port 8765...")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    bus_choice(bus1)
    asyncio.run(main())
