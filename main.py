import asyncio
import atexit
import logging
import os
import signal
import sys
import threading

from bot.discord_bot import run_bot, ready_discord
from event_bus import event_bus
from monitor.log_file_monitor import log_file_monitor
from monitor.valheim_log_parser import handle_message

log_level = os.getenv("LOG_LEVEL", "INFO").upper()

# Configure logging
logging.basicConfig(
    level=log_level,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)
logging.getLogger("discord").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# Set Windows event loop policy to Selector (for compatibility)
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    logger.info("Windows event loop policy set.")

shutdown_event = asyncio.Event()


def handle_shutdown_signal():
    """Handles shutdown signals by setting the event to stop asyncio tasks."""
    logger.info("Shutdown signal received, shutting down gracefully...")
    shutdown_event.set()


def register_signal_handlers():
    """Registers signal handlers, using a thread-based approach on Windows."""
    if sys.platform == "win32":
        signal.signal(signal.SIGINT, lambda sig, frame: handle_shutdown_signal())
        signal.signal(signal.SIGTERM, lambda sig, frame: handle_shutdown_signal())
    else:
        loop = asyncio.get_running_loop()
        for sig in (signal.SIGTERM, signal.SIGINT):
            loop.add_signal_handler(sig, handle_shutdown_signal)


def select_log_monitoring():
    monitor_type = os.getenv('MONITOR_TYPE')
    unit_name = os.getenv('UNIT_NAME')  # systemd service name
    log_file = os.getenv('LOG_FILE_PATH')  # log file path

    # Match on the monitor type
    match monitor_type:
        case 'journal' if unit_name:
            from monitor.journal_monitor import journal_monitor
            return journal_monitor, unit_name
        case 'file' if log_file:
            return log_file_monitor, log_file
        case _:
            logger.error("Invalid configuration. Please set MONITOR_TYPE and UNIT_NAME, or LOG_FILE_PATH.")
            exit(1)


async def main():
    monitor, monitor_target = select_log_monitoring()
    monitor = log_file_monitor
    monitor_target = "test.log"
    register_signal_handlers()


    bot_task = asyncio.create_task(run_bot())

    # Wait for all subscribers to be ready
    logger.debug("Waiting for all subscribers to be ready...")
    await asyncio.gather(ready_discord.wait())
    logger.debug("All subscribers are ready!")

    monitor_task = asyncio.create_task(monitor(monitor_target))


    # Send test message after subscribers are ready
    # start_mes = "Session \"Donnersberg\" with join code 582905 and IP 130.61.112.24:2456 is active with 0 player(s)"
    # player_join = "Console: <color=orange>Erwin</color>: <color=#FFEB04FF>I HAVE ARRIVED!</color>"
    #
    # logger.debug("Sending test message...")
    # await handle_message(start_mes)
    # await handle_message(player_join)
    # logger.debug("Test message sent.")

    # Wait until shutdown event is triggered
    await shutdown_event.wait()
    logger.info("Cancelling tasks...")

    monitor_task.cancel()
    bot_task.cancel()

    # Wait for tasks to cancel gracefully
    await asyncio.gather(bot_task, monitor_task, return_exceptions=True)
    logger.info("Shutdown complete.")


if __name__ == "__main__":
    asyncio.run(main())
