 
import aiohttp
import asyncio
from event_bus import event_bus

GRAFANA_URL = "http://your-grafana-server:8086/write?db=logdata"

async def send_to_grafana(event_data):
    async with aiohttp.ClientSession() as session:
        async with session.post(GRAFANA_URL, data=f"events,source=log value=1") as resp:
            print(f"Grafana response: {resp.status}")

async def handle_grafana_events():
    event_bus.subscribe("ServerOnlineEvent", send_to_grafana)
    event_bus.subscribe("PlayerJoined", send_to_grafana)
