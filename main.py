import asyncio
import atexit
import logging
import os
import signal
import sys
import threading

from bot.discord_bot import run_bot, ready_discord
from event_bus import event_bus
from monitor.valheim_log_parser import handle_message

log_level = os.getenv("LOG_LEVEL", "INFO").upper()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
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

# def on_exit():
#     """Called when Python exits (works for PyCharm stop button)."""
#     handle_shutdown_signal()
#
# # Register exit handler for PyCharm stop button
# atexit.register(on_exit)

async def main():
    register_signal_handlers()

    bot_task = asyncio.create_task(run_bot())

    # Wait for all subscribers to be ready
    logger.debug("Waiting for all subscribers to be ready...")
    await asyncio.gather(ready_discord.wait())
    logger.debug("All subscribers are ready!")

    # Send test message after subscribers are ready
    start_mes = "Session \"Donnersberg\" with join code 582905 and IP 130.61.112.24:2456 is active with 0 player(s)"
    player_join = "Console: <color=orange>Erwin</color>: <color=#FFEB04FF>I HAVE ARRIVED!</color>"

    logger.debug("Sending test message...")
    await handle_message(start_mes)
    await handle_message(player_join)
    logger.debug("Test message sent.")

    # Wait until shutdown event is triggered
    await shutdown_event.wait()
    logger.info("Cancelling tasks...")

    bot_task.cancel()

    # Wait for tasks to cancel gracefully
    await asyncio.gather(bot_task, return_exceptions=True)
    logger.info("Shutdown complete.")


if __name__ == "__main__":
    asyncio.run(main())
