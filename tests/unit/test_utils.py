import unittest
from unittest.mock import MagicMock, patch
from discord import Message
from messages import SingleMessage, ModAction

# Import the functions to test
from utils import format_message, format_single_message, format_discord_message, format_mod_action

class TestUtils(unittest.TestCase):
    def setUp(self):
        # Create mock objects for testing
        self.mock_message = MagicMock(spec=Message)
        self.mock_message.author.name = "TestUser"
        self.mock_message.author.id = "123456789"
        self.mock_message.id = "987654321"
        self.mock_message.channel.name = "test-channel"
        self.mock_message.channel.id = "456789123"
        self.mock_message.guild.name = "Test Server"
        self.mock_message.guild.id = "789123456"
        self.mock_message.content = "This is a test message"
        
        # Create a SingleMessage object for testing
        self.single_message = SingleMessage(
            content="This is a test message",
            server_id="789123456",
            server_name="Test Server",
            user_id="123456789",
            user_name="TestUser",
            channel_id="456789123",
            channel_name="test-channel",
            message_id="987654321"
        )
        
        # Create a ModAction object for testing
        self.mod_action = ModAction(
            action="delete",
            message=self.single_message
        )
    
    def test_format_message(self):
        # Test the format_message function
        expected_output = "TestUser (user id: 123456789, message id: 987654321) in test-channel (channel id: 456789123) in server Test Server (server id: 789123456):\nThis is a test message"
        self.assertEqual(format_message(self.mock_message), expected_output)
    
    def test_format_single_message(self):
        # Test the format_single_message function
        expected_output = "TestUser (user id: 123456789, message id: 987654321) in test-channel (channel id: 456789123) in server Test Server (server id: 789123456):\nThis is a test message"
        self.assertEqual(format_single_message(self.single_message), expected_output)
    
    def test_format_discord_message_guild(self):
        # Test the format_discord_message function with a guild message
        expected_output = "TestUser (user id: 123456789, message id: 987654321) in test-channel (channel id: 456789123) in server Test Server (server id: 789123456):\nThis is a test message"
        self.assertEqual(format_discord_message(self.mock_message), expected_output)
    
    def test_format_discord_message_dm(self):
        # Test the format_discord_message function with a DM message
        dm_message = MagicMock(spec=Message)
        dm_message.author.name = "TestUser"
        dm_message.author.id = "123456789"
        dm_message.id = "987654321"
        dm_message.content = "This is a test DM"
        dm_message.guild = None
        
        expected_output = "TestUser (user id: 123456789, message id: 987654321) in DM:\nThis is a test DM"
        self.assertEqual(format_discord_message(dm_message), expected_output)
    
    def test_format_mod_action(self):
        # Test the format_mod_action function
        expected_output = "delete (user id: 123456789, message id: 987654321) in test-channel (channel id: 456789123) in server Test Server (server id: 789123456):\nThis is a test message"
        self.assertEqual(format_mod_action(self.mod_action), expected_output)

if __name__ == "__main__":
    unittest.main() 