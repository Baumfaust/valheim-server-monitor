#!/usr/bin/env python3

import select
from systemd import journal
import time

def main():
    j = journal.Reader()
    j.log_level(journal.LOG_INFO)  # Optional: Set log level filter

    # Add match for specific unit (service)
    #j.add_match(_SYSTEMD_UNIT="valheim_server.service") # replace with your service name
    j.add_match(_SYSTEMD_USER_UNIT="valheim_server.service")

    j.seek_tail()  # Start from the end
    j.get_previous() # Important: Move to the last entry to prevent getting the same entry again

    p = select.poll()
    p.register(j, j.get_events())

    while True:
        if p.poll():
            if j.process() == journal.APPEND: # Check if new entries are available
                for entry in j:
#                    timestamp_readable = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(int(entry['__REALTIME_TIMESTAMP']) / 1000000)))
                    print(f"{entry['MESSAGE']}")
                   # print(f"[{timestamp_readable}] {entry['MESSAGE']}")
        time.sleep(0.1)  # Avoid high CPU usage when no events

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting.")