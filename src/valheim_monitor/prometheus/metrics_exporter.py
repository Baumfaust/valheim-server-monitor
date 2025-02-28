import asyncio
import logging

from event_bus import Topic, event_bus
from monitor.valheim_log_parser import (
    PlayerDied,
    PlayerJoined,
    PlayerLeft,
    ServerStarted,
    ServerStopped,
)
from prometheus_client import Counter, Gauge, start_http_server

logger = logging.getLogger(__name__)
ready_metrics_exporter = asyncio.Event()

server_status = Gauge("valheim_server_status", "Online status of valheim server")
online_players_total = Gauge("valheim_online_players_total", "Total number of players currently online")
player_status = Gauge("valheim_player_status", "Online status of individual players", ["player_name"])
player_death_count = Counter("valheim_player_death_count", "Death count per player", ["player_name"])

async def update_metrics(event_data):
    try:
        match event_data:
            case ServerStarted():
                server_status.set(1)
            case ServerStopped():
                server_status.set(0)
            case PlayerJoined(player_name):
                logger.debug(f"Setting metric player joined: {player_name}")
                player_status.labels(player_name).set(1)
            case PlayerDied(player_name):
                logger.debug(f"Setting metric player died: {player_name}")
                player_death_count.labels(player_name).inc()
            case PlayerLeft(player_name):
                logger.debug(f"Setting metric player left: {player_name}")
                player_status.labels(player_name).set(0)
            case _:
                logger.warning("Unknown event type")
    except Exception as e:
        logger.error(f"Error updating metrics: {e}")

async def run_metrics_exporter():
    try:
        topic = Topic.LOG_EVENT
        event_bus.subscribe(topic, update_metrics)
        logger.debug(f"Metrics exporter subscribed to {topic}")
        ready_metrics_exporter.set()
        logger.debug("starting http server")
        start_http_server(8000)
        logger.debug("http server started on port 8000")

    except asyncio.CancelledError:
        logger.debug("Stopping metrics exporter")
        raise