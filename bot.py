import logging
import pathlib
import typing
from collections import defaultdict
from typing import List, Type

import aiohttp
import asyncpg
import discord
import mystbin as mystbin_library
from discord.ext import commands

import config
from utils.context import CustomContext
from utils.logging import LoggingEventsFlags


class LoggingConfig:
    __slots__ = ("default", "message", "member", "join_leave", "voice", "server")

    def __init__(self, default, message, member, join_leave, voice, server):
        self.default = default
        self.message = message
        self.member = member
        self.join_leave = join_leave
        self.voice = voice
        self.server = server

    def _replace(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class Korii(commands.AutoShardedBot):
    pool: asyncpg.Pool
    user: discord.ClientUser
    owner_ids: List[int]

    def __init__(self) -> None:
        super().__init__(
            command_prefix=self.get_prefix,
            case_insensitive=True,
            strip_after_prefix=True,
            description="A multi-purpose bot 👻\n" "**Website:** https://korino.dev/bot\n" "**Dashboard:** https://korino.dev/dashboard",
            intents=discord.Intents.all(),
            allowed_mentions=discord.AllowedMentions.none(),
            owner_ids=[1022842005920940063, 812015432370356224, 555818548291829792, 916964266274324502],
        )

        self.ext_logger = logging.getLogger("korii.ext")

        self.NO_PREFIX = False
        self.DEFAULT_PREFIX = "s!"

        self.color = 0x10B981
        self.messages = ["what do you want", "leave me alone", "commit alt f4", "i'm tired boss", "STOP", "WHAT", "??!??!?!?!?!?!?", "go away"]

        self.E = {}  # Dictionary of all bot emojis
        self.files = self.lines = self.classes = self.functions = self.coroutines = self.comments = 0

        self.prank_messages = self.lucky_messages = self.unlucky_messages = []

        self.ping_cooldown: commands.CooldownMapping = commands.CooldownMapping.from_cooldown(1, 5, commands.BucketType.user)
        self.levelling_cooldown: commands.CooldownMapping = commands.CooldownMapping.from_cooldown(1, 45, commands.BucketType.member)

        self.log_webhooks: Type[LoggingConfig] = LoggingConfig
        self.log_channels: typing.Dict[int, LoggingConfig] = {}
        self.log_cache = defaultdict(lambda: defaultdict(list))
        self.guild_loggings: typing.Dict[int, LoggingEventsFlags] = {}


    def tick(self, boolean: bool | None):
        if boolean == True:
            return self.E["yes"]
        elif boolean == False:
            return self.E["no"]
        else:
            return self.E["hyphen"]

    def fill(self, name: str, variable: list):
        file = open(name, encoding="utf-8")
        for line in file.readlines():
            if not line.startswith("##"):
                variable.append(line.replace("\n", ""))

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

    def update_log(self, deliver_type: str, webhook_url: str, guild_id: int):
        guild_id = getattr(guild_id, "id", guild_id)
        if deliver_type == "default":
            self.log_channels[guild_id]._replace(default=webhook_url)
        elif deliver_type == "message":
            self.log_channels[guild_id]._replace(message=webhook_url)
        elif deliver_type == "member":
            self.log_channels[guild_id]._replace(member=webhook_url)
        elif deliver_type == "join_leave":
            self.log_channels[guild_id]._replace(join_leave=webhook_url)
        elif deliver_type == "voice":
            self.log_channels[guild_id]._replace(voice=webhook_url)
        elif deliver_type == "server":
            self.log_channels[guild_id]._replace(server=webhook_url)

    async def load_emojis(self) -> None:
        await self.wait_until_ready()
        EMOJI_GUILDS = [1036756543917527161, 1040293187354361857]

        for guild_id in EMOJI_GUILDS:
            guild = self.get_guild(guild_id)
            assert guild
            emojis = guild.emojis
            for emoji in emojis:
                self.E[f"{emoji.name}"] = f"<:ghost:{emoji.id}>"

    async def on_ready(self):
        await self.load_emojis()

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
        self.pool = await asyncpg.create_pool(config.DATABASE) # type: ignore

        if not self.pool:
            raise RuntimeError("Failed to connect with the database.")

        with open("data/schema.sql") as file:
            await self.pool.execute(file.read())

        self.bot_code()
        await self.load_extensions()
        await self.populate_cache()

    async def start(self) -> None:
        discord.utils.setup_logging(level=logging.INFO)

        self.uptime = discord.utils.utcnow()
        self.session = aiohttp.ClientSession()
        self.mystbin = mystbin_library.Client()

        self.fill("data/messages/prank_messages.txt", self.prank_messages)
        self.fill("data/messages/lucky_messages.txt", self.lucky_messages)

        await super().start(config.BOT_TOKEN, reconnect=True)

    async def get_prefix(self, message: discord.Message, /) -> List[str] | str:
        prefixes: List[str] = []
        prefixes.append(self.DEFAULT_PREFIX)

        if (not message.guild or message.author.id in self.owner_ids) and self.NO_PREFIX:
            prefixes.append("")

        return commands.when_mentioned_or(*prefixes)(self, message)

    async def get_context(self, message, *, cls=CustomContext):
        return await super().get_context(message, cls=cls)

    async def populate_cache(self):
        for entry in await self.pool.fetch("SELECT * FROM log_channels"):
            guild_id = entry["guild_id"]
            await self.pool.execute(
                "INSERT INTO logging_events(guild_id) VALUES ($1) ON CONFLICT (guild_id) DO NOTHING",
                entry["guild_id"],
            )

            self.log_channels[guild_id] = LoggingConfig(
                default=entry["default_channel"],
                message=entry["message_channel"],
                join_leave=entry["join_leave_channel"],
                member=entry["member_channel"],
                voice=entry["voice_channel"],
                server=entry["server_channel"],
            )

            flags = dict(
                await self.pool.fetchrow(
                    "SELECT message_delete, message_purge, message_edit, member_join, member_leave, member_update, user_ban, user_unban, "
                    "user_update, invite_create, invite_delete, voice_join, voice_leave, voice_move, voice_mod, emoji_create, emoji_delete, "
                    "emoji_update, sticker_create, sticker_delete, sticker_update, server_update, stage_open, stage_close, channel_create, "
                    "channel_delete, channel_edit, role_create, role_delete, role_edit FROM logging_events WHERE guild_id = $1",
                    guild_id,
                )
            )
            self.guild_loggings[guild_id] = LoggingEventsFlags(**flags)

        logging.info(f"All cache populated successfully")
