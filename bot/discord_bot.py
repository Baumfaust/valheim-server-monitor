import asyncio
import logging
import os
from typing import Final

import discord
from dotenv import load_dotenv

from bot.join_messages import random_join_message
from event_bus import Topic, event_bus
from monitor.valheim_log_parser import PlayerDied, PlayerJoined, ServerStarted, ServerStopped, ValheimSession

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
                await default_channel.send(f"🏞️ Server **{session_name}** with join code **{join_code}** "
                                           f"and IP **{address}** is online "
                                           f"with {player_count} player(s)!")
            case ServerStarted(valheim_version):
                await default_channel.send(f"🏞️ Valheim server started with version **{valheim_version}**")
            case ServerStopped():
                await default_channel.send("❌ Valheim server stopped!")
            case PlayerJoined(player_name):
                await default_channel.send(random_join_message(player_name))
            case PlayerDied(player_name):
                await default_channel.send(f"💀 **{player_name}** died!")
            case _:
                logger.warning("Unknown event type")
    else:
        logger.debug("No valid channel found!")


async def handle_discord_events():
    async def send_event_to_discord(event_data):
        logger.info(f"received event {event_data}")
        await send_discord_message(event_data)

    topic = Topic.LOG_EVENT
    event_bus.subscribe(topic, send_event_to_discord)
    logger.debug(f"Discord bot subscribed to {topic}")


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
