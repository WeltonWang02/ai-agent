import os
from mistralai import Mistral
import re
import json
from discord.ext import commands
from moderation import TOOLS

MISTRAL_MODEL = "mistral-large-latest"
SYSTEM_PROMPT = "You are a helpful assistant."



class MistralAgent:
    def __init__(self):
        MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
        self.client = Mistral(api_key=MISTRAL_API_KEY)

    def process_tool_call(self, message: str) -> dict:
        match = re.search(r'<tool>(.*?)</tool>', message)
        if match:
            tool_call = match.group(1)
            return json.loads(tool_call)
        return None

    async def send_message(self, message: str, system_prompt: str = SYSTEM_PROMPT) -> str:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message},
        ]

        response = await self.client.chat.complete_async(
            model=MISTRAL_MODEL,
            messages=messages,
        )

        return response.choices[0].message.content        