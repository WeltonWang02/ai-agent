from dataclasses import dataclass, field
from typing import Dict, List, Optional
from discord import Message

MAX_MESSAGE_CONTEXT = 10    
MAX_RECENT_MOD_ACTIONS = 20

@dataclass
class SingleMessage:
    content: str
    server_id: Optional[str]
    server_name: str
    user_id: str
    user_name: str
    channel_id: Optional[str]
    channel_name: Optional[str]
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
    recent_actions: list[ModAction]
    actions: Dict[str, list[ModAction]] = field(default_factory=dict)
    channels: Dict[str, dict[str, str]] = field(default_factory=dict)

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
        self.dm_history = {}  # User ID -> list of message IDs
    
    # We still need to track servers for rules and moderation actions
    def ensure_server_exists(self, message: Message):
        if message.guild and message.guild.id not in self.servers:
            self.servers[str(message.guild.id)] = Server(
                id=message.guild.id, 
                name=message.guild.name, 
                rules=DEFAULT_RULES, 
                actions={},
                recent_actions=[]
            )
    
    def add_message(self, message: Message):
        # We only need to ensure servers exist and track DM message IDs
        if message.guild:
            self.ensure_server_exists(message)
        else:
            # For DMs, just track the message ID
            if message.author.id not in self.dm_history:
                self.dm_history[message.author.id] = []
            
            self.dm_history[message.author.id].append(message.id)
            # Keep only the most recent MAX_MESSAGE_CONTEXT messages
            self.dm_history[message.author.id] = self.dm_history[message.author.id][-MAX_MESSAGE_CONTEXT:]
    
    def create_single_message(self, message: Message) -> SingleMessage:
        """Create a SingleMessage object from a Discord Message"""
        if message.guild:
            return SingleMessage(
                content=message.content,
                server_id=message.guild.id,
                server_name=message.guild.name,
                user_id=message.author.id,
                user_name=message.author.name,
                channel_id=message.channel.id,
                channel_name=message.channel.name,
                message_id=message.id
            )
        else:
            return SingleMessage(
                content=message.content,
                server_id=None,
                server_name="Private User DMs",
                user_id=message.author.id,
                user_name=message.author.name,
                channel_id=None,
                channel_name=None,
                message_id=message.id
            )
    
    def get_user_mod_actions(self, user_id: str, server_ids: list[str]):
        actions = []
        for server_id in server_ids:
            if str(server_id) not in self.servers:
                continue

            if user_id not in self.servers[str(server_id)].actions:
                continue

            actions.extend(self.servers[str(server_id)].actions[user_id])

        return actions[:MAX_RECENT_MOD_ACTIONS]
    
    def add_mod_action(self, action: str, message_data: dict, user_id: str):
        server_id = message_data.get("server_id")
        if not server_id:
            return
            
        if str(server_id) not in self.servers:
            return
            
        if user_id not in self.servers[str(server_id)].actions:
            self.servers[str(server_id)].actions[user_id] = []
            
        # Create a SingleMessage object from the message data
        message = SingleMessage(
            content=message_data.get("content", ""),
            server_id=server_id,
            server_name=message_data.get("server_name", "Unknown Server"),
            user_id=user_id,
            user_name=message_data.get("user_name", "Unknown User"),
            channel_id=message_data.get("channel_id"),
            channel_name=message_data.get("channel_name"),
            message_id=message_data.get("message_id", "")
        )
        
        self.servers[str(server_id)].actions[user_id].append(ModAction(action, message))
        self.servers[str(server_id)].recent_actions.append(ModAction(action, message))
        # Keep only the most recent MAX_RECENT_MOD_ACTIONS
        self.servers[str(server_id)].recent_actions = self.servers[str(server_id)].recent_actions[-MAX_RECENT_MOD_ACTIONS:]
        
        # Save changes to disk
        self.save()
    
    def save(self):
        """Save the current state to disk"""
        # Import here to avoid circular imports
        from db import FileDB
        FileDB.save_messages(self)
    
    @classmethod
    def load(cls):
        """Load the state from disk"""
        # Import here to avoid circular imports
        from db import FileDB
        return FileDB.load_messages()

    def update_last_read(self, user_id: str, channel_id: str, message_id: str):
        for server in self.servers.values():
            if channel_id in server.channels:
                server.channels[channel_id][user_id] = message_id
            else:
                server.channels[channel_id] = {user_id: message_id}
