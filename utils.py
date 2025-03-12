from discord import Message
from messages import SingleMessage, ModAction

def format_message(message: Message) -> str:
    return f"{message.author.name} (user id: {message.author.id}, message id: {message.id}) in {message.channel.name} (channel id: {message.channel.id}) in server {message.guild.name} (server id: {message.guild.id}):\n{message.content}"

def format_single_message(message: SingleMessage) -> str:
    return f"{message.user_name} (user id: {message.user_id}, message id: {message.message_id}) in {message.channel_name} (channel id: {message.channel_id}) in server {message.server_name} (server id: {message.server_id}):\n{message.content}"

def format_discord_message(message: Message) -> str:
    """Format a Discord Message object directly"""
    if message.guild:
        return f"{message.author.name} (user id: {message.author.id}, message id: {message.id}) in {message.channel.name} (channel id: {message.channel.id}) in server {message.guild.name} (server id: {message.guild.id}):\n{message.content}"
    else:
        return f"{message.author.name} (user id: {message.author.id}, message id: {message.id}) in DM:\n{message.content}"

def format_mod_action(action: ModAction) -> str:
    return f"{action.action} (user id: {action.message.user_id}, message id: {action.message.message_id}) in {action.message.channel_name} (channel id: {action.message.channel_id}) in server {action.message.server_name} (server id: {action.message.server_id}):\n{action.message.content}"