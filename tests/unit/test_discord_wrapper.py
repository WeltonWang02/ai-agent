import unittest
from unittest.mock import MagicMock, patch, AsyncMock
from discord.ext import commands
from discord_wrapper import DiscordWrapper

class TestDiscordWrapper(unittest.TestCase):
    def setUp(self):
        # Create a mock bot
        self.mock_bot = MagicMock(spec=commands.Bot)
        
        # Create a DiscordWrapper instance for testing
        self.discord_wrapper = DiscordWrapper(self.mock_bot)
        
        # Create mock objects for testing
        self.mock_user = AsyncMock()
        self.mock_channel = MagicMock()
        self.mock_guild = MagicMock()
        self.mock_message = MagicMock()
        
        # Set up the mock bot's methods
        self.mock_bot.fetch_user = AsyncMock(return_value=self.mock_user)
        self.mock_bot.get_channel = MagicMock(return_value=self.mock_channel)
        self.mock_bot.get_guild = MagicMock(return_value=self.mock_guild)
        self.mock_channel.fetch_message = AsyncMock(return_value=self.mock_message)
    
    async def test_send_dm(self):
        # Test sending a DM
        user_id = "123456789"
        message = "This is a test DM"
        
        await self.discord_wrapper.send_dm(user_id, message)
        
        # Check that fetch_user was called with the correct user ID
        self.mock_bot.fetch_user.assert_called_once_with(int(user_id))
        
        # Check that send was called on the user with the correct message
        self.mock_user.send.assert_called_once_with(message)
    
    async def test_send_message(self):
        # Test sending a message to a channel
        channel_id = "987654321"
        message = "This is a test message"
        
        await self.discord_wrapper.send_message(channel_id, message)
        
        # Check that get_channel was called with the correct channel ID
        self.mock_bot.get_channel.assert_called_once_with(int(channel_id))
        
        # Check that send was called on the channel with the correct message
        self.mock_channel.send.assert_called_once_with(message)
    
    async def test_ban_user(self):
        # Test banning a user
        guild_id = "111222333"
        user_id = "123456789"
        
        await self.discord_wrapper.ban_user(guild_id, user_id)
        
        # Check that get_guild was called with the correct guild ID
        self.mock_bot.get_guild.assert_called_once_with(int(guild_id))
        
        # Check that fetch_user was called with the correct user ID
        self.mock_bot.fetch_user.assert_called_once_with(int(user_id))
        
        # Check that ban was called on the guild with the correct user
        self.mock_guild.ban.assert_called_once_with(self.mock_user)
    
    async def test_kick_user(self):
        # Test kicking a user
        guild_id = "111222333"
        user_id = "123456789"
        
        await self.discord_wrapper.kick_user(guild_id, user_id)
        
        # Check that get_guild was called with the correct guild ID
        self.mock_bot.get_guild.assert_called_once_with(int(guild_id))
        
        # Check that fetch_user was called with the correct user ID
        self.mock_bot.fetch_user.assert_called_once_with(int(user_id))
        
        # Check that kick was called on the guild with the correct user
        self.mock_guild.kick.assert_called_once_with(self.mock_user)
    
    async def test_unban_user(self):
        # Test unbanning a user
        guild_id = "111222333"
        user_id = "123456789"
        
        await self.discord_wrapper.unban_user(guild_id, user_id)
        
        # Check that get_guild was called with the correct guild ID
        self.mock_bot.get_guild.assert_called_once_with(int(guild_id))
        
        # Check that fetch_user was called with the correct user ID
        self.mock_bot.fetch_user.assert_called_once_with(int(user_id))
        
        # Check that unban was called on the guild with the correct user
        self.mock_guild.unban.assert_called_once_with(self.mock_user)
    
    async def test_delete_message(self):
        # Test deleting a message
        channel_id = "987654321"
        message_id = "123456789"
        
        await self.discord_wrapper.delete_message(channel_id, message_id)
        
        # Check that get_channel was called with the correct channel ID
        self.mock_bot.get_channel.assert_called_once_with(int(channel_id))
        
        # Check that fetch_message was called on the channel with the correct message ID
        self.mock_channel.fetch_message.assert_called_once_with(int(message_id))
        
        # Check that delete was called on the message
        self.mock_message.delete.assert_called_once()
    
    async def test_send_message_no_channel(self):
        # Test sending a message to a non-existent channel
        channel_id = "987654321"
        message = "This is a test message"
        
        # Set get_channel to return None
        self.mock_bot.get_channel.return_value = None
        
        # This should not raise an exception
        await self.discord_wrapper.send_message(channel_id, message)
        
        # Check that get_channel was called with the correct channel ID
        self.mock_bot.get_channel.assert_called_once_with(int(channel_id))
        
        # Check that send was not called
        self.mock_channel.send.assert_not_called()
    
    async def test_delete_message_no_channel(self):
        # Test deleting a message from a non-existent channel
        channel_id = "987654321"
        message_id = "123456789"
        
        # Set get_channel to return None
        self.mock_bot.get_channel.return_value = None
        
        # This should not raise an exception
        await self.discord_wrapper.delete_message(channel_id, message_id)
        
        # Check that get_channel was called with the correct channel ID
        self.mock_bot.get_channel.assert_called_once_with(int(channel_id))
        
        # Check that fetch_message was not called
        self.mock_channel.fetch_message.assert_not_called()
    
    async def test_delete_message_no_message(self):
        # Test deleting a non-existent message
        channel_id = "987654321"
        message_id = "123456789"
        
        # Set fetch_message to return None
        self.mock_channel.fetch_message.return_value = None
        
        # This should not raise an exception
        await self.discord_wrapper.delete_message(channel_id, message_id)
        
        # Check that get_channel was called with the correct channel ID
        self.mock_bot.get_channel.assert_called_once_with(int(channel_id))
        
        # Check that fetch_message was called with the correct message ID
        self.mock_channel.fetch_message.assert_called_once_with(int(message_id))

if __name__ == "__main__":
    unittest.main() 