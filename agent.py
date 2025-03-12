import os
from mistralai import Mistral
import re
import json

MISTRAL_MODEL = "mistral-large-latest"
SYSTEM_PROMPT = "You are a helpful assistant."

TOOLS = [
    {
        "name": "send_dm",
        "description": "Send a direct message to a user",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {"type": "string", "description": "The ID of the user to send the message to"},
                "message": {"type": "string", "description": "The message to send to the user"}
            }
        }
    },
    {
        "name": "delete_message",
        "description": "Delete a message from a channel",
        "parameters": {
            "type": "object",
            "properties": {
                "channel_id": {"type": "string", "description": "The ID of the channel to send the message to"},
                "message": {"type": "string", "description": "The message to send to the channel"}
            }
        }
    },
    {   
        "name": "ban_user",
        "description": "Ban a user from a server",
        "parameters": {
            "type": "object",
            "properties": {
                "server_id": {"type": "string", "description": "The ID of the server to ban the user from"},
                "user_id": {"type": "string", "description": "The ID of the user to ban from the server"}
            }
        }
    }
]


class MistralAgent:
    def __init__(self):
        MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

        self.client = Mistral(api_key=MISTRAL_API_KEY)

    def _get_tool_call(self, message: str) -> dict:
        match = re.search(r'<tool>(.*?)</tool>', message)
        if match:
            tool_call = match.group(1)
            return json.loads(tool_call)
        return None

    async def _send_message(self, message: str) -> str:
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": message},
        ]

        response = await self.client.chat.complete_async(
            model=MISTRAL_MODEL,
            messages=messages,
        )

        return response.choices[0].message.content        

    async def _process_tool_call(self, message: str ) -> str:
        try:    
            tool_call = self._get_tool_call(message)
            if tool_call:
                return tool_call
            else:
                return "No tool call found"
        except Exception as e:
            return f"Error: {e}"