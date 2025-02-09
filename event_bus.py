import logging
from enum import Enum

logger = logging.getLogger(__name__)


class Topic(Enum):
    LOG_EVENT = 1


class EventBus:
    def __init__(self):
        self.subscribers = {}

    def subscribe(self, topic: Topic, callback):
        if topic not in self.subscribers:
            self.subscribers[topic] = []
        self.subscribers[topic].append(callback)

    async def publish(self, topic, event_data):
        if topic in self.subscribers:
            for callback in self.subscribers[topic]:
                await callback(event_data)
                logger.debug(f"Published {event_data} to {topic} ")


event_bus = EventBus()
