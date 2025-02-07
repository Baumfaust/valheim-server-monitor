import asyncio

class EventBus:
    def __init__(self):
        self.subscribers = {}
        self.ready_events = {}  # Track readiness of different components

    def subscribe(self, event_name, callback):
        if event_name not in self.subscribers:
            self.subscribers[event_name] = []
        self.subscribers[event_name].append(callback)
        print("Subscribed to", event_name)

    async def publish(self, event_name, event_data):
        if event_name in self.subscribers:
            for callback in self.subscribers[event_name]:
                await callback(event_data)
                print("Published", event_name)

    def register_ready_event(self, name):
        """Registers a readiness event that components will signal when ready."""
        self.ready_events[name] = asyncio.Event()
        print("Registered ready event", name)

    async def wait_for_all_ready(self):
        """Waits until all registered components signal readiness."""
        await asyncio.gather(*(event.wait() for event in self.ready_events.values()))

    def signal_ready(self, name):
        """Marks a component as ready."""
        if name in self.ready_events:
            self.ready_events[name].set()

event_bus = EventBus()
