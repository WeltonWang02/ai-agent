from agent import OpenAIAgent
import discord
import logging

from messages import SingleMessage

logger = logging.getLogger(__name__)

class Summarizer:
    def __init__(self):
        self.agent = OpenAIAgent()

    async def summarize_messages(self, messages: list) -> str:
        # Prepare the message content for summarization
        message_content = "\n".join([
            f"{msg.author.name}: {msg.content}" if isinstance(msg, discord.Message) else f"{msg.user_name}: {msg.content}" 
            for msg in messages
        ])

        # Define a prompt for summarization
        summarization_prompt = f"Summarize the following conversation:\n{message_content}"

        # Use the Mistral agent to generate a summary
        summary = await self.agent.send_message(summarization_prompt)

        logger.info(f"Generated summary: {summary}")
        return summary

    def format_message(self, msg) -> str:
        if isinstance(msg, discord.Message):
            return f"{msg.author.name}: {msg.content}"
        elif isinstance(msg, SingleMessage):
            return f"{msg.user_name}: {msg.content}"
        else:
            return "Unknown message type"