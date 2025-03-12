import unittest
from unittest.mock import MagicMock, patch
from discord import Message, Guild, TextChannel, User
from messages import Messages, SingleMessage, ModAction, Server

class TestMessages(unittest.TestCase):
    def setUp(self):
        # Create a Messages instance for testing
        self.messages = Messages()
        
        # Create mock objects for testing
        self.mock_guild = MagicMock(spec=Guild)
        self.mock_guild.id = "789123456"
        self.mock_guild.name = "Test Server"
        
        self.mock_channel = MagicMock(spec=TextChannel)
        self.mock_channel.id = "456789123"
        self.mock_channel.name = "test-channel"
        
        self.mock_user = MagicMock(spec=User)
        self.mock_user.id = "123456789"
        self.mock_user.name = "TestUser"
        
        self.mock_message = MagicMock(spec=Message)
        self.mock_message.id = "987654321"
        self.mock_message.content = "This is a test message"
        self.mock_message.guild = self.mock_guild
        self.mock_message.channel = self.mock_channel
        self.mock_message.author = self.mock_user
    
    def test_ensure_server_exists_new_server(self):
        # Test ensuring a server exists when it doesn't already
        self.messages.ensure_server_exists(self.mock_message)
        
        # Check that the server was added to the servers dictionary
        self.assertIn(self.mock_guild.id, self.messages.servers)
        
        # Check that the server has the correct attributes
        server = self.messages.servers[self.mock_guild.id]
        self.assertEqual(server.id, self.mock_guild.id)
        self.assertEqual(server.name, self.mock_guild.name)
        self.assertEqual(server.rules, "Allow everything and don't do anything.")
        self.assertEqual(server.actions, {})
        self.assertEqual(server.recent_actions, [])
    
    def test_ensure_server_exists_existing_server(self):
        # Add a server to the servers dictionary
        self.messages.servers[self.mock_guild.id] = Server(
            id=self.mock_guild.id,
            name=self.mock_guild.name,
            rules="Custom rules",
            actions={},
            recent_actions=[]
        )
        
        # Test ensuring a server exists when it already does
        self.messages.ensure_server_exists(self.mock_message)
        
        # Check that the server still exists and wasn't modified
        self.assertIn(self.mock_guild.id, self.messages.servers)
        server = self.messages.servers[self.mock_guild.id]
        self.assertEqual(server.rules, "Custom rules")
    
    def test_add_message_guild(self):
        # Test adding a message from a guild
        self.messages.add_message(self.mock_message)
        
        # Check that the server was added
        self.assertIn(self.mock_guild.id, self.messages.servers)
    
    def test_add_message_dm(self):
        # Create a DM message
        dm_message = MagicMock(spec=Message)
        dm_message.id = "987654321"
        dm_message.content = "This is a test DM"
        dm_message.guild = None
        dm_message.author = self.mock_user
        
        # Test adding a DM message
        self.messages.add_message(dm_message)
        
        # Check that the DM was added to the dm_history
        self.assertIn(self.mock_user.id, self.messages.dm_history)
        self.assertIn(dm_message.id, self.messages.dm_history[self.mock_user.id])
    
    def test_create_single_message_guild(self):
        # Test creating a SingleMessage from a guild message
        single_message = self.messages.create_single_message(self.mock_message)
        
        # Check that the SingleMessage has the correct attributes
        self.assertEqual(single_message.content, self.mock_message.content)
        self.assertEqual(single_message.server_id, self.mock_guild.id)
        self.assertEqual(single_message.server_name, self.mock_guild.name)
        self.assertEqual(single_message.user_id, self.mock_user.id)
        self.assertEqual(single_message.user_name, self.mock_user.name)
        self.assertEqual(single_message.channel_id, self.mock_channel.id)
        self.assertEqual(single_message.channel_name, self.mock_channel.name)
        self.assertEqual(single_message.message_id, self.mock_message.id)
    
    def test_create_single_message_dm(self):
        # Create a DM message
        dm_message = MagicMock(spec=Message)
        dm_message.id = "987654321"
        dm_message.content = "This is a test DM"
        dm_message.guild = None
        dm_message.author = self.mock_user
        
        # Test creating a SingleMessage from a DM message
        single_message = self.messages.create_single_message(dm_message)
        
        # Check that the SingleMessage has the correct attributes
        self.assertEqual(single_message.content, dm_message.content)
        self.assertIsNone(single_message.server_id)
        self.assertEqual(single_message.server_name, "Private User DMs")
        self.assertEqual(single_message.user_id, self.mock_user.id)
        self.assertEqual(single_message.user_name, self.mock_user.name)
        self.assertIsNone(single_message.channel_id)
        self.assertEqual(single_message.channel_name, None)
        self.assertEqual(single_message.message_id, dm_message.id)
    
    def test_get_user_mod_actions(self):
        # Add a server to the servers dictionary
        server_id = self.mock_guild.id
        self.messages.servers[server_id] = Server(
            id=server_id,
            name=self.mock_guild.name,
            rules="Custom rules",
            actions={},
            recent_actions=[]
        )
        
        # Create a SingleMessage for the mod action
        single_message = SingleMessage(
            content="This is a test message",
            server_id=server_id,
            server_name=self.mock_guild.name,
            user_id=self.mock_user.id,
            user_name=self.mock_user.name,
            channel_id=self.mock_channel.id,
            channel_name=self.mock_channel.name,
            message_id=self.mock_message.id
        )
        
        # Create a ModAction
        mod_action = ModAction(
            action="delete",
            message=single_message
        )
        
        # Add the mod action to the server
        self.messages.servers[server_id].actions[self.mock_user.id] = [mod_action]
        
        # Test getting user mod actions
        actions = self.messages.get_user_mod_actions(self.mock_user.id, [server_id])
        
        # Check that the correct actions were returned
        self.assertEqual(len(actions), 1)
        self.assertEqual(actions[0].action, "delete")
        self.assertEqual(actions[0].message.content, "This is a test message")
    
    def test_add_mod_action(self):
        # Add a server to the servers dictionary
        server_id = self.mock_guild.id
        self.messages.servers[server_id] = Server(
            id=server_id,
            name=self.mock_guild.name,
            rules="Custom rules",
            actions={},
            recent_actions=[]
        )
        
        # Create message data for the mod action
        message_data = {
            "content": "This is a test message",
            "server_id": server_id,
            "server_name": self.mock_guild.name,
            "user_id": self.mock_user.id,
            "user_name": self.mock_user.name,
            "channel_id": self.mock_channel.id,
            "channel_name": self.mock_channel.name,
            "message_id": self.mock_message.id
        }
        
        # Test adding a mod action
        self.messages.add_mod_action("delete", message_data, self.mock_user.id)
        
        # Check that the mod action was added to the server's actions
        self.assertIn(self.mock_user.id, self.messages.servers[server_id].actions)
        actions = self.messages.servers[server_id].actions[self.mock_user.id]
        self.assertEqual(len(actions), 1)
        self.assertEqual(actions[0].action, "delete")
        
        # Check that the mod action was added to the server's recent_actions
        recent_actions = self.messages.servers[server_id].recent_actions
        self.assertEqual(len(recent_actions), 1)
        self.assertEqual(recent_actions[0].action, "delete")

if __name__ == "__main__":
    unittest.main() 