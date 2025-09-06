import asyncio
import requests
import websockets
from websockets.asyncio.server import serve


class bus:
    def __init__(self,stop_count, long, lat,stops_list=[]):
        self.stop_count=stop_count
        self.long=long
        self.lat=lat
        self.stops_list=stops_list
    
    @property
    def stops__list(self):
        return self.stops_list
    
    @stops__list.setter#for adding more stops in total stops
    def stops__list(self,*args):
        #assert len(args)==1
        new_stop=[[long,lat] for long,lat in args]
        if self.stops_list==[]:
            self.stops_list=new_stop
        else:
            self.stops_list.append(new_stop[0])
        return self.stops_list

global bus1
bus1=bus(4, 76.369777, 30.354376)


def bus_choice(bus_):
    global choice
    choice=bus(bus_.stop_count,bus_.long,bus_.lat)
    return choice

bus_choice(bus1)

choice.stops__list=(76.3922, 30.33625)



async def values(websocket):
    def choose_stop(i):
        return i

    coords = await websocket.recv()
    start=[choice.long,choice.lat]
    stops=[start,[76.3922, 30.33625], [76.41, 30.35],[76.6073, 30.4693], [76.75, 30.55]]#places where bus will stop

    headers = {"Authorization":"eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6IjU5YjczMDZjNTI5MjQ2NThiZGFlYzA5Yjg0YWFiZGQ0IiwiaCI6Im11cm11cjY0In0="
    ,"Content-Type": "application/json"}

    initial_distance=None

    data={"locations":stops,"id":"request","metrics":["distance"],"sources":[0],"units":"km"}
    request=requests.post("https://api.openrouteservice.org/v2/matrix/driving-car",headers=headers,json=data)
    content=request.json()

    distance=[i for i in content['distances'][0]]

    if initial_distance is None:
        initial_distance=distance

    def progression():
        progress=[initial-current for current,initial in zip(distance,initial_distance)]
        progress_percentage=(progress(len(progress))/initial_distance(len(initial_distance)))*100
        return progress_percentage

    speed=2

    def stop_details(i):
        dist=distance[i]
        time=dist/speed
        return time,dist

