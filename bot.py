import os
import discord
import logging

from discord.ext import commands
from dotenv import load_dotenv
from agent import MistralAgent
from moderation import Moderation
from summarizer import Summarizer

PREFIX = "!"

# Define a constant for the number of messages to summarize
SUMMARY_MESSAGE_LIMIT = 10

# Setup logging
logger = logging.getLogger("discord")

# Load the environment variables
load_dotenv()

# Create the bot with all intents
# The message content and members intent must be enabled in the Discord Developer Portal for the bot to work.
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=PREFIX, intents=intents)

# Import the Mistral agent from the agent.py file
agent = MistralAgent()

# Get the token from the environment variables
token = os.getenv("DISCORD_TOKEN")

moderation = Moderation(bot)

# Initialize the summarizer
summarizer = Summarizer()

@bot.event
async def on_ready():
    """
    Called when the client is done preparing the data received from Discord.
    Prints message on terminal when bot successfully connects to discord.

    https://discordpy.readthedocs.io/en/latest/api.html#discord.on_ready
    """
    logger.info(f"{bot.user} has connected to Discord!")


@bot.event
async def on_message(message: discord.Message):
    """
    Called when a message is sent in any channel the bot can see.

    https://discordpy.readthedocs.io/en/latest/api.html#discord.on_message
    """
    # Don't delete this line! It's necessary for the bot to process commands.
    await bot.process_commands(message)

    if message.guild:
        # sent to a server
        await moderation.moderate(message)

    # Ignore messages from self or other bots to prevent infinite loops.
    if message.author.bot or message.content.startswith("!"):
        return

# Commands


# This example command is here to show you how to add commands to the bot.
# Run !ping with any number of arguments to see the command in action.
# Feel free to delete this if your project will not need commands.
@bot.command(name="ping", help="Pings the bot.")
async def ping(ctx, *, arg=None):
    if arg is None:
        await ctx.send("Pong!")
    else:
        await ctx.send(f"Pong! Your argument was {arg}")

@bot.command(name="summarize", help="Summarizes the last N messages in the current channel.")
async def summarize(ctx):
    # Fetch the last N messages from the channel, where N is defined by SUMMARY_MESSAGE_LIMIT
    messages = [message async for message in ctx.channel.history(limit=SUMMARY_MESSAGE_LIMIT)]

    # Generate a summary
    summary = await summarizer.summarize_messages(messages)

    # Send the summary back to the channel
    await ctx.send(f"Summary of the last {SUMMARY_MESSAGE_LIMIT} messages:\n{summary}")

@bot.command(name="summarize_unread", help="Summarizes unread messages in the current channel.")
async def summarize_unread(ctx):
    # Get unread messages for the user in the current channel
    unread_messages = moderation.messages.get_unread_messages(ctx.author.id, ctx.channel.id)

    if not unread_messages:
        await ctx.send("No unread messages to summarize.")
        return

    # Generate a summary
    summary = await summarizer.summarize_messages(unread_messages)

    # Send the summary back to the channel
    await ctx.send(f"Summary of unread messages:\n{summary}")

    # Update the last read message for the user
    if unread_messages:
        last_message_id = unread_messages[-1].message_id
        moderation.messages.update_last_read(ctx.author.id, ctx.channel.id, last_message_id)

# Start the bot, connecting it to the gateway
bot.run(token)
