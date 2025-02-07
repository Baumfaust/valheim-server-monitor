import os
from typing import Final

import discord
import asyncio

from dotenv import load_dotenv

from event_bus import event_bus

# Load environment variables from .env
load_dotenv()
TOKEN: Final[str] = os.getenv("DISCORD_TOKEN")


intents = discord.Intents.default()
client = discord.Client(intents=intents)

async def send_discord_message(event_data):
    print(f"wait for discord to be ready")
    await client.wait_until_ready()
    print(f"Bot ready")
    if default_channel:
        await default_channel.send(event_data.session_name)
        print(f"✅ Message sent: {event_data.session_name}")
    else:
        print("⚠️ No valid channel found!")

    # channel = client.get_channel(1)
    # if channel:
    #     await channel.send(str(event_data.session_name))
    #     print(f"✅ Message sent to channel {CHANNEL_ID}: {message}")
    # else:
    #     print("⚠️ Invalid Discord Channel ID!")

async def handle_discord_events():
    async def send_event_to_discord(event_data):
        print(f"received event {event_data}")
        await send_discord_message(event_data)

    event_bus.subscribe("ServerOnlineEvent", send_event_to_discord)
    event_bus.subscribe("PlayerJoined", send_event_to_discord)
    event_bus.subscribe("ValheimLogEvent", send_event_to_discord)

    print("✅ Discord bot subscribed to events.")
    event_bus.signal_ready("discord_bot")


@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    global default_channel
    default_channel = None

    # Get the first available text channel
    for guild in client.guilds:
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                default_channel = channel
                print(f"✅ Using channel: {default_channel.name} ({default_channel.id})")
                break
        if default_channel:
            break
    await handle_discord_events()


async def run_bot():
    await client.start(TOKEN)
