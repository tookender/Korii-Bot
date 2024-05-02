import logging
import pathlib

import discord
import mystbin as mystbin_library
import aiohttp
import asyncpg
from discord.ext import commands
import config
from typing import List


class Korii(commands.AutoShardedBot):
    pool: asyncpg.Pool | None
    user: discord.ClientUser
    owner_ids: List[int]

    def __init__(self) -> None:
        super().__init__(
            command_prefix=self.get_prefix,  # type: ignore
            case_insensitive=True,
            strip_after_prefix=True,
            description="A multi-purpose bot 👻\n" "**Website:** https://korino.dev/bot\n" "**Dashboard:** https://korino.dev/dashboard",
            intents=discord.Intents.all(),
            allowed_mentions=discord.AllowedMentions.none(),
            owner_ids=[1022842005920940063, 555818548291829792],
        )

        self.ext_logger = logging.getLogger("korii.ext")

        self.NO_PREFIX = True
        self.DEFAULT_PREFIX = "s!"

        self.color = 0x10B981
        self.messages = ["what do you want", "leave me alone", "commit alt f4", "i'm tired boss", "STOP", "WHAT", "??!??!?!?!?!?!?", "go away"]

        self.E = {}  # Dictionary of all bot emojis
        self.files = self.lines = self.classes = self.functions = self.coroutines = self.comments = 0

        self.ping_cooldown: commands.CooldownMapping = commands.CooldownMapping.from_cooldown(1, 30, commands.BucketType.guild)
        self.levelling_cooldown: commands.CooldownMapping = commands.CooldownMapping.from_cooldown(1, 45, commands.BucketType.member)

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
        self.pool = await asyncpg.create_pool(config.DATABASE)

        if not self.pool:
            raise RuntimeError("Failed to connect with the database.")

        with open("data/schema.sql") as file:
            await self.pool.execute(file.read())

        self.bot_code()
        await self.load_extensions()

    async def start(self) -> None:
        discord.utils.setup_logging(level=logging.INFO)

        self.uptime = discord.utils.utcnow()
        self.session = aiohttp.ClientSession()
        self.mystbin = mystbin_library.Client()

        await super().start(config.BOT_TOKEN, reconnect=True)

    async def get_prefix(self, message: discord.Message, /) -> List[str] | str:
        prefixes: List[str] = []
        prefixes.append(self.DEFAULT_PREFIX)

        if (not message.guild or message.author.id in self.owner_ids) and self.NO_PREFIX:
            prefixes.append("")

        return commands.when_mentioned_or(*prefixes)(self, message)
