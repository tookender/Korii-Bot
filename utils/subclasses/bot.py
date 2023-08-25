import datetime
import logging
import pathlib
from typing import Self

import discord
import mystbin as mystbin_library
from aiohttp import ClientSession
from asyncpg import Pool
from discord.ext import commands
from tree import CommandTree


class Korii(commands.AutoShardedBot):
    user: discord.ClientUser
    pool: Pool
    session: ClientSession
    uptime: datetime.datetime
    mystbin: mystbin_library.Client
    maintenace: bool

    def __init__(self, session: ClientSession, pool: Pool, **kwargs) -> None:
        super().__init__(
            command_prefix=commands.when_mentioned_or("s!"),
            case_insensitive=True,
            strip_after_prefix=True,
            description="A multi-purpose bot with swag 😎\n" "**Website:** https://bot.korino.xyz\n" "**Docs:** https://bot.korino.xyz/docs",
            intents=discord.Intents.all(),
            allowed_mentions=discord.AllowedMentions.none(),
            tree_cls=CommandTree,
        )

        self.maintenace = False

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