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


class Messages:
    def __init__(self):
        self.servers = {
            # Server ID -> Server
        }

    def add_message(self, message: Message):
        if message.guild.id not in self.servers:
            self.servers[message.guild.id] = Server(id=message.guild.id, name=message.guild.name, rules="", channels={})

        if message.channel.id not in self.servers[message.guild.id].channels:
            self.servers[message.guild.id].channels[message.channel.id] = Channel(message.channel.id, [])

        self.servers[message.guild.id].channels[message.channel.id].messages.append(message)

        # Keep only the last MAX_MESSAGE_CONTEXT messages
        self.servers[message.guild.id].channels[message.channel.id].messages = self.servers[message.guild.id].channels[message.channel.id].messages[-MAX_MESSAGE_CONTEXT:]

    def get_messages(self, server_id: str, channel_id: str):
        if server_id not in self.servers:
            return []

        if channel_id not in self.servers[server_id].channels:
            return []

        return self.servers[server_id].channels[channel_id].messages