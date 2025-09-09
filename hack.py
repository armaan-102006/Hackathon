import asyncio
import requests
import websockets
from websockets.asyncio.server import serve
import json

client_connections = set()

#use a dict instead of set and use a forloop to constantly update the bus prefrences. forloop listens continously.
global initial_distance,distance
distance=None
initial_distance=None
async def bus_handler(websocket):
    global initial_distance,distance,bus1
    async for coords in websocket:
        coords=json.loads(coords)
        print(coords)
        #later we will assign different id's to each  
        bus1=bus(4,int(coords['longitude']), int(coords['latitude']),[[coords['longitude'],coords['latitude']],[76.3922, 30.33625], [76.41, 30.35],[76.6073, 30.4693], [76.75, 30.55]])
        bus_choice(bus1)
        
        headers = {"Authorization":"eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6IjU5YjczMDZjNTI5MjQ2NThiZGFlYzA5Yjg0YWFiZGQ0IiwiaCI6Im11cm11cjY0In0="
,"Content-Type": "application/json"}
        
        data={"locations":choice.stops_list,"id":"request","metrics":["distance"],"sources":[0],"units":"km"}
        request=requests.post("https://api.openrouteservice.org/v2/matrix/driving-car",headers=headers,json=data)
        content=request.json()

        distance=[i for i in content['distances'][0]]
        set_intial_distance()
        distance_percent=distance_percentage()
        progress=progression()
        times=[]
        dist=[]
        for i in range(1,choice.stop_count+1):
            tim,dista=stop_details(i)
            times.append(tim)
            dist.append(dista)

        xyz={"distance":dist,"time":times,"percent_covered":distance_percent,"stop_count":choice.stop_count}

        if client_connections:
            await asyncio.gather(*(client.send(json.dumps(xyz)) for client in client_connections))
            print("Forwarded to clients")
    await websocket.wait_closed()

async def client_handler(websocket):
    print("client connected")
    client_connections.add(websocket)
    try:
        await websocket.wait_closed()
    finally:
        print("client diconnected")
        client_connections.remove(websocket)

async def handler(websocket):
    path=websocket.request.path
    if path=="/client":
        await client_handler(websocket)
    elif path=="/bus":
        await bus_handler(websocket)


class bus:
    def __init__(self,stop_count, long, lat,stops_list=None):
        self.stop_count=stop_count
        self.long=long
        self.lat=lat
        self.stops_list=stops_list
    
def bus_choice(bus_):
    global choice
    choice=bus(bus_.stop_count,bus_.long,bus_.lat,bus_.stops_list)
    return choice

def set_intial_distance():
    global initial_distance
    if initial_distance is None:
        initial_distance=distance
        return initial_distance

def distance_percentage():
    total_distance=initial_distance[len(initial_distance)-1]
    distance_percentage=[(stop_distance/total_distance)*100 for stop_distance in initial_distance]
    return distance_percentage


def progression():
    progress=[initial-current for current,initial in zip(distance,initial_distance)]
    progress_percentage=(progress[len(progress)-1]/initial_distance[len(initial_distance)-1])*100
    return progress_percentage

def stop_details(i):
    speed=2
    dist=distance[i]
    time=dist/speed
    return time,dist



async def main():
    async with serve(handler,"0.0.0.0", 5000) as server:
        await server.serve_forever()

if __name__=="__main__":
    asyncio.run(main())
