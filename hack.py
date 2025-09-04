# visit UG Activity Space-I
import asyncio
import requests
import websockets
'''
async def values(websocket):
    coords = await websocket.recv()
    print(coords)
'''
class bus:
    def __init__(self,stop_count, long, lat):
        self.stop_count=stop_count
        self.long=long
        self.lat=lat

bus1=bus(3, 76.369777, 30.354376)

long = 76.3922#aassuming real time longitude of bus
lat = 30.33625#aassuming real time latitude of bus
start=[long,lat]
stops=[[76.3922, 30.33625], [76.41, 30.35], [76.75, 30.55], [76.6073, 30.4693]]#places where bus will stop

speed=10#assuming real time speed of bus

def destination(i):
    return stops[i]

waypoints="|".join([f"{long},{lat}" for lat,long in stops])
request1=requests.get(f"https://api.geoapify.com/v1/routing?waypoints={waypoints}&mode=bus&format=json&apiKey=4fe2472c1b414c14bd0cd38015886bff")
content=request1.json()
results=content['results']
one=results[0]
geometry=one['geometry']
coordinates1=[[point['lat'],point['lon']] for point in geometry[0]]
coordinates2=[[point['lat'],point['lon']] for point in geometry[1]]
leg=one['legs']

def time_estimate(i):#estimated time to reach a stop
    stop=leg[i]
    distance=int(stop['distance'])/1000
    time = distance/speed
    return time

stops=[[stop[1],stop[0]] for stop in stops]#because geoapify takes input in format[longitude,latitude] while it's opposite in folium
start=[lat,long]

