import os
from mistralai import Mistral
import re
import json
from discord.ext import commands
from tenacity import retry, stop_after_attempt, wait_exponential

MISTRAL_MODEL = "mistral-large-latest"
SYSTEM_PROMPT = "You are a helpful assistant."

class MistralAgent:
    def __init__(self):
        MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
        self.client = Mistral(api_key=MISTRAL_API_KEY)

    def process_tool_call(self, message: str) -> list:
        matches = re.findall(r'<tool>(.*?)</tool>', message, re.DOTALL)
        tool_calls = []
        for match in matches:
            tool_calls.append(json.loads(match))
        return tool_calls

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
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