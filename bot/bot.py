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

import datetime
import itertools
import logging
import pathlib
import time
from typing import Coroutine

import aiohttp
import asyncpg
import discord
import mystbin as mystbin_library
import pygit2
from discord.ext import commands

from bot import CommandTree, LevellingCacheManager


class Korii(commands.AutoShardedBot):
    user: discord.ClientUser
    pool: asyncpg.Pool
    session: aiohttp.ClientSession
    uptime: datetime.datetime
    mystbin: mystbin_library.Client
    levelling_cache: LevellingCacheManager

    def __init__(self):
        super().__init__(
            command_prefix=commands.when_mentioned_or("s!"),
            description="A multi-purpose bot with swag 😎\n" "**Website:** https://bot.korino.xyz\n" "**Docs:** https://bot.korino.xyz/docs",
            intents=discord.Intents.all(),
            allowed_mentions=discord.AllowedMentions.none(),
            tree_cls=CommandTree,
        )

        self.owner_ids = {1022842005920940063, 555818548291829792}
        self.E: dict = {}  # Dictionary of all bot emojis

        self.ext_logger = logging.getLogger("korino.ext")
        self.cache_logger = logging.getLogger("korino.cache")
        self.levelling_cache_logger = logging.getLogger("korino.cache.levelling")

        self.files = self.lines = self.classes = self.functions = self.coroutines = self.comments = 0

    async def on_ready(self):
        # Loading data about the bot's code
        path = pathlib.Path("./")
        for file in path.rglob("*.py"):
            if str(file).startswith("venv"):
                continue

            self.files += 1
            with file.open() as file:
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

        # Loading all emojis into the emoji cache

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

    async def shorten_text(self, text: str, length: int | None = None, code: int | None = None, link: bool = False):
        """A function to shorten text
        shorten_text("Hello World", 6) --> Hello
        shorten_text("Hello World", 6, link=True) --> Hello [...](link)
        shorten_text("Hello World", 6, code=True) --> ```{code}\nHello\n```[...](link)
        """

        if not length:
            url = await self.mystbin.create_paste(filename="OwO.txt", content=text)

            return url

        if not link:
            return text[:length]

        if len(text) <= length:
            return text

        url = await self.mystbin.create_paste(filename="OwO.txt", content=text)
        text = text[:length]

        if code:
            return f"```{code}\n{text}```[...]({url} 'But wait, there is more!')"

        return f"{text}[...]({url} 'But wait, there is more!')"

    async def timeit(self, coro: Coroutine) -> float:
        start = time.perf_counter()
        await coro
        end = time.perf_counter()

        return (end - start) * 1000

    def format_commit(self, commit: pygit2.Commit) -> str:
        short, _, _ = commit.message.partition("\n")
        short_sha2 = commit.hex[0:6]
        commit_tz = datetime.timezone(datetime.timedelta(minutes=commit.commit_time_offset))
        commit_time = datetime.datetime.fromtimestamp(commit.commit_time).astimezone(commit_tz)

        # [`hash`](url) message (offset)
        offset = discord.utils.format_dt(commit_time.astimezone(datetime.timezone.utc), style="R")
        short = short.split(" ")
        emoji = short[0]
        short.pop(0)
        short = " ".join(short)
        return f"[`{short_sha2}`](https://github.com/Korino-Development/Korii-Bot/commit/{commit.hex}) {short}"

    def get_latest_commits(self, count=5):
        repo = pygit2.Repository(".git")
        commits = list(itertools.islice(repo.walk(repo.head.target, pygit2.GIT_SORT_TOPOLOGICAL), count))
        return "\n".join(self.format_commit(c) for c in commits)

    def yes_no(self, bool: bool):
        """Returns yes if the value is True and no if the value is False"""
        if bool:
            return "Yes"

        return "No"

    @discord.utils.copy_doc(yes_no)
    def yn(self, bool: bool):
        return self.yes_no(bool)
