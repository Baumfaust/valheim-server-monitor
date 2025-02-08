import asyncio
import logging
from enum import Enum

logger = logging.getLogger(__name__)

class Topic(Enum):
     LOG_EVENT= 1


class EventBus:
    def __init__(self):
        self.subscribers = {}
        self.ready_events = {}  # Track readiness of different components

    def subscribe(self, topic: Topic, callback):
        if topic not in self.subscribers:
            self.subscribers[topic] = []
        self.subscribers[topic].append(callback)
        logger.debug(f"Subscribed to {topic}")

    async def publish(self, topic, event_data):
        if topic in self.subscribers:
            for callback in self.subscribers[topic]:
                await callback(event_data)
                logger.debug(f"Published {event_data} to {topic} ")

    def register_ready_event(self, name):
        """Registers a readiness event that components will signal when ready."""
        self.ready_events[name] = asyncio.Event()
        logger.debug("Registered ready event", name)

    async def wait_for_all_ready(self):
        """Waits until all registered components signal readiness."""
        await asyncio.gather(*(event.wait() for event in self.ready_events.values()))

    def signal_ready(self, name):
        """Marks a component as ready."""
        if name in self.ready_events:
            self.ready_events[name].set()

event_bus = EventBus()
