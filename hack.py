import folium
import requests
from requests.structures import CaseInsensitiveDict

headers = CaseInsensitiveDict()
headers["Content-Type"] = "application/json"

'''
ip_coord=requests.get(f"https://api.geoapify.com/v1/ipinfo?ip=2401:4900:851c:a7cc:f8f0:fbff:feae:bd69&apiKey=4fe2472c1b414c14bd0cd38015886bff")
content=ip_coord.json()

coords=content['location']
'''
long = 76.3922
lat = 30.33625
start=[long,lat]
stops=[[76.3922, 30.33625], [76.41, 30.35], [76.75, 30.55], [76.6073, 30.4693]]
'''
data={
  "mode": "drive",
  "agents": [
    {"start_location": start, "end_location": start, "pickup_capacity": 50}
  ],
  "jobs": [
    {"location": stops[0], "duration": 300, "pickup_amount": 10},
    {"location": stops[1],    "duration": 300, "pickup_amount": 15},
    {"location": stops[2],  "duration": 300, "pickup_amount": 12},
    {"location": stops[3],    "duration": 300, "pickup_amount": 8}
  ]
}

request=requests.post("https://api.geoapify.com/v1/routeplanner?apiKey=4fe2472c1b414c14bd0cd38015886bff",headers=headers, json=data)
content=request.json()
features=content['features']
one=features[0]
properties=one['properties']
waypoints=properties['waypoints']
coords=[waypoint['original_location'] for waypoint in waypoints]
coords=[[coord[1],coord[0]] for coord in coords]'''

waypoints="|".join([f"{long},{lat}" for lat,long in stops])
requests=requests.get(f"https://api.geoapify.com/v1/routing?waypoints={waypoints}&mode=bus&format=json&apiKey=4fe2472c1b414c14bd0cd38015886bff")
content=requests.json()
results=content['results']
one=results[0]
geometry=one['geometry']
coordinates1=[[point['lat'],point['lon']] for point in geometry[0]]
coordinates2=[[point['lat'],point['lon']] for point in geometry[1]]



stops=[[stop[1],stop[0]] for stop in stops]#because geoapify takes input in format[longitude,latitude] while it's opposite in folium
start=[lat,long]

m = folium.Map([45.35, -121.6972], zoom_start=12)
for stop in stops:
    folium.Marker(location=stop,tooltip="",popup="Bus Stop",icon=folium.Icon(icon="bus", prefix="fa", color="red"),).add_to(m)

folium.Marker(location=start,tooltip="Bus",popup="Bus1",icon=folium.Icon(icon="car", prefix="fa", color="blue"),).add_to(m)
folium.PolyLine(coordinates1, tooltip="Path").add_to(m)
folium.PolyLine(coordinates2, tooltip="Path").add_to(m)
m.save("footprint.html")

