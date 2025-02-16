import asyncio
import logging
import os
from typing import Final

import discord
from dotenv import load_dotenv

from bot.join_messages import random_join_message
from event_bus import Topic, event_bus
from monitor.valheim_log_parser import (
    PlayerDied,
    PlayerJoined,
    PlayerLeft,
    ServerStarted,
    ServerStopped,
    ValheimSession,
)

# Configure Logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

# Load environment variables
load_dotenv()
TOKEN: Final[str] = os.getenv("DISCORD_TOKEN")

# Discord Bot Setup
intents = discord.Intents.default()
intents.guilds = True

client = discord.Client(intents=intents)

# Event to signal when bot is ready
ready_discord = asyncio.Event()
server_channels = {}  # Dictionary to store channels per server


async def send_discord_message(event_data):
    """Sends event messages to the #valheim channel of each server."""
    await client.wait_until_ready()

    for guild_id, channel in server_channels.items():
        if channel:
            match event_data:
                case ValheimSession(session_name, join_code, address, player_count):
                    await channel.send(f"🏞️ Server **{session_name}** is online! Join code: **{join_code}** "
                                       f"| IP: **{address}** | Players: **{player_count}**")
                case ServerStarted(valheim_version):
                    await channel.send(f"🏞️ Valheim server started, running version **{valheim_version}**")
                case ServerStopped():
                    await channel.send("❌ Valheim server stopped")
                case PlayerJoined(player_name):
                    await channel.send(random_join_message(player_name))
                case PlayerDied(player_name):
                    await channel.send(f"💀 **{player_name}** died")
                case PlayerLeft(player_name):
                    await channel.send(f"👋 **{player_name}** left the server")
                case _:
                    logger.warning("Unknown event type")
        else:
            logger.debug(f"No valid #valheim channel found for guild {guild_id}")


async def handle_discord_events():
    """Subscribes to log events and forwards them to Discord."""
    async def send_event_to_discord(event_data):
        logger.debug(f"Received event: {event_data}")
        await send_discord_message(event_data)

    topic = Topic.LOG_EVENT
    event_bus.subscribe(topic, send_event_to_discord)
    logger.debug(f"Discord bot subscribed to {topic}")


@client.event
async def on_ready():
    """Triggered when the bot connects to Discord."""
    logger.debug(f'Logged in as {client.user}')
    global server_channels
    server_channels = {}  # Reset channels in case of reconnect
    logger.debug(f'Client has {len(client.guilds)} guilds')
    for guild in client.guilds:
        valheim_channel = discord.utils.get(guild.text_channels, name="valheim")

        if valheim_channel:
            logger.debug(f"Found #valheim in {guild.name} ({guild.id})")
            if valheim_channel.permissions_for(guild.me).send_messages:
                logger.debug(f"Bot has permission to send messages in {valheim_channel}")
                server_channels[guild.id] = valheim_channel
                logger.debug(f"Added {valheim_channel} to server_channels")
        else:
            server_channels[guild.id] = None
            logger.warning(f"No #valheim channel found in {guild.name} ({guild.id})")

    await handle_discord_events()
    ready_discord.set()


async def run_bot():
    """Starts the Discord bot and handles shutdown."""
    try:
        await client.start(TOKEN)
    except asyncio.CancelledError:
        logger.debug("Bot task cancelled. Closing Discord client...")
        await client.close()
        logger.debug("Discord client closed.")
        raise  # Propagate the error to handle shutdown properly
