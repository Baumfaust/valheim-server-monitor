import logging
import re
from dataclasses import dataclass

from src.valheim_monitor.event_bus import Topic, event_bus

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class LogEntry:
    pass


@dataclass(frozen=True)
class ValheimSession(LogEntry):
    """Holds information parsed from a Valheim server log message."""

    session_name: str
    join_code: int
    address: str
    player_count: int

@dataclass(frozen=True)
class ServerStarted(LogEntry):
    valheim_version: str

@dataclass(frozen=True)
class ServerStopped(LogEntry):
    pass

@dataclass(frozen=True)
class PlayerJoined(LogEntry):
    player_name: str

@dataclass(frozen=True)
class PlayerDied(LogEntry):
    player_name: str

@dataclass(frozen=True)
class PlayerLeft(LogEntry):
    player_name: str

def parse_session_message(entry_message: str):
    pattern = (
        r"Session \"(.*?)\" with join code (\d+) and IP (.*?:\d+) "
        r"is active with (\d+) player\(s\)"
    )
    match = re.search(pattern, entry_message)
    if match:
        session_name = match.group(1)
        join_code = int(match.group(2))
        address = match.group(3)
        player_count = int(match.group(4))
        return ValheimSession(session_name, join_code, address, player_count)
    return None

def sever_started_version_message(entry_message: str):
    # This pattern matches:
    pattern = r"Valheim version:.*(\d+\.\d+\.\d+)"
    match = re.search(pattern, entry_message)
    if match:
        valheim_version = match.group(1)
        return ServerStarted(valheim_version)
    return None

def sever_stopped_message(entry_message: str):
    # This pattern matches:
    pattern = r"OnApplicationQuit"
    match = re.search(pattern, entry_message)
    if match:
        return ServerStopped()
    return None

# Parser for player join messages
def parse_player_joined_message(entry_message: str):
    # This pattern matches:
    pattern = r"<color=orange>(.*?)</color>: <color=#FFEB04FF>"
    match = re.search(pattern, entry_message)
    if match:
        player_name = match.group(1)
        return PlayerJoined(player_name)
    return None

def parse_player_died_message(entry_message: str):
    # This pattern matches:
    pattern = r"Got character ZDOID from (\w+) : 0:0"
    match = re.search(pattern, entry_message)
    if match:
        player_name = match.group(1)
        return PlayerDied(player_name)
    return None

_player_session_ids = {}

def parse_player_session_id_message(entry_message: str):
    # This pattern matches:
    pattern = r"Got character ZDOID from (\w+)\s*:\s*(\d+)"
    match = re.search(pattern, entry_message)
    if match:
        player_name = match.group(1)
        player_session_id = match.group(2)
        if player_name not in _player_session_ids or _player_session_ids[player_name] != player_session_id:
            _player_session_ids[player_name] = player_session_id
            logger.info(f"Added player to local cache: {player_name} with id {player_session_id}")
        logger.debug(f"Local cache: {', '.join(f'{name}: {id}' for name, id in _player_session_ids.items())}")
    return

def parse_player_left_message(entry_message: str):
    # This pattern matches:
    pattern = r"Destroying.*\bowner\s+(\d+)\b"
    match = re.search(pattern, entry_message)
    if match:
        player_session_id = match.group(1)
        player_name = next((name for name, session in _player_session_ids.items()
                            if session.startswith(player_session_id)), None)

        if player_name:
            del _player_session_ids[player_name]
            logger.info(f"Deleted player from local cache: {player_name} with id {player_session_id}")
            return PlayerLeft(player_name)
        else:
            logger.warning(f"Player {player_name} not found in local cache")
    return None


# List of parser functions for extensibility
_log_parsers = [
    sever_started_version_message,
    parse_session_message,
    parse_player_joined_message,
    parse_player_session_id_message,
    parse_player_died_message,
    parse_player_left_message,
    sever_stopped_message,
]


def parse_valheim_log(entry_message: str) -> LogEntry | None:
    """
    Iterates over registered parsers and returns the first matching log entry.
    Returns None if no parser matches the entry message.
    """
    for parser in _log_parsers:
        result = parser(entry_message)
        if result is not None:
            return result
    return None


async def handle_message(entry_message):
    if log_entry := parse_valheim_log(entry_message):
        logger.info(f"pushing event {log_entry}")
        await event_bus.publish(Topic.LOG_EVENT, log_entry)
