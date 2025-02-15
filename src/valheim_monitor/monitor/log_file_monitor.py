import asyncio
import logging
import os

from valheim_monitor.monitor.valheim_log_parser import handle_message

logger = logging.getLogger(__name__)


async def log_file_monitor(file_path: str):
    """Monitors the log file for new events."""
    logger.info(f"Start monitoring log file: {file_path}")
    try:
        with open(file_path) as file:
            file.seek(0, 2)  # Move to the end of the file
            while True:
                line = file.readline()
                if line:
                    logger.debug(f"log line => {line}")
                    await handle_message(line.strip())
                else:
                    await asyncio.sleep(1)
    except FileNotFoundError:
        logger.error(f"Log file not found: {file_path}, current working directory {os.getcwd()}")
    except asyncio.CancelledError:
        logger.info("File Monitor task cancelled.")
        raise
    except Exception as e:
        logger.error(f"An error occurred while monitoring the log file: {str(e)}")
