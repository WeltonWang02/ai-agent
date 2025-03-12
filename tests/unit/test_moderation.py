import unittest
from unittest.mock import MagicMock, patch, AsyncMock
import json
from discord import Message, Member, Guild, TextChannel, User
from discord.ext import commands
from moderation import Moderation, TOOLS
from messages import Messages, SingleMessage, ModAction
from agent import MistralAgent
from discord_wrapper import DiscordWrapper

class TestModeration(unittest.TestCase):
    def setUp(self):
        # Create mock objects
        self.mock_bot = MagicMock(spec=commands.Bot)
        
        # Create patches
        self.messages_patch = patch('moderation.Messages')
        self.agent_patch = patch('moderation.MistralAgent')
        self.discord_wrapper_patch = patch('moderation.DiscordWrapper')
        
        # Start patches
        self.mock_messages_class = self.messages_patch.start()
        self.mock_agent_class = self.agent_patch.start()
        self.mock_discord_wrapper_class = self.discord_wrapper_patch.start()
        
        # Create mock instances
        self.mock_messages = MagicMock(spec=Messages)
        self.mock_agent = MagicMock(spec=MistralAgent)
        self.mock_discord_wrapper = MagicMock(spec=DiscordWrapper)
        
        # Set return values for the mock classes
        self.mock_messages_class.return_value = self.mock_messages
        self.mock_agent_class.return_value = self.mock_agent
        self.mock_discord_wrapper_class.return_value = self.mock_discord_wrapper
        
        # Create a Moderation instance for testing
        self.moderation = Moderation(self.mock_bot)
        
        # Create mock Discord objects
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
        
        # Set up the mock agent's methods
        self.mock_agent.send_message = AsyncMock()
        self.mock_agent.process_tool_call = MagicMock()
        
        # Set up the mock discord_wrapper's methods
        self.mock_discord_wrapper.send_dm = AsyncMock()
        self.mock_discord_wrapper.send_message = AsyncMock()
        self.mock_discord_wrapper.delete_message = AsyncMock()
        self.mock_discord_wrapper.ban_user = AsyncMock()
        self.mock_discord_wrapper.kick_user = AsyncMock()
        self.mock_discord_wrapper.unban_user = AsyncMock()
    
    def tearDown(self):
        # Stop patches
        self.messages_patch.stop()
        self.agent_patch.stop()
        self.discord_wrapper_patch.stop()
    
    def test_init(self):
        # Test that the Moderation class initializes correctly
        self.assertEqual(self.moderation.bot, self.mock_bot)
        self.assertEqual(self.moderation.messages, self.mock_messages)
        self.assertEqual(self.moderation.agent, self.mock_agent)
    
    def test_is_author_admin(self):
        # Test checking if a user is an admin
        
        # Create a mock member with admin permissions
        admin_member = MagicMock(spec=Member)
        admin_member.guild_permissions.administrator = True
        
        # Create a mock message with an admin author
        admin_message = MagicMock(spec=Message)
        admin_message.author = admin_member
        
        # Test with an admin user
        self.assertTrue(self.moderation.is_author_admin(admin_message))
        
        # Create a mock member without admin permissions
        non_admin_member = MagicMock(spec=Member)
        non_admin_member.guild_permissions.administrator = False
        
        # Create a mock message with a non-admin author
        non_admin_message = MagicMock(spec=Message)
        non_admin_message.author = non_admin_member
        
        # Test with a non-admin user
        self.assertFalse(self.moderation.is_author_admin(non_admin_message))
    
    async def test_run_tool_send_dm(self):
        # Test running the send_dm tool
        tool_call = {
            "name": "send_dm",
            "parameters": {
                "user_id": "123456789",
                "message": "This is a test DM"
            }
        }
        
        await self.moderation.run_tool(tool_call)
        
        # Check that send_dm was called with the correct arguments
        self.mock_discord_wrapper.send_dm.assert_called_once_with(
            "123456789", "This is a test DM"
        )
    
    async def test_run_tool_send_message(self):
        # Test running the send_message tool
        tool_call = {
            "name": "send_message",
            "parameters": {
                "channel_id": "456789123",
                "message": "This is a test message"
            }
        }
        
        await self.moderation.run_tool(tool_call)
        
        # Check that send_message was called with the correct arguments
        self.mock_discord_wrapper.send_message.assert_called_once_with(
            "456789123", "This is a test message"
        )
    
    async def test_run_tool_delete_message(self):
        # Test running the delete_message tool
        tool_call = {
            "name": "delete_message",
            "parameters": {
                "channel_id": "456789123",
                "message_id": "987654321"
            }
        }
        
        await self.moderation.run_tool(tool_call)
        
        # Check that delete_message was called with the correct arguments
        self.mock_discord_wrapper.delete_message.assert_called_once_with(
            "456789123", "987654321"
        )
    
    async def test_run_tool_ban_user(self):
        # Test running the ban_user tool
        tool_call = {
            "name": "ban_user",
            "parameters": {
                "guild_id": "789123456",
                "user_id": "123456789"
            }
        }
        
        await self.moderation.run_tool(tool_call)
        
        # Check that ban_user was called with the correct arguments
        self.mock_discord_wrapper.ban_user.assert_called_once_with(
            "789123456", "123456789"
        )
    
    async def test_run_tool_kick_user(self):
        # Test running the kick_user tool
        tool_call = {
            "name": "kick_user",
            "parameters": {
                "guild_id": "789123456",
                "user_id": "123456789"
            }
        }
        
        await self.moderation.run_tool(tool_call)
        
        # Check that kick_user was called with the correct arguments
        self.mock_discord_wrapper.kick_user.assert_called_once_with(
            "789123456", "123456789"
        )
    
    async def test_run_tool_unban_user(self):
        # Test running the unban_user tool
        tool_call = {
            "name": "unban_user",
            "parameters": {
                "guild_id": "789123456",
                "user_id": "123456789"
            }
        }
        
        await self.moderation.run_tool(tool_call)
        
        # Check that unban_user was called with the correct arguments
        self.mock_discord_wrapper.unban_user.assert_called_once_with(
            "789123456", "123456789"
        )
    
    async def test_run_tool_unknown_tool(self):
        # Test running an unknown tool
        tool_call = {
            "name": "unknown_tool",
            "parameters": {}
        }
        
        # This should not raise an exception
        await self.moderation.run_tool(tool_call)
    
    @patch('moderation.format_discord_message')
    async def test_moderate(self, mock_format_discord_message):
        # Set up the mock format_discord_message function
        mock_format_discord_message.return_value = "Formatted message"
        
        # Set up the mock agent's send_message method
        self.mock_agent.send_message.return_value = "Response with tool calls"
        
        # Set up the mock agent's process_tool_call method
        tool_call = {
            "name": "send_message",
            "parameters": {
                "channel_id": "456789123",
                "message": "This is a response message"
            }
        }
        self.mock_agent.process_tool_call.return_value = [tool_call]
        
        # Test moderating a message
        await self.moderation.moderate(self.mock_message)
        
        # Check that ensure_server_exists was called
        self.mock_messages.ensure_server_exists.assert_called_once_with(self.mock_message)
        
        # Check that add_message was called
        self.mock_messages.add_message.assert_called_once_with(self.mock_message)
        
        # Check that format_discord_message was called
        mock_format_discord_message.assert_called_once_with(self.mock_message)
        
        # Check that send_message was called with the correct arguments
        self.mock_agent.send_message.assert_called_once()
        
        # Check that process_tool_call was called with the correct arguments
        self.mock_agent.process_tool_call.assert_called_once_with("Response with tool calls")
        
        # Check that run_tool was called with the correct arguments
        self.mock_discord_wrapper.send_message.assert_called_once_with(
            "456789123", "This is a response message"
        )
    
    @patch('moderation.format_discord_message')
    async def test_handle_user_conversation(self, mock_format_discord_message):
        # Set up the mock format_discord_message function
        mock_format_discord_message.return_value = "Formatted message"
        
        # Set up the mock agent's send_message method
        self.mock_agent.send_message.return_value = "Response with tool calls"
        
        # Set up the mock agent's process_tool_call method
        tool_call = {
            "name": "send_dm",
            "parameters": {
                "user_id": "123456789",
                "message": "This is a response DM"
            }
        }
        self.mock_agent.process_tool_call.return_value = [tool_call]
        
        # Create a DM message
        dm_message = MagicMock(spec=Message)
        dm_message.id = "987654321"
        dm_message.content = "This is a test DM"
        dm_message.guild = None
        dm_message.author = self.mock_user
        
        # Test handling a user conversation
        await self.moderation.handle_user_conversation(dm_message)
        
        # Check that add_message was called
        self.mock_messages.add_message.assert_called_once_with(dm_message)
        
        # Check that format_discord_message was called
        mock_format_discord_message.assert_called_once_with(dm_message)
        
        # Check that send_message was called with the correct arguments
        self.mock_agent.send_message.assert_called_once()
        
        # Check that process_tool_call was called with the correct arguments
        self.mock_agent.process_tool_call.assert_called_once_with("Response with tool calls")
        
        # Check that run_tool was called with the correct arguments
        self.mock_discord_wrapper.send_dm.assert_called_once_with(
            "123456789", "This is a response DM"
        )

if __name__ == "__main__":
    unittest.main() 