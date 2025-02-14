import pytest

import event_bus
from monitor.valheim_log_parser import (
    PlayerDied,
    PlayerJoined,
    PlayerLeft,
    ServerStarted,
    ServerStopped,
    ValheimSession,
    handle_message,
    parse_player_died_message,
    parse_player_joined_message,
    parse_player_left_message,
    parse_player_session_id_message,
    parse_session_message,
    parse_valheim_log,
    sever_started_version_message,
    sever_stopped_message,
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

def test_sever_stopped_message():
    log_message = '02/09/2025 23:26:30: Game - OnApplicationQuit'

    result = sever_stopped_message(log_message)

    assert result is not None
    assert isinstance(result, ServerStopped)

def test_parse_player_joined_message_en():
    log_message = 'Console: <color=orange>Erwin</color>: <color=#FFEB04FF>I HAVE ARRIVED!</color>'

    result = parse_player_joined_message(log_message)

    assert result is not None
    assert isinstance(result, PlayerJoined)
    assert result.player_name == "Erwin"

def test_parse_player_joined_message_de():
    log_message = 'Console: <color=orange>Baumfaust</color>: <color=#FFEB04FF>ICH BIN ANGEKOMMEN!</color>'

    result = parse_player_joined_message(log_message)

    assert result is not None
    assert isinstance(result, PlayerJoined)
    assert result.player_name == "Baumfaust"

def test_parse_player_died_message():
    log_message = ' 02/14/2025 21:07:48: Got character ZDOID from Baumfaust : 0:0'

    result = parse_player_died_message(log_message)

    assert result is not None
    assert isinstance(result, PlayerDied)
    assert result.player_name == "Baumfaust"

def test_parse_player_left_message():
    session_message = '02/14/2025 21:09:48: Got character ZDOID from Baumfaust : 1470032995:3'
    left_message = '02/14/2025 21:07:48: Destroying abandoned non persistent zdo 1470032995:743 owner 1470032995'

    parse_player_session_id_message(session_message)
    
    left_result = parse_player_left_message(left_message)

    assert left_result is not None
    assert isinstance(left_result, PlayerLeft)
    assert left_result.player_name == "Baumfaust"


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