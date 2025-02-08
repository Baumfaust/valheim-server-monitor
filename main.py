import asyncio
import logging
import os

from bot.discord_bot import run_bot, ready_discord
from event_bus import event_bus
from monitor.valheim_log_parser import handle_message

log_level = os.getenv("LOG_LEVEL", "INFO").upper()
# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Default level
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),  # Log to a file
        logging.StreamHandler()  # Log to console
    ]
)
logging.getLogger("discord").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


async def main():
    # Step 1: Start all event subscribers (but don't send events yet)
    bot_task = asyncio.create_task(run_bot())
    # grafana_task = asyncio.create_task(start_grafana())

    # Step 2: Wait until all subscribers are ready
    logger.debug("Waiting for all subscribers to be ready...")
    await asyncio.gather(ready_discord.wait())
    logger.debug("All subscribers are ready!")

    # Step 3: Send test event (only after all subscribers are ready)
    start_mes = "Session \"Donnersberg\" with join code 582905 and IP 130.61.112.24:2456 is active with 0 player(s)"
    player_join = "Console: <color=orange>Erwin</color>: <color=#FFEB04FF>I HAVE ARRIVED!</color>"
    logger.debug("Sending test message...")
    await handle_message(start_mes)
    await handle_message(player_join)
    logger.debug("Test message sent.")

    # Step 4: Keep the bot running
    await bot_task
    # await grafana_task


# Run everything
if __name__ == "__main__":
    asyncio.run(main())
