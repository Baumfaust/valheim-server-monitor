import os
import logging
from typing import Final

import discord
import asyncio

from dotenv import load_dotenv

from event_bus import event_bus, Topic
from monitor.valheim_log_parser import ValheimSession, PlayerJoined

logger = logging.getLogger(__name__)

# Load environment variables from .env
load_dotenv()
TOKEN: Final[str] = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
client = discord.Client(intents=intents)

ready_discord = asyncio.Event()

async def send_discord_message(event_data):
    await client.wait_until_ready()
    if default_channel:
        match event_data:
            case ValheimSession(session_name, join_code, address, player_count):
                await default_channel.send(f"🏞️ Server **{session_name}** is online with {player_count} player(s)!")
            case PlayerJoined(player_name):
                await default_channel.send(f"🏹 **{player_name}** joined the game!")
            case _:
                logger.warning("⚠Unknown event type")
    else:
        logger.debug("No valid channel found!")

async def handle_discord_events():
    async def send_event_to_discord(event_data):
        logger.debug(f"received event {event_data}")
        await send_discord_message(event_data)

    event_bus.subscribe(Topic.LOG_EVENT, send_event_to_discord)
    logger.debug("Discord bot subscribed to events.")

@client.event
async def on_ready():
    logger.debug(f'Logged in as {client.user}')
    global default_channel
    default_channel = None

    # Get the first available text channel
    for guild in client.guilds:
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                default_channel = channel
                logger.debug(f"Using channel: {default_channel.name} ({default_channel.id})")
                break
        if default_channel:
            break
    await handle_discord_events()
    ready_discord.set()

async def run_bot():
    try:
        await client.start(TOKEN)
    except asyncio.CancelledError:
        logger.info("Bot task cancelled. Closing Discord client...")
        # Close the client gracefully if cancellation is received.
        await client.close()
        logger.info("Discord client closed.")
        raise