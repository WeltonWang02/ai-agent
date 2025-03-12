from discord.ext import commands

class DiscordWrapper:
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def send_dm(self, user_id: str, message: str):
        user = await self.bot.fetch_user(int(user_id))
        await user.send(message)

    async def send_message(self, channel_id: str, message: str):
        channel = self.bot.get_channel(int(channel_id))
        if channel:
            await channel.send(message)

    async def ban_user(self, guild_id: str, user_id: str):
        guild = self.bot.get_guild(int(guild_id))
        user = await self.bot.fetch_user(int(user_id))
        if guild and user:
            await guild.ban(user)

    async def kick_user(self, guild_id: str, user_id: str):
        guild = self.bot.get_guild(int(guild_id))
        user = await self.bot.fetch_user(int(user_id))
        if guild and user:
            await guild.kick(user)

    async def unban_user(self, guild_id: str, user_id: str):
        guild = self.bot.get_guild(int(guild_id))
        if guild:
            await guild.unban(user_id)

    async def delete_message(self, channel_id: str, message_id: str):
        channel = self.bot.get_channel(int(channel_id))
        if channel:
            message = await channel.fetch_message(int(message_id))
            if message:
                await message.delete()  
