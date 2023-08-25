import discord
from discord.ext import commands

from utils import Korii


class PingCog(commands.Cog):
    def __init__(self, bot: Korii):
        self.bot = bot
        self.cooldown: commands.CooldownMapping = commands.CooldownMapping.from_cooldown(1, 30, commands.BucketType.guild)

    @commands.Cog.listener("on_message")
    async def ping(self, message: discord.Message):
        if message.reference and message.reference.resolved:
            return

        bucket = self.cooldown.get_bucket(message)
        
        if bucket:
            retry_after = bucket.update_rate_limit()
        else:
            retry_after = None

        if retry_after:
            return
        
        if str(self.bot.user.id) in message.content.lower():
            return await message.reply("fuck off.")
