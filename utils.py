from discord import Message
from messages import SingleMessage

def format_message(message: Message) -> str:
    return f"{message.author.name} (user id: {message.author.id}, message id: {message.id}) in {message.channel.name} (channel id: {message.channel.id}) in server {message.guild.name} (server id: {message.guild.id}):\n{message.content}"

def format_single_message(message: SingleMessage) -> str:
    return f"{message.user_name} (user id: {message.user_id}, message id: {message.message_id}) in {message.channel_name} (channel id: {message.channel_id}) in server {message.server_name} (server id: {message.server_id}):\n{message.content}"