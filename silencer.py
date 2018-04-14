# Start of a discord bot
import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import time
import os

SILENCER_BOT_TOKEN = os.environ['SILENCER_BOT_TOKEN']

Client = discord.Client()
client_ = commands.Bot(command_prefix = "!")

@client_.event
async def on_ready():
    print("Yeah, Bot baby!")

@client_.event
async def on_message(message):
    if message.content == "cookie":
        await client_.send_message(message.channel, ":cookie:")
client_.run(SILENCER_BOT_TOKEN)
