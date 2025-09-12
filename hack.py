# visit UG Activity Space-I
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
        bus1=bus(4,coords['longitude'], coords['latitude'],coords['speed'],[[coords['longitude'],coords['latitude']],[76.359376, 30.353063], [76.365075, 30.353664],[76.367698, 30.353972], [76.371361, 30.354414]])
        bus_choice(bus1)
        
        headers = {"Authorization":"eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6IjU5YjczMDZjNTI5MjQ2NThiZGFlYzA5Yjg0YWFiZGQ0IiwiaCI6Im11cm11cjY0In0="
,"Content-Type": "application/json"}
        
        data={"locations":choice.stops_list,"id":"request","metrics":["distance"],"sources":[0],"units":"km"}
        request=requests.post("https://api.openrouteservice.org/v2/matrix/driving-car",headers=headers,json=data)
        content=request.json()

        distance=[i for i in content['distances'][0]]
        print(distance)
        set_intial_distance()
        distance_percent=distance_percentage()
        progress=progression()
        times=[]
        dist=[]
        for i in range(1,choice.stop_count+1):
            tim,dista=stop_details(i)
            times.append(tim)
            dist.append(dista)

        xyz={"distance":dist,"time":times,"percent_covered":distance_percent,'progress_percentage':progress,"stop_count":choice.stop_count,'stops':{'type':'stops','stop_coords':choice.stops_list}}

        if client_connections:
            print(xyz)
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
'''
async def map_handler(websocket):
    global choice
    print("map added")
    '''

async def handler(websocket):
    path=websocket.request.path
    if path=="/client":
        await client_handler(websocket)
    elif path=="/bus":
        await bus_handler(websocket)
    '''elif path=='/map':
        await map_handler(websocket)'''


class bus:
    def __init__(self,stop_count, long, lat,speed,stops_list=None):
        self.stop_count=stop_count
        self.long=long
        self.lat=lat
        self.stops_list=stops_list
        self.speed=speed
    
def bus_choice(bus_):
    global choice
    choice=bus(bus_.stop_count,bus_.long,bus_.lat,bus_.speed,bus_.stops_list)
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
    speed=choice.speed
    dist=distance[i]
    try:
        time=dist/speed
    except ZeroDivisionError:
        time="--"
        return time ,dist
    else:
        return time ,dist


async def main():
    async with serve(handler,"0.0.0.0", 5000) as server:
        await server.serve_forever()

if __name__=="__main__":
    asyncio.run(main())

#ascending order for distances
#distance will be a lsit of stops in correct order of their distance from least to most
#time will be an integer in terms of hours
#distance_percentage is the percentage of distance that a particular stop is at from the beginning out of total distance i.e. distance of last stop from beginning and it will be in list format and similar to distances will be in the correct required order.
