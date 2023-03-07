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
import logging
import pathlib

import aiohttp
import asyncpg
import discord
import jishaku
import mystbin

from bot import BOT_TOKEN, DATABASE, Korii, LevellingCacheManager

jishaku.Flags.HIDE = True
jishaku.Flags.NO_UNDERSCORE = True
jishaku.Flags.NO_DM_TRACEBACK = True
jishaku.Flags.USE_ANSI_ALWAYS = True
jishaku.Flags.FORCE_PAGINATOR = True

discord.VoiceClient.warn_nacl = False


async def load_extensions(bot: Korii) -> None:
    success = 0
    failed = 0

    await bot.load_extension("jishaku")

    for extension in pathlib.Path("./bot/extensions").glob("*/__init__.py"):
        extension = str(extension.parent).replace("/", ".").replace("\\", ".")
        try:
            await bot.load_extension(extension)
            bot.ext_logger.info(f"Loaded {extension}")
            success += 1
        
        except Exception as error:
            bot.ext_logger.error(f"Failed to load {extension}", exc_info=error)
            failed += 1
    
    return bot.ext_logger.info(f"Loaded {success} out of {success + failed} extensions")


async def main():
    discord.utils.setup_logging(level=logging.INFO)

    async with Korii() as bot, aiohttp.ClientSession() as session, asyncpg.create_pool(DATABASE) as pool, LevellingCacheManager(pool) as level_cache:
        bot.pool = pool
        bot.session = session
        bot.uptime = discord.utils.utcnow()
        bot.mystbin = mystbin.Client(session=session)
        bot.levelling_cache = level_cache

        with open("schema.sql") as file:
            await bot.pool.execute(file.read())

        await load_extensions(bot)

        await bot.start(BOT_TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
