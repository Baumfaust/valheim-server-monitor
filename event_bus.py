import asyncio

class EventBus:
    def __init__(self):
        self.queue = asyncio.Queue()
        self.subscribers = {}

    async def publish(self, event_type, data):
        """Publish an event"""
        await self.queue.put((event_type, data))

    def subscribe(self, event_type, callback):
        """Subscribe to an event"""
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(callback)

    async def start_listening(self):
        """Continuously listen for new events"""
        while True:
            event_type, data = await self.queue.get()
            if event_type in self.subscribers:
                for callback in self.subscribers[event_type]:
                    await callback(data)

event_bus = EventBus()
