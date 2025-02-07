import asyncio
from time import sleep

from bot.discord_bot import run_bot
from grafana.grafana_sender import handle_grafana_events
from event_bus import event_bus
from monitor.valheim_log_parser import parse_valheim_log, handle_message


async def main():
    # Step 1: Start all event subscribers (but don't send events yet)
    event_bus.register_ready_event("discord_bot")
    bot_task = asyncio.create_task(run_bot())
    #grafana_task = asyncio.create_task(start_grafana())

    # Step 2: Wait until all subscribers are ready
    print("Waiting for all subscribers to be ready...")
    await event_bus.wait_for_all_ready()
    print("All subscribers are ready!")

    # Step 3: Send test event (only after all subscribers are ready)
    start_mes = "Session \"Donnersberg\" with join code 582905 and IP 130.61.112.24:2456 is active with 0 player(s)"
    print("Sending test message...")
    await handle_message(start_mes)
    print("Test message sent.")

    # Step 4: Keep the bot running
    await bot_task
    #await grafana_task

# Run everything
if __name__ == "__main__":
    asyncio.run(main())

