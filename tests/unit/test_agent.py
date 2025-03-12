import unittest
from unittest.mock import MagicMock, patch, AsyncMock
import json
import os
from agent import MistralAgent

class TestMistralAgent(unittest.TestCase):
    def setUp(self):
        # Create a patch for the Mistral client
        self.mistral_client_patch = patch('agent.Mistral')
        self.mock_mistral_client = self.mistral_client_patch.start()
        
        # Create a mock for the Mistral client instance
        self.mock_client_instance = MagicMock()
        self.mock_mistral_client.return_value = self.mock_client_instance
        
        # Create a mock for the chat.complete_async method
        self.mock_client_instance.chat = MagicMock()
        self.mock_client_instance.chat.complete_async = AsyncMock()
        
        # Create a MistralAgent instance for testing
        self.agent = MistralAgent()
    
    def tearDown(self):
        # Stop the patch
        self.mistral_client_patch.stop()
    
    def test_init(self):
        # Test that the MistralAgent initializes correctly
        self.assertEqual(self.agent.client, self.mock_client_instance)
        self.mock_mistral_client.assert_called_once()
    
    def test_process_tool_call_single(self):
        # Test processing a single tool call
        message = "Here's a tool call: <tool>{\"name\": \"test_tool\", \"parameters\": {\"param1\": \"value1\"}}</tool>"
        expected_tool_calls = [{"name": "test_tool", "parameters": {"param1": "value1"}}]
        
        tool_calls = self.agent.process_tool_call(message)
        
        self.assertEqual(tool_calls, expected_tool_calls)
    
    def test_process_tool_call_multiple(self):
        # Test processing multiple tool calls
        message = """
        Here's the first tool call: <tool>{"name": "tool1", "parameters": {"param1": "value1"}}</tool>
        And here's another: <tool>{"name": "tool2", "parameters": {"param2": "value2"}}</tool>
        """
        expected_tool_calls = [
            {"name": "tool1", "parameters": {"param1": "value1"}},
            {"name": "tool2", "parameters": {"param2": "value2"}}
        ]
        
        tool_calls = self.agent.process_tool_call(message)
        
        self.assertEqual(tool_calls, expected_tool_calls)
    
    def test_process_tool_call_no_tools(self):
        # Test processing a message with no tool calls
        message = "This message doesn't contain any tool calls."
        
        tool_calls = self.agent.process_tool_call(message)
        
        self.assertEqual(tool_calls, [])
    
    @patch('agent.MISTRAL_MODEL', 'test-model')
    async def test_send_message(self):
        # Create a mock response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message = MagicMock()
        mock_response.choices[0].message.content = "This is a test response"
        
        # Set the mock response for the complete_async method
        self.mock_client_instance.chat.complete_async.return_value = mock_response
        
        # Test sending a message
        message = "This is a test message"
        system_prompt = "This is a test system prompt"
        
        response = await self.agent.send_message(message, system_prompt)
        
        # Check that the complete_async method was called with the correct arguments
        self.mock_client_instance.chat.complete_async.assert_called_once_with(
            model='test-model',
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message},
            ],
        )
        
        # Check that the correct response was returned
        self.assertEqual(response, "This is a test response")
    
    @patch('agent.MISTRAL_MODEL', 'test-model')
    @patch('agent.SYSTEM_PROMPT', 'default-system-prompt')
    async def test_send_message_default_system_prompt(self):
        # Create a mock response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message = MagicMock()
        mock_response.choices[0].message.content = "This is a test response"
        
        # Set the mock response for the complete_async method
        self.mock_client_instance.chat.complete_async.return_value = mock_response
        
        # Test sending a message with the default system prompt
        message = "This is a test message"
        
        response = await self.agent.send_message(message)
        
        # Check that the complete_async method was called with the correct arguments
        self.mock_client_instance.chat.complete_async.assert_called_once_with(
            model='test-model',
            messages=[
                {"role": "system", "content": "default-system-prompt"},
                {"role": "user", "content": message},
            ],
        )
        
        # Check that the correct response was returned
        self.assertEqual(response, "This is a test response")

if __name__ == "__main__":
    unittest.main() 