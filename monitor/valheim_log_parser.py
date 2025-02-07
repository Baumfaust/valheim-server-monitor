#!/usr/bin/env python3

import re
from dataclasses import dataclass
from typing import Any, Callable, Optional

from event_bus import event_bus


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


# async def handle_message(entry: dict[str, Any]):
async def handle_message(entry_message):

    if log_entry := parse_valheim_log(entry_message):
            print(f"pushing event {log_entry}")
            await event_bus.publish("ValheimLogEvent", log_entry)


def parse_valheim_log(entry_message):
    """Parses Valheim server log messages for session information."""
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
