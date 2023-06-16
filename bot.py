"""
Korii Bot: A multi-purpose bot with swag 😎
Copyright (C) 2023 Ender2K89

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import asyncio
import datetime
import logging
import pathlib

import asyncpg
import discord
import mystbin as mystbin_library
from aiohttp import ClientSession
from asyncpg import Pool
from discord.ext import commands

import config
from utils.subclasses.tree import CommandTree


class Korii(commands.AutoShardedBot):
    user: discord.ClientUser
    pool: Pool
    session: ClientSession
    uptime: datetime.datetime
    mystbin: mystbin_library.Client

    def __init__(self, *, session: ClientSession, pool: Pool, **kwargs) -> None:
        intents = discord.Intents.all()
        # intents.guild_messages = False
        
        super().__init__(
            command_prefix=commands.when_mentioned_or("s!"),
            case_insensitive=True,
            strip_after_prefix=True,
            description="A multi-purpose bot with swag 😎\n" "**Website:** https://bot.korino.xyz\n" "**Docs:** https://bot.korino.xyz/docs",
            intents=discord.Intents.all(),
            allowed_mentions=discord.AllowedMentions.none(),
            tree_cls=CommandTree,
        )

        self.pool: Pool = pool
        self.session: ClientSession = session

        self.owner_ids = {1022842005920940063, 555818548291829792}
        self.E: dict = {}  # Dictionary of all bot emojis
        self.bool_emojis = {
            True: "🟩",
            False: "🟥",
            None: "⬜",
        }

        self.ext_logger = logging.getLogger("korii.ext")
        self.cache_logger = logging.getLogger("korii.cache")
        self.levelling_cache_logger = logging.getLogger("korii.cache.levelling")

        self.files = self.lines = self.classes = self.functions = self.coroutines = self.comments = 0
    
    def bot_code(self):
        """ Loading data about the bot's code """

        path = pathlib.Path("./")
        for file in path.rglob("*.py"):
            if str(file).startswith("venv"):
                continue

            self.files += 1
            with file.open(encoding="utf-8") as file:
                for line in file.readlines():
                    line = line.strip()
                    self.lines += 1
                    if line.startswith("class"):
                        self.classes += 1
                    if line.startswith("def"):
                        self.functions += 1
                    if line.startswith("async def"):
                        self.coroutines += 1
                    if "#" in line:
                        self.comments += 1
    
    def emoji_cache(self):
        """ Loading all emojis into the emoji cache """

        emoji_guilds = [1036756543917527161, 1040293187354361857]

        success = 0
        failed = 0

        for guild in emoji_guilds:
            emoji_guild = self.get_guild(guild)

            if not emoji_guild:
                self.cache_logger.error(f"Emoji guild {guild} not found")
                failed += 1

            else:
                for emoji in emoji_guild.emojis:
                    self.E[emoji.name.lower()] = f"<{'a' if emoji.animated else ''}:owo:{emoji.id}>"

                self.cache_logger.info(f"Emoji guild {guild} has been loaded")
                success += 1

        self.cache_logger.info(f"Loaded {success} out of {success + failed} emoji guilds")

    async def load_extensions(self) -> None:
        success = 0
        failed = 0

        await self.load_extension("jishaku")

        for extension in pathlib.Path("./extensions").glob("*/__init__.py"):
            extension = str(extension.parent).replace("/", ".").replace("\\", ".")
            try:
                await self.load_extension(extension)
                self.ext_logger.info(f"Loaded {extension}")
                success += 1

            except Exception as error:
                self.ext_logger.error(f"Failed to load {extension}", exc_info=error)
                failed += 1

        return self.ext_logger.info(f"Loaded {success} out of {success + failed} extensions")

    async def on_ready(self):
        # Establishing some variables
        self.uptime = discord.utils.utcnow()
        self.mystbin = mystbin_library.Client()

        # Loading data about the bot's code
        self.bot_code()

        # Loading all emojis into the emoji cache
        self.emoji_cache()

        # Loading schemal.sql
        with open("data/schema.sql") as file:
            await self.pool.execute(file.read())
        
        # Loading all extensions
        await self.load_extensions()


async def run_bot() -> None:
    discord.utils.setup_logging(level=logging.INFO)

    async with ClientSession() as session, asyncpg.create_pool(config.DATABASE) as pool,\
        Korii(session=session, pool=pool) as bot:

        try:
            await bot.start(config.BOT_TOKEN)
        
        except KeyboardInterrupt:
            return


if __name__ == "__main__":
    asyncio.run(run_bot())