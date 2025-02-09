
import pytest

from event_bus import EventBus, Topic


@pytest.mark.asyncio(loop_scope='function')
async def test_single_subscription():
    """Test that a single subscriber receives the published event."""
    event_bus = EventBus()
    received_events = []

    async def mock_callback(event_data):
        received_events.append(event_data)

    event_bus.subscribe(Topic.LOG_EVENT, mock_callback)
    await event_bus.publish(Topic.LOG_EVENT, "Test Event")

    assert received_events == ["Test Event"], "Subscriber did not receive the event"

@pytest.mark.asyncio(loop_scope='function')
async def test_multiple_subscriptions():
    """Test that multiple subscribers receive the same event."""
    event_bus = EventBus()
    received_events_1 = []
    received_events_2 = []

    async def callback_1(event_data):
        received_events_1.append(event_data)

    async def callback_2(event_data):
        received_events_2.append(event_data)

    event_bus.subscribe(Topic.LOG_EVENT, callback_1)
    event_bus.subscribe(Topic.LOG_EVENT, callback_2)

    await event_bus.publish(Topic.LOG_EVENT, "Test Event")

    assert received_events_1 == ["Test Event"], "First subscriber did not receive the event"
    assert received_events_2 == ["Test Event"], "Second subscriber did not receive the event"

@pytest.mark.asyncio(loop_scope='function')
async def test_no_event_for_unsubscribed_topic():
    """Test that an event published to an unregistered topic does not trigger callbacks."""
    event_bus = EventBus()
    received_events = []

    async def mock_callback(event_data):
        received_events.append(event_data)

    event_bus.subscribe(Topic.LOG_EVENT, mock_callback)

    # Publish to a non-existent topic
    await event_bus.publish("OTHER_TOPIC", "This should not be received")

    assert not received_events, "Event was incorrectly received for an unsubscribed topic"

@pytest.mark.asyncio(loop_scope='function')
async def test_no_subscribers():
    """Test that publishing an event with no subscribers does not cause errors."""
    event_bus = EventBus()
    try:
        await event_bus.publish(Topic.LOG_EVENT, "Test Event")
    except Exception as e:
        pytest.fail(f"Publishing with no subscribers raised an error: {e}")
