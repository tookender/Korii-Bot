import asyncio
import logging

import discord
import jishaku
from bot import Korii

jishaku.Flags.HIDE = True
jishaku.Flags.RETAIN = True
jishaku.Flags.NO_UNDERSCORE = True
jishaku.Flags.NO_DM_TRACEBACK = True
jishaku.Flags.USE_ANSI_ALWAYS = True
jishaku.Flags.FORCE_PAGINATOR = True


async def main():
    discord.utils.setup_logging(level=logging.INFO)

    try:
        bot = Korii()

    except Exception as error:
        return logging.warn("Failed to load Korii", exc_info=error)

    async with bot:
        await bot.start(bot.config.BOT_TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
