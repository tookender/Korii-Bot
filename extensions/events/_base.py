import datetime, pytz
from discord.ext import commands, tasks

from bot import Korii


class EventsBase(commands.Cog):
    def __init__(self, bot: Korii):
        self.bot = bot
        self.quests.start()
        self.gifts.start()
    
    def cog_unload(self):
        self.quests.cancel()
        self.gifts.cancel()

    @tasks.loop(minutes=1)
    async def quests(self):
        now = datetime.datetime.now()

        if now.weekday() == 2:
            if now.hour == 16 and now.minute == 0:
                channel = self.bot.get_channel(1269897035327209504)
                await channel.send("📅 | Weekly quests have refreshed!")
        else:
            if now.hour == 16 and now.minute == 0:
                channel = self.bot.get_channel(1269897035327209504)
                await channel.send("🗓️ | Daily quests have refreshed.")

    @tasks.loop(minutes=1)
    async def gifts(self):
        now = datetime.datetime.now()

        if now.hour == 3 and now.minute == 40:
            channel = self.bot.get_channel(1269897035327209504)
            await channel.send("🎁 | Go claim your daily gift!")