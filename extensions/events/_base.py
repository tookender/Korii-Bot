import datetime, pytz
from discord.ext import commands, tasks

from bot import Korii


class EventsBase(commands.Cog):
    def __init__(self, bot: Korii):
        self.bot = bot
        self.quests.start()
    
    def cog_unload(self):
        self.quests.cancel()

    @tasks.loop(minutes=1)
    async def quests(self):
        now = datetime.datetime.now()

        if now.weekday() == 2:
            if now.hour == 16 and now.minute == 0:
                channel = self.bot.get_channel(1269897035327209504)
                await channel.send("⚠️ | Weekly Quests have been refreshed")
        else:
            if now.hour == 16 and now.minute == 0:
                channel = self.bot.get_channel(1269897035327209504)
                await channel.send("⚠️ | Daily Quests have been refreshed")

    @tasks.loop(time=datetime.time(hour=10, minute=0))
    async def before(self):
        timezone = pytz.timezone("America/Chicago")
        time = timezone.localize(datetime.datetime.now().replace(hour=19, minute=0, second=0, microsecond=0))
        unix_timestamp = int(time.timestamp())

        channel = self.bot.get_channel(1269897035327209504)
        await channel.send(f"⚠️ | Make sure to log in before <t:{unix_timestamp}:F>") 