import logging
import re
from dataclasses import dataclass

from event_bus import Topic, event_bus

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
class PlayerJoined(LogEntry):
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


# Parser for player join messages
def parse_player_join_message(entry_message: str):
    # This pattern matches:
    # "Console: <color=orange>Erwin</color>: <color=#FFEB04FF>I HAVE ARRIVED!</color>"
    pattern = r"Console: <color=orange>(.*?)</color>: <color=#FFEB04FF>I HAVE ARRIVED!</color>"
    match = re.search(pattern, entry_message)
    if match:
        player_name = match.group(1)
        return PlayerJoined(player_name)
    return None


# List of parser functions for extensibility
_log_parsers = [
    parse_session_message,
    parse_player_join_message,
    # Additional parsers can be added here
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
        logger.debug(f"pushing event {log_entry}")
        await event_bus.publish(Topic.LOG_EVENT, log_entry)
