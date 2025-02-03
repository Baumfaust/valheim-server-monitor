import pytest
import asyncio
from event_bus import EventBus

@pytest.mark.asyncio(loop_scope='function')
async def test_event_bus_publish_and_subscribe():
    event_bus = EventBus()

    # A flag to check if the event is received
    event_received = []

    # A simple callback function for subscribers
    async def event_callback(data):
        event_received.append(data)

    # Subscribe to an event
    event_bus.subscribe("test_event", event_callback)

    # Publish the event
    await event_bus.publish("test_event", "event_data")

    # Simulate the event bus listening in a task
    listener_task = asyncio.create_task(event_bus.start_listening())

    # Wait for the event to be processed
    await asyncio.sleep(0.1)

    # Check if the event data was received by the callback
    assert "event_data" in event_received

    # Cancel the listener task as we are done
    listener_task.cancel()


@pytest.mark.asyncio(loop_scope='function')
async def test_event_bus_multiple_subscribers():
    event_bus = EventBus()

    # Flags to check if events are received by multiple subscribers
    subscriber1_received = []
    subscriber2_received = []

    # Subscriber 1 callback function
    async def subscriber1_callback(data):
        subscriber1_received.append(data)

    # Subscriber 2 callback function
    async def subscriber2_callback(data):
        subscriber2_received.append(data)

    # Subscribe both callbacks to the same event
    event_bus.subscribe("test_event", subscriber1_callback)
    event_bus.subscribe("test_event", subscriber2_callback)

    # Publish the event
    await event_bus.publish("test_event", "event_data")

    # Simulate the event bus listening in a task
    listener_task = asyncio.create_task(event_bus.start_listening())

    # Wait for the event to be processed
    await asyncio.sleep(0.1)

    # Assert that both subscribers received the event
    assert "event_data" in subscriber1_received
    assert "event_data" in subscriber2_received

    # Cancel the listener task as we are done
    listener_task.cancel()


@pytest.mark.asyncio(loop_scope='function')
async def test_event_bus_no_subscribers():
    event_bus = EventBus()

    # Publish an event with no subscribers
    await event_bus.publish("test_event", "event_data")

    # Simulate the event bus listening in a task
    listener_task = asyncio.create_task(event_bus.start_listening())

    # Since there are no subscribers, it should not receive anything
    await asyncio.sleep(0.1)

    # Cancel the listener task as we are done
    listener_task.cancel()
