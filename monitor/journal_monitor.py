import logging

import asyncio
import select
import time

from systemd import journal

from monitor.valheim_log_parser import parse_valheim_log

logger = logging.getLogger(__name__)


def journal_monitor(unit_name: str):
    try:
        logger.info(f"Monitoring systemd journal for unit: {unit_name}")
        j = journal.Reader()
        j.log_level(journal.LOG_INFO)  # Optional: Set log level filter

        j.add_match(_SYSTEMD_USER_UNIT=unit_name)

        j.seek_tail()  # Start from the end
        j.get_previous()  # Important: Move to the last entry to prevent getting the same entry again

        p = select.poll()
        p.register(j, j.get_events())

        while True:
            if p.poll() and j.process() == journal.APPEND:  # Check if new entries are available
                for entry in j:
                    parse_valheim_log(f"{entry['MESSAGE']}")
            time.sleep(0.1)

    except asyncio.CancelledError:
        logger.info("File Monitor task cancelled.")
        raise
    except Exception as e:
        logger.error(f"An error occurred while monitoring unit {unit_name}: {str(e)}")


if __name__ == "__main__":
    try:
        journal_monitor()
    except KeyboardInterrupt:
        print("Exiting.")
