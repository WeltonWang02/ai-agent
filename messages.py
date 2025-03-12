from dataclasses import dataclass
from typing import Dict, List
from discord import Message

MAX_MESSAGE_CONTEXT = 10    
MAX_RECENT_MOD_ACTIONS = 20

@dataclass
class Channel:
    id: str
    messages: List[str]

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
    
@dataclass
class ModAction:
    action: str
    message: SingleMessage

@dataclass
class Server:
    id: str
    rules: str
    name: str
    channels: Dict[str, Channel]
    actions: Dict[str, list[ModAction]]

DEFAULT_RULES = """Allow everything and don't do anything."""

@dataclass
class User:
    id: str
    name: str
    messages: List[SingleMessage]

class Messages:
    def __init__(self):
        self.servers = {
            # Server ID -> Server
        }
        self.dms = {
            # User ID -> User
        }

    def add_message(self, message: Message):
        if message.guild:

            if message.guild.id not in self.servers:
                self.servers[message.guild.id] = Server(id=message.guild.id, name=message.guild.name, rules=DEFAULT_RULES, channels={}, actions={})

            if message.channel.id not in self.servers[message.guild.id].channels:
                self.servers[message.guild.id].channels[message.channel.id] = Channel(message.channel.id, [])


            single_message = SingleMessage(content=message.content, server_id=message.guild.id, server_name=message.guild.name, user_id=message.author.id, user_name=message.author.name, channel_id=message.channel.id, channel_name=message.channel.name, message_id=message.id)
            self.servers[message.guild.id].channels[message.channel.id].messages.append(single_message)

            # Keep only the last MAX_MESSAGE_CONTEXT messages
            self.servers[message.guild.id].channels[message.channel.id].messages = self.servers[message.guild.id].channels[message.channel.id].messages[-MAX_MESSAGE_CONTEXT:]

        else:
            if message.author.id not in self.dms:
                self.dms[message.author.id] = User(id=message.author.id, name=message.author.name, messages=[])

            single_message = SingleMessage(content=message.content, server_id=None, server_name="Private User DMs", user_id=message.author.id, user_name=message.author.name, channel_id=None, channel_name=None, message_id=message.id)
            self.dms[message.author.id].messages.append(single_message)

    def get_messages(self, server_id: str, channel_id: str):
        if server_id not in self.servers:
            return []

        if channel_id not in self.servers[server_id].channels:
            return []

        return self.servers[server_id].channels[channel_id].messages
    
    def get_user_message(self, user_id: str):
        if user_id not in self.dms:
            return []

        return self.dms[user_id].messages
    
    def get_user_mod_actions(self, user_id: str, server_ids: list[str]):
        actions = []
        for server_id in server_ids:
            if server_id not in self.servers:
                continue

            if user_id not in self.servers[server_id].actions:
                continue

            actions.extend(self.servers[server_id].actions[user_id])

        return actions[:MAX_RECENT_MOD_ACTIONS]
    
    def add_mod_action(self, actions: str, message: SingleMessage, user_id: str):
        if user_id not in self.servers[message.server_id].actions:
            self.servers[message.server_id].actions[user_id] = []

        self.servers[message.server_id].actions[user_id].append(ModAction(actions, message))