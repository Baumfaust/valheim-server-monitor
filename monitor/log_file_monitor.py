import asyncio
import time
import re
from event_bus import event_bus
from monitor.valheim_log_parser import parse_valheim_log

LOG_FILE = "/path/to/logfile.log"

async def monitor_log():
    """Monitors the log file for new events."""
    with open(LOG_FILE, "r") as file:
        file.seek(0, 2)  # Move to the end of the file
        while True:
            line = file.readline()
            if line:
                await parse_valheim_log(line.strip())
                # await process_log_line(line.strip())
            else:
                await asyncio.sleep(1)  # Avoid busy-waiting

# async def process_log_line(line):
#     """Processes a log line and triggers events based on patterns."""
#     if "Server is now online" in line:
#         await event_bus.publish("ServerOnlineEvent", {"message": "Server is online"})
#     elif match := re.search(r"Player (\w+) joined the game", line):
#         await event_bus.publish("PlayerJoined", {"player": match.group(1)})
#
