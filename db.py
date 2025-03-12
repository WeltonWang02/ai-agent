import json
import os
import logging
from dataclasses import asdict
from typing import Dict, List, Optional
from messages import Messages, Server, ModAction, SingleMessage

logger = logging.getLogger(__name__)

# Directory for storing database files
DB_DIR = "db"
SERVERS_FILE = os.path.join(DB_DIR, "servers.json")
DM_HISTORY_FILE = os.path.join(DB_DIR, "dm_history.json")

class FileDB:
    """Simple file-based database for storing Messages and Moderation data."""
    
    @staticmethod
    def ensure_db_dir():
        """Ensure the database directory exists."""
        if not os.path.exists(DB_DIR):
            os.makedirs(DB_DIR)
            logger.info(f"Created database directory: {DB_DIR}")
    
    @staticmethod
    def save_messages(messages: Messages):
        """Save Messages data to JSON files."""
        FileDB.ensure_db_dir()
        
        # Convert servers to a serializable format
        servers_data = {}
        for server_id, server in messages.servers.items():
            # Convert ModAction objects to dictionaries
            recent_actions = []
            for action in server.recent_actions:
                recent_actions.append({
                    "action": action.action,
                    "message": asdict(action.message)
                })
            
            # Convert user actions to dictionaries
            actions = {}
            for user_id, user_actions in server.actions.items():
                actions[user_id] = []
                for action in user_actions:
                    actions[user_id].append({
                        "action": action.action,
                        "message": asdict(action.message)
                    })
            
            # Create server data dictionary
            servers_data[server_id] = {
                "id": server.id,
                "name": server.name,
                "rules": server.rules,
                "recent_actions": recent_actions,
                "actions": actions
            }
        
        # Save servers data
        with open(SERVERS_FILE, 'w') as f:
            json.dump(servers_data, f, indent=2)
            logger.info(f"Saved servers data to {SERVERS_FILE}")
        
        # Save DM history
        with open(DM_HISTORY_FILE, 'w') as f:
            json.dump(messages.dm_history, f, indent=2)
            logger.info(f"Saved DM history to {DM_HISTORY_FILE}")
    
    @staticmethod
    def load_messages() -> Messages:
        """Load Messages data from JSON files."""
        FileDB.ensure_db_dir()
        messages = Messages()
        
        # Load servers data if file exists
        if os.path.exists(SERVERS_FILE):
            try:
                with open(SERVERS_FILE, 'r') as f:
                    servers_data = json.load(f)
                
                for server_id, server_data in servers_data.items():
                    # Create Server object
                    server = Server(
                        id=server_data["id"],
                        name=server_data["name"],
                        rules=server_data["rules"],
                        recent_actions=[],
                        actions={}
                    )
                    
                    # Load recent actions
                    for action_data in server_data["recent_actions"]:
                        message = SingleMessage(**action_data["message"])
                        action = ModAction(action=action_data["action"], message=message)
                        server.recent_actions.append(action)
                    
                    # Load user actions
                    for user_id, user_actions_data in server_data["actions"].items():
                        server.actions[user_id] = []
                        for action_data in user_actions_data:
                            message = SingleMessage(**action_data["message"])
                            action = ModAction(action=action_data["action"], message=message)
                            server.actions[user_id].append(action)
                    
                    messages.servers[server_id] = server
                
                logger.info(f"Loaded servers data from {SERVERS_FILE}")
            except Exception as e:
                logger.error(f"Error loading servers data: {e}")
        
        # Load DM history if file exists
        if os.path.exists(DM_HISTORY_FILE):
            try:
                with open(DM_HISTORY_FILE, 'r') as f:
                    messages.dm_history = json.load(f)
                logger.info(f"Loaded DM history from {DM_HISTORY_FILE}")
            except Exception as e:
                logger.error(f"Error loading DM history: {e}")
        
        return messages 