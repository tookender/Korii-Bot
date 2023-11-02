import logging
import pathlib

import discord
import mystbin as mystbin_library
import aiohttp
import asyncpg
from discord.ext import commands
import config
from typing import Any


class Korii(commands.AutoShardedBot):
    user: discord.ClientUser

    def __init__(self) -> None:
        super().__init__(
            command_prefix=commands.when_mentioned_or("s!"),
            case_insensitive=True,
            strip_after_prefix=True,
            description="A multi-purpose bot with swag 😎\n" "**Website:** https://bot.korino.dev\n" "**Docs:** https://bot.korino.dev/docs",
            intents=discord.Intents.all(),
            allowed_mentions=discord.AllowedMentions.none(),
            owner_ids=[1022842005920940063, 555818548291829792],
        )

        self.ext_logger = logging.getLogger("korii.ext")
        self.cache_logger = logging.getLogger("korii.cache")

        self.E = {}  # Dictionary of all bot emojis
        self.files = self.lines = self.classes = self.functions = self.coroutines = self.comments = 0

    def bot_code(self):
        """Loading data about the bot's code"""

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
        """Loading all emojis into the emoji cache"""

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

        for file in pathlib.Path("./extensions").glob("*.py"):
            *tree, _ = file.parts
            try:
                await self.load_extension(f"{'.'.join(tree)}.{file.stem}")
                self.ext_logger.info(f"Loaded {file}")
                success += 1

            except Exception as error:
                self.ext_logger.error(f"Failed to load {file}", exc_info=error)
                failed += 1

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

    async def setup_hook(self) -> None:
        self.pool: asyncpg.Pool = await asyncpg.create_pool(config.DATABASE)

        if not self.pool:
            raise RuntimeError("Failed connecting to database.")

        with open("data/schema.sql") as file:
            await self.pool.execute(file.read())

        self.bot_code()
        self.emoji_cache()
        await self.load_extensions()

    async def start(self) -> None:
        discord.utils.setup_logging(level=logging.INFO)

        async with aiohttp.ClientSession() as session:
            self.session = session

        self.uptime = discord.utils.utcnow()
        self.mystbin = mystbin_library.Client()

        await super().start(config.BOT_TOKEN, reconnect=True)
