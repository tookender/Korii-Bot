import datetime
import itertools
import time
from typing import Coroutine

import discord
import pygit2


def tick(boolean: bool | None):
    if boolean == True:
        return "<:yes:1036761765322686505>"
    elif boolean == False:
        return "<:no:1036761731806003210>"
    else:
        return "<:icons_hyphen:1240731518175809556>"

async def shorten_text(bot, text: str, length: int | None = None, code: int | None = None, link: bool = False):
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

def get_member_permissions(permissions: discord.Permissions):
    perms = []
    
    if permissions.administrator:
        perms.append("Administrator")
        
        return "Administrator"
    
    if permissions.manage_guild:
        perms.append("Manage guild")
        
    if permissions.ban_members:
        perms.append("Ban members")
        
    if permissions.kick_members:
        perms.append("Kick members")
        
    if permissions.manage_channels:
        perms.append("Manage channels")
        
    if permissions.manage_emojis:
        perms.append("Manage custom emotes")
        
    if permissions.manage_messages:
        perms.append("Manage messages")
        
    if permissions.manage_permissions:
        perms.append("Manage permissions")
        
    if permissions.manage_roles:
        perms.append("Manage roles")
        
    if permissions.mention_everyone:
        perms.append("Mention everyone")
        
    if permissions.manage_emojis:
        perms.append("Manage emojis")
        
    if permissions.manage_webhooks:
        perms.append("Manage webhooks")
        
    if permissions.move_members:
        perms.append("Move members")
        
    if permissions.mute_members:
        perms.append("Mute members")
        
    if permissions.deafen_members:
        perms.append("Deafen members")
        
    if permissions.priority_speaker:
        perms.append("Priority speaker")
        
    if permissions.view_audit_log:
        perms.append("See audit log")
        
    if permissions.create_instant_invite:
        perms.append("Create instant invites")
    
    return ", ".join(perms) if perms else 'No permissions'

def col(color=None, /, *, fmt=0, bg=False):
    base = "\u001b["
    if fmt != 0:
        base += "{fmt};"
    if color is None:
        base += "{color}m"
        color = 0
    else:
        if bg is True:
            base += "4{color}m"
        else:
            base += "3{color}m"
    return base.format(fmt=fmt, color=color)