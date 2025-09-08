import asyncio
import requests
import websockets
from websockets.asyncio.server import serve

async def values(websocket):
    path=websocket.request.path
    if path== "/bus":
        coords = await websocket.recv()
        print(coords)
    if path=="/client":
        await websocket.send(coords)
        print("coordinates sent")
