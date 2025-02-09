#!/usr/bin/env python3
import logging

import asyncio
import select
import time

from systemd import journal # pip3 install systemd-python


import select
import time

from monitor.valheim_log_parser import parse_valheim_log


async def journal_monitor(unit_name):
    try:
        j = journal.Reader()
        j.log_level(journal.LOG_INFO)  # Optional: Set log level filter

        # Add match for specific unit (service)
        #j.add_match(_SYSTEMD_UNIT="valheim_server.service") # replace with your service name
        j.add_match(_SYSTEMD_USER_UNIT=unit_name)

        j.seek_tail()  # Start from the end
        j.get_previous() # Important: Move to the last entry to prevent getting the same entry again

        p = select.poll()
        p.register(j, j.get_events())
        line_number = 1
        while True:
            await asyncio.to_thread(p.poll)
            if j.process() == journal.APPEND: # Check if new entries are available
                for entry in j:
                    line = entry['MESSAGE']
                    print(f"{line_number} => {line}")
                    parse_valheim_log(f"{line}")
                    line_number += 1
            await asyncio.sleep(0.1)

    except KeyboardInterrupt:
        print("\n👋 Exiting log monitor...")
    except Exception as e:
        print(f"❌ Error reading systemd logs: {e}")
