import asyncio
import json
import requests
import websockets

clients = set()  # Track connected clients

# Your bus class remains the same (you can keep or adjust as needed)
class Bus:
    def __init__(self, stop_count, long, lat, stops_list=None):
        self.stop_count = stop_count
        self.long = long
        self.lat = lat
        self.stops_list = stops_list or []

    @property
    def stops_list_prop(self):
        return self.stops_list

    @stops_list_prop.setter
    def stops_list_prop(self, *args):
        new_stop = [[lng, lat] for lng, lat in args]
        if not self.stops_list:
            self.stops_list = new_stop
        else:
            self.stops_list.append(new_stop[0])
        return self.stops_list

bus1 = Bus(4, 76.369777, 30.354376)

choice = None
def bus_choice(bus_):
    global choice
    choice = Bus(bus_.stop_count, bus_.long, bus_.lat, bus_.stops_list)
    return choice

bus_choice(bus1)
choice.stops_list_prop = (76.3922, 30.33625)

# Helper function: call OpenRouteService API to get distances
def get_distances(stops):
    headers = {
        "Authorization": "eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6IjU5YjczMDZjNTI5MjQ2NThiZGFlYzA5Yjg0YWFiZGQ0IiwiaCI6Im11cm11cjY0In0=",
        "Content-Type": "application/json"
    }
    data = {
        "locations": stops,
        "id": "request",
        "metrics": ["distance"],
        "sources": [0],
        "units": "km"
    }
    response = requests.post("https://api.openrouteservice.org/v2/matrix/driving-car", headers=headers, json=data)
    return response.json()['distances'][0]  # return the distances row

# WebSocket handler coroutine
async def handler(websocket, path):
    # Register client
    clients.add(websocket)
    try:
        async for message in websocket:
            # Receive live position update from send.html
            data = json.loads(message)

            # Update current bus location
            choice.long = data.get('longitude', choice.long)
            choice.lat = data.get('latitude', choice.lat)

            # Define stops: start (bus current) + fixed stops
            stops = [[choice.long, choice.lat], [76.3922, 30.33625], [76.41, 30.35], [76.6073, 30.4693], [76.75, 30.55]]

            # Get updated distance data
            distances = get_distances(stops)

            # Example processing: estimated speed and ETA calculation (customize as needed)
            speed = data.get('speed')
            if not speed or speed == 0:  # if speed unavailable, assign default
                speed = 30  # assuming 30 km/h default speed

            # Calculate ETA to last stop in minutes
            distance_to_end = distances[-1]
            eta_minutes = (distance_to_end / speed) * 60 if speed else None

            # Build data to broadcast
            broadcast_data = {
                "latitude": choice.lat,
                "longitude": choice.long,
                "speed": speed,
                "eta": round(eta_minutes, 1) if eta_minutes else None,
                "timestamp": data.get('timestamp')
            }

            # Broadcast updated data to all other clients
            for client in clients:
                if client != websocket and client.open:
                    await client.send(json.dumps(broadcast_data))

    except websockets.ConnectionClosed:
        pass
    finally:
        clients.remove(websocket)

async def main():
    async with websockets.serve(handler, "0.0.0.0", 8765):
        print("WebSocket Server listening on port 8765...")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    bus_choice(bus1)  # initialize choice bus
    asyncio.run(main())
