#!/usr/bin/env python3

import re
from dataclasses import dataclass
from typing import Optional, Callable, Any


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


def handle_message(
    callback: Optional[Callable[[LogEntry], None]], entry: dict[str, Any]
):
    """Handles a journal entry and calls the callback if appropriate."""
    if "MESSAGE" not in entry:
        return  # Handle cases where MESSAGE is missing

    message = entry["MESSAGE"]
    if log_entry := parse_valheim_log(message):
        if callback:
            callback(log_entry)


def parse_valheim_log(entry_message):
    """Parses Valheim server log messages for session information."""
    pattern = (r"Session \"(.*?)\" with join code (\d+) and IP (.*?:\d+) "
               r"is active with (\d+) player\(s\)")
    match = re.search(pattern, entry_message)
    if match:
        session_name = match.group(1)
        join_code = int(match.group(2))
        address = match.group(3)
        player_count = int(match.group(4))
        return ValheimSession(session_name, join_code, address, player_count)
    return None
