import unittest
from unittest.mock import MagicMock, patch, AsyncMock
import discord
from discord.ext import commands
from bot import on_ready, on_message, ping

class TestBot(unittest.TestCase):
    def setUp(self):
        # Create mock objects
        self.mock_bot = MagicMock(spec=commands.Bot)
        self.mock_bot.user = MagicMock()
        self.mock_bot.user.name = "TestBot"
        
        # Create a mock context for command testing
        self.mock_ctx = MagicMock()
        self.mock_ctx.send = AsyncMock()
        
        # Create a mock message
        self.mock_message = MagicMock(spec=discord.Message)
        self.mock_message.author = MagicMock(spec=discord.User)
        self.mock_message.author.bot = False
        self.mock_message.content = "Hello, bot!"
        self.mock_message.guild = MagicMock(spec=discord.Guild)
        
        # Create patches
        self.moderation_patch = patch('bot.moderation')
        
        # Start patches
        self.mock_moderation = self.moderation_patch.start()
        
        # Set up the mock moderation's methods
        self.mock_moderation.moderate = AsyncMock()
        self.mock_moderation.handle_user_conversation = AsyncMock()
    
    def tearDown(self):
        # Stop patches
        self.moderation_patch.stop()
    
    @patch('bot.logger')
    async def test_on_ready(self, mock_logger):
        # Test the on_ready event handler
        await on_ready()
        
        # Check that the logger.info was called with the correct message
        mock_logger.info.assert_called_once()
    
    async def test_on_message_bot_message(self):
        # Test handling a message from a bot
        self.mock_message.author.bot = True
        
        # Call the on_message event handler
        await on_message(self.mock_message)
        
        # Check that process_commands was called
        self.mock_bot.process_commands.assert_not_called()
        
        # Check that moderate and handle_user_conversation were not called
        self.mock_moderation.moderate.assert_not_called()
        self.mock_moderation.handle_user_conversation.assert_not_called()
    
    async def test_on_message_command(self):
        # Test handling a message that starts with the command prefix
        self.mock_message.content = "!command"
        
        # Call the on_message event handler
        await on_message(self.mock_message)
        
        # Check that process_commands was called
        self.mock_bot.process_commands.assert_called_once_with(self.mock_message)
        
        # Check that moderate and handle_user_conversation were not called
        self.mock_moderation.moderate.assert_not_called()
        self.mock_moderation.handle_user_conversation.assert_not_called()
    
    async def test_on_message_guild(self):
        # Test handling a message from a guild
        
        # Call the on_message event handler
        await on_message(self.mock_message)
        
        # Check that process_commands was called
        self.mock_bot.process_commands.assert_called_once_with(self.mock_message)
        
        # Check that moderate was called
        self.mock_moderation.moderate.assert_called_once_with(self.mock_message)
        
        # Check that handle_user_conversation was not called
        self.mock_moderation.handle_user_conversation.assert_not_called()
    
    async def test_on_message_dm(self):
        # Test handling a direct message
        self.mock_message.guild = None
        
        # Call the on_message event handler
        await on_message(self.mock_message)
        
        # Check that process_commands was called
        self.mock_bot.process_commands.assert_called_once_with(self.mock_message)
        
        # Check that moderate was not called
        self.mock_moderation.moderate.assert_not_called()
        
        # Check that handle_user_conversation was called
        self.mock_moderation.handle_user_conversation.assert_called_once_with(self.mock_message)
    
    async def test_ping_no_arg(self):
        # Test the ping command with no argument
        
        # Call the ping command
        await ping(self.mock_ctx)
        
        # Check that send was called with the correct message
        self.mock_ctx.send.assert_called_once_with("Pong!")
    
    async def test_ping_with_arg(self):
        # Test the ping command with an argument
        arg = "test argument"
        
        # Call the ping command
        await ping(self.mock_ctx, arg=arg)
        
        # Check that send was called with the correct message
        self.mock_ctx.send.assert_called_once_with(f"Pong! Your argument was {arg}")

if __name__ == "__main__":
    unittest.main() 