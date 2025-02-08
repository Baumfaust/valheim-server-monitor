#!/usr/bin/env python3

import re
from dataclasses import dataclass

from event_bus import event_bus, Topic


# Define a base class for log entries
@dataclass(frozen=True)
class LogEntry:
    pass


# Dataclass for Valheim session start messages
@dataclass(frozen=True)
class ValheimSession(LogEntry):
    """Holds information parsed from a Valheim server log message."""

    session_name: str
    join_code: int
    address: str
    player_count: int


# Dataclass for other potential messages (example)
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

# async def handle_message(entry: dict[str, Any]):
async def handle_message(entry_message):

    if log_entry := parse_valheim_log(entry_message):
            print(f"pushing event {log_entry}")
            await event_bus.publish(Topic.LOG_EVENT, log_entry)


# def parse_valheim_log(entry_message):
#     """Parses Valheim server log messages for session information."""
#     pattern = (
#         r"Session \"(.*?)\" with join code (\d+) and IP (.*?:\d+) "
#         r"is active with (\d+) player\(s\)"
#     )
#     match = re.search(pattern, entry_message)
#     if match:
#         session_name = match.group(1)
#         join_code = int(match.group(2))
#         address = match.group(3)
#         player_count = int(match.group(4))
#         return ValheimSession(session_name, join_code, address, player_count)
#     return None

# def handle_message(callback: Optional[Callable[[LogEntry], None]], entry: dict[str, Any]):
#     """Handles a journal entry and calls the callback if appropriate."""
#     if "MESSAGE" not in entry:
#         return  # Handle cases where MESSAGE is missing
#
#     message = entry["MESSAGE"]
#     if (log_entry := parse_valheim_log(message)) and callback:
#         callback(log_entry)
#
# async def parse_valheim_log(line):
#     """Processes a log line and triggers events based on patterns."""
#     if "Server is now online" in line:
#         await event_bus.publish("ServerOnlineEvent", {"message": "Server is online"})
#     elif match := re.search(r"Player (\w+) joined the game", line):
#         await event_bus.publish("PlayerJoined", {"player": match.group(1)})
#
# def parse_valheim_log(entry_message):
#     """Parses Valheim server log messages for session information."""
#     pattern = (
#         r"Session \"(.*?)\" with join code (\d+) and IP (.*?:\d+) "
#         r"is active with (\d+) player\(s\)"
#     )
#     match = re.search(pattern, entry_message)
#     if match:
#         session_name = match.group(1)
#         join_code = int(match.group(2))
#         address = match.group(3)
#         player_count = int(match.group(4))
#         return ValheimSession(session_name, join_code, address, player_count)
#     return None
