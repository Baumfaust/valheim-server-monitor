import pytest

import event_bus
from monitor.valheim_log_parser import (
    PlayerJoined,
    ValheimSession,
    handle_message,
    parse_player_join_message,
    parse_session_message,
    parse_valheim_log, ServerStarted, sever_started_version_message,
)


def test_parse_session_message():
    log_message = ('Session "MyValheimSession" with join code 12345 and IP 192.168.1.100:2456 '
                   'is active with 10 player(s)')

    result = parse_session_message(log_message)

    assert result is not None
    assert isinstance(result, ValheimSession)
    assert result.session_name == "MyValheimSession"
    assert result.join_code == 12345
    assert result.address == "192.168.1.100:2456"
    assert result.player_count == 10


def test_sever_started_version_message():
    log_message = '02/09/2025 23:01:19: Valheim version: l-0.219.16 (network version 32)'

    result = sever_started_version_message(log_message)

    assert result is not None
    assert isinstance(result, ServerStarted)
    assert result.valheim_version == "0.219.16"

def test_parse_player_join_message():
    log_message = 'Console: <color=orange>Erwin</color>: <color=#FFEB04FF>I HAVE ARRIVED!</color>'

    result = parse_player_join_message(log_message)

    assert result is not None
    assert isinstance(result, PlayerJoined)
    assert result.player_name == "Erwin"




def test_parse_valheim_log_session():
    log_message = ('Session "MyValheimSession" with join code 12345 and IP 192.168.1.100:2456 '
                   'is active with 10 player(s)')

    result = parse_valheim_log(log_message)

    assert result is not None
    assert isinstance(result, ValheimSession)


def test_parse_valheim_log_player_join():
    log_message = 'Console: <color=orange>Erwin</color>: <color=#FFEB04FF>I HAVE ARRIVED!</color>'

    result = parse_valheim_log(log_message)

    assert result is not None
    assert isinstance(result, PlayerJoined)


def test_parse_valheim_log_no_match():
    log_message = "Some other log message"

    result = parse_valheim_log(log_message)

    assert result is None


@pytest.mark.asyncio(loop_scope='function')
async def test_handle_message_session(mocker):
    log_message = ('Session "MyValheimSession" with join code 12345 and IP 192.168.1.100:2456 '
                   'is active with 10 player(s)')

    mock_publish = mocker.patch('event_bus.EventBus.publish')  # Mock event_bus.publish

    await handle_message(log_message)

    log_entry = ValheimSession("MyValheimSession", 12345, "192.168.1.100:2456", 10)

    # Assert that the mock publish method was called with the correct arguments
    mock_publish.assert_called_once_with(event_bus.Topic.LOG_EVENT, log_entry)


@pytest.mark.asyncio(loop_scope='function')
async def test_handle_message_player_join(mocker):
    log_message = 'Console: <color=orange>Erwin</color>: <color=#FFEB04FF>I HAVE ARRIVED!</color>'

    mock_publish = mocker.patch('event_bus.EventBus.publish')  # Mock event_bus.publish

    await handle_message(log_message)

    log_entry = PlayerJoined("Erwin")

    # Assert that the mock publish method was called with the correct arguments
    mock_publish.assert_called_once_with(event_bus.Topic.LOG_EVENT, log_entry)


@pytest.mark.asyncio(loop_scope='function')
async def test_handle_message_no_match(mocker):
    log_message = "Some other log message"

    mock_publish = mocker.patch('event_bus.EventBus.publish')  # Mock event_bus.publish

    await handle_message(log_message)

    # Ensure that the publish method was not called
    mock_publish.assert_not_called()