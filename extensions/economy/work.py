import random
import re

from discord.ext import commands

from utils import Embed

from ._base import EconomyBase
from .utils import *

jobs = [
    "An old man thanks you with $40 for helping him cross the road.",
    "Dr. Doofenshmirtz rewards you with $700 for cleaning his laboratory.",
    "You helped the city exterminate the rats in the sewer for $300. Remy can stay, however.",
    "You helped in a bake sale, and earned $60.",
    "Cleaning people's shoes was a lot easier than you expected for $150.",
    "You cleaned a wealthy man's mansion for $500!",
    "You cleaned a vampire's spooky manor for $600!",
    "Apple picking is a lifestyle, and you made it work for $80.",
    "A small business appreciates your work, and gives you $150.",
    "A small business rewards you $275 for your advertising success.",
    "A large company appreciates you helping to manufacture a type of plastic and rewards you $650.",
    "The fishing industry booms again as you earn your keep for $200.",
    "👻 $1000",
    "👻👻 $2000",
    "👻👻👻 $3000",
    "A homeless man is feeling generous today, and only today. He gives you $1.",
    "A kind lady hands you $1.",
    "A dog gives you $1.",
    "You help a man pick up his fallen items, and he gives you $5.",
    "You help a woman find an item in a store aisle, and she hands you $1.",
    "Strangely, you follow a cat to the garbage and spot $5.",
    "You helped a guy take out his trash and he gives you $5!",
    "You helped a guy paint his fence for $10.",
    "You helped a guy paint his walls for $15.",
    "You helped a guy roof his house for $30.",
    "You helped a guy install a new TV for $10.",
    "You helped a guy plan out his renovations for $5.",
]


class WorkCog(EconomyBase):
    @commands.hybrid_command(description="Work a random job for a cash reward.")
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def work(self, ctx):
        job = random.choice(jobs)

        match = re.search(r"\$(\d+)", job)
        amount = int(match.group(1)) if match else 0
        await add_money(self.bot, ctx.author.id, amount)

        return await self.send_embed(
            ctx,
            text=job,
            return_embed=False,
        )
