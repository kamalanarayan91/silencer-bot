# Start of a discord bot

from discord.ext import commands

import asyncio
import discord
import logging
import os

logging.basicConfig(level=logging.INFO)

SILENCER_BOT_TOKEN = os.environ['SILENCER_BOT_TOKEN']
GOD_ROLE_IDS = ["434852173436813313"]
MUTE_SECONDS = 60

client = commands.Bot(command_prefix = "!")

def can_mute(user):
    """
    Checks if the user is allowed to mute
    """
    muter_role_ids = [role.id for role in user.roles]
    logging.info(muter_role_ids)

    for id in muter_role_ids:
        if id in GOD_ROLE_IDS:
            return True
    logging.info("cannot mute! {}".format(user.id))
    return False

@client.event
async def on_ready():
    logging.info("Yeah, Bot baby!")

@client.event
async def on_message(message):
    lower_case_content  = message.content.lower()

    # Server Mutes a user specified for a certain time
    if lower_case_content.startswith('!shutup'):

        logging.info("Received mute command from {}".format(message.author))
        args = message.content.split(" ")
        muter = message.author

        if len(args) < 2:
            await client.send_message(message.channel, "shutup command needs a user name e.g !shutup @Demofreak")
            return

        mutee = args[1] # Yes, I will ignore the rest of your arguments
        mutee = mutee[2:-1] # Remove the '<@' and '>'
        logging.info(mutee)

        # Check if the muter has required permissions
        if can_mute(muter) == False:
            await client.send_message(message.channel, "No, you shut up <@{}> ".format(muter.id))
            return

        # Find the mutee
        mutee = message.server.get_member(mutee)
        logging.info("Muting {} initiated by {}".format(mutee.display_name, muter.name))

        await client.send_message(message.channel, "Casting last word on <@{}> ".format(mutee.id))

        await client.server_voice_state(mutee, mute=True)

        await asyncio.sleep(MUTE_SECONDS)

        logging.info("Unmuting {}".format(mutee.display_name))
        await client.server_voice_state(mutee, mute=False)

    elif lower_case_content.startswith('!ping'):
        logging.info("Received ping command from {}".format(message.author))
        command_user_id = message.author.id
        await client.send_message(message.channel, "<@{}> Pong!".format(command_user_id))


client.run(SILENCER_BOT_TOKEN)

