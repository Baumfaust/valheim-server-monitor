import asyncio
import logging

from event_bus import Topic, event_bus
from monitor.valheim_log_parser import (
    PlayerDied,
    PlayerJoined,
    PlayerLeft,
)
from prometheus_client import Counter, Gauge, start_http_server

logger = logging.getLogger(__name__)
ready_metrics_exporter = asyncio.Event()

online_players_total = Gauge("online_players_total", "Total number of players currently online")
player_status = Gauge("player_status", "Online status of individual players", ["player_name"])
player_death_count = Counter("player_death_count", "Death count per player", ["player_name"])


async def update_metrics(event_data):
    match event_data:
        case PlayerJoined(player_name):
            player_status.labels(player_name).set(1)
        case PlayerDied(player_name):
            player_death_count.labels(player_name).inc()
        case PlayerLeft(player_name):
            player_status.labels(player_name).set(0)
        case _:
            logger.warning("Unknown event type")


async def run_metrics_exporter():
    try:
        start_http_server(8000)
        topic = Topic.LOG_EVENT
        event_bus.subscribe(topic, update_metrics)
        logger.debug(f"Metrics exporter subscribed to {topic}")
        ready_metrics_exporter.set()
    except asyncio.CancelledError:
        logger.debug("Stopping metrics exporter")
        raise
