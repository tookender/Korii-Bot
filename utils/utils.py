import datetime
import itertools
import time
from typing import Coroutine

import discord
import pygit2

from bot import Korii


async def shorten_text(bot: Korii, text: str, length: int | None = None, code: int | None = None, link: bool = False):
    """A function to shorten text
    shorten_text("Hello World", 6) --> Hello
    shorten_text("Hello World", 6, link=True) --> Hello [...](link)
    shorten_text("Hello World", 6, code=True) --> ```{code}\nHello\n```[...](link)
    """

    if not length:
        url = await bot.mystbin.create_paste(filename="OwO.txt", content=text)

        return url

    if not link:
        return text[:length]

    if len(text) <= length:
        return text

    url = await bot.mystbin.create_paste(filename="OwO.txt", content=text)
    text = text[:length]

    if code:
        return f"```{code}\n{text}```[...]({url} 'But wait, there is more!')"

    return f"{text}[...]({url} 'But wait, there is more!')"


async def timeit(coro: Coroutine) -> float:
    start = time.perf_counter()
    await coro
    end = time.perf_counter()

    return (end - start) * 1000


def format_commit(commit: pygit2.Commit) -> str:
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


def get_latest_commits(count=5):
    repo = pygit2.Repository(".git")
    commits = list(itertools.islice(repo.walk(repo.head.target, pygit2.GIT_SORT_TOPOLOGICAL), count))
    return "\n".join(format_commit(c) for c in commits)


def yes_no(bool: bool):
    """Returns yes if the value is True and no if the value is False"""
    if bool:
        return "Yes"

    return "No"


@discord.utils.copy_doc(yes_no)
def yn(bool: bool):
    return yes_no(bool)


def to_boolean(argument: str) -> bool:
    lowered = argument.lower()
    if lowered in ("yes", "y", "true", "t", "1", "on", "truth", "ye", "yeah", "yup"):
        return True
    elif lowered in ("no", "n", "false", "f", "0", "off", "na", "nah", "nop", "nope"):
        return False
    else:
        return True
