from dataclasses import dataclass
from typing import Dict, List
from discord import Message

MAX_MESSAGE_CONTEXT = 10    

@dataclass
class Channel:
    id: str
    messages: List[str]

@dataclass
class Server:
    id: str
    rules: str
    name: str
    channels: Dict[str, Channel]

@dataclass
class SingleMessage:
    content: str
    server_id: str
    server_name: str
    user_id: str
    user_name: str
    channel_id: str
    channel_name: str
    message_id: str

DEFAULT_RULES = """Allow everything and don't do anything."""

class Messages:
    def __init__(self):
        self.servers = {
            # Server ID -> Server
        }

    def add_message(self, message: Message):
        if message.guild.id not in self.servers:
            self.servers[message.guild.id] = Server(id=message.guild.id, name=message.guild.name, rules=DEFAULT_RULES, channels={})

        if message.channel.id not in self.servers[message.guild.id].channels:
            self.servers[message.guild.id].channels[message.channel.id] = Channel(message.channel.id, [])


        single_message = SingleMessage(content=message.content, server_id=message.guild.id, server_name=message.guild.name, user_id=message.author.id, user_name=message.author.name, channel_id=message.channel.id, channel_name=message.channel.name, message_id=message.id)
        self.servers[message.guild.id].channels[message.channel.id].messages.append(single_message)

        # Keep only the last MAX_MESSAGE_CONTEXT messages
        self.servers[message.guild.id].channels[message.channel.id].messages = self.servers[message.guild.id].channels[message.channel.id].messages[-MAX_MESSAGE_CONTEXT:]

    def get_messages(self, server_id: str, channel_id: str):
        if server_id not in self.servers:
            return []

        if channel_id not in self.servers[server_id].channels:
            return []

        return self.servers[server_id].channels[channel_id].messages