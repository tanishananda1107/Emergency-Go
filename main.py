from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
import random

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# Emergency Request Model
# -------------------------
class EmergencyRequest(BaseModel):
    emergency_type: str
    location: str

active_requests = []

@app.post("/request-help")
def request_help(req: EmergencyRequest):

    request_id = len(active_requests) + 1

    emergency = {
        "id": request_id,
        "type": req.emergency_type,
        "location": req.location,
        "status": "Dispatched",
        "eta": "8 min"
    }

    active_requests.append(emergency)

    return emergency


@app.get("/requests")
def get_requests():
    return active_requests


# -------------------------
# Fake Live Tracking API
# -------------------------
@app.websocket("/track/{request_id}")
async def track(ws: WebSocket, request_id: int):
    await ws.accept()

    lat, lon = 12.9716, 77.5946  # start point

    while True:
        lat += random.uniform(0.0001, 0.0005)
        lon += random.uniform(0.0001, 0.0005)

        await ws.send_json({
            "lat": lat,
            "lon": lon
        })

        await asyncio.sleep(1)
