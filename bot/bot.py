import logging
import random
from datetime import datetime

import aiohttp
import asyncpg
import config
import discord
import mystbin as mystbin_library
from discord import Embed, app_commands
from discord.ext import commands
from utilities.classes.config import Configuration


class KoriiComandTree(app_commands.CommandTree):
    async def on_error(
        self,
        interaction: discord.Interaction,
        error: app_commands.AppCommandError,
    ) -> None:
        if interaction.command:
            embed = Embed(
                title=f"{interaction.client.E['close']} Error",  # type: ignore
                color=discord.Color.red(),
            )

            embed.add_field(name="Reason", value=error)

        embed = Embed(
            title=f"{interaction.client.E['close']} Unexpected Error",  # type: ignore
            description="We are sorry for this inconvenience.\n"
            "The developers have been notified about this and will fix it.",
            color=discord.Color.red(),
        )

        embed.add_field(name="Reason", value=error)

        if interaction.response.is_done():
            return await interaction.followup.send(embed=embed, ephemeral=True)

        return await interaction.response.send_message(embed=embed, ephemeral=True)


class Korii(commands.AutoShardedBot):
    pool: asyncpg.Pool
    session: aiohttp.ClientSession
    mystbin: mystbin_library.Client

    __slots__: tuple = (
        "pool",
        "session",
        "mystbin",
    )

    def __init__(self, **kwargs):
        super().__init__(
            command_prefix=commands.when_mentioned_or("s!"),
            description="A multi-purpose bot with swag 😎\n"
            "**Website:** https://bot.korino.xyz\n"
            "**Docs:** https://bot.korino.xyz/docs",
            intents=discord.Intents.all(),
            allowed_mentions=discord.AllowedMentions.none(),
            tree_cls=KoriiComandTree,
            **kwargs,
        )
        self.config: Configuration = Configuration(
            BOT_TOKEN=config.BOT_TOKEN,
            POSTGRESQL=config.DATABASE,
            EXTENSIONS=config.EXTENSIONS,
        )

        self.owner_ids = {1022842005920940063, 746807014658801704}
        self.E: dict = {}  # This will be a dictionary of all cool emojis

        self.website = "https://bot.korino.xyz"
        self.source = "https://bot.korino.xyz/source"
        self.invite = "https://bot.korino.xyz/invite"
        self.docs = "https://bot.korino.xyz/docs"

    @staticmethod
    def random_pastel_color() -> discord.Color:
        return discord.Color.from_hsv(random.random(), 0.28, 0.97)

    @staticmethod
    def random_neon_color() -> discord.Color:
        return discord.Color.from_hsv(random.random(), 0.7, 1.0)

    async def on_ready(self) -> None:
        if not hasattr(self, "launch_time"):
            self.launch_time = discord.utils.utcnow()

        # Here we are loading all emojis into the emoji cache

        emoji_guilds = [1036756543917527161, 1040293187354361857]

        for guild in emoji_guilds:
            emoji_guild = self.get_guild(guild)

            if not emoji_guild:
                logging.error(f"[CACHE] Emoji guild {guild} not found")

            else:
                for emoji in emoji_guild.emojis:
                    self.E[emoji.name.lower()] = f"<{'a' if emoji.animated else ''}:owo:{emoji.id}>"

                logging.info(f"[CACHE] Emoji guild {guild} has been loaded")

    async def setup_hook(self):
        # Initializing the database

        try:
            self.pool = await asyncpg.create_pool(self.config.POSTGRESQL)  # type: ignore
            logging.info("[DB] Connected to database")

        except Exception as error:
            logging.error(f"[DB] Failed to connect to database", exc_info=error)
            exit()
        
        # Executing the schema.sql to make sure all tables exist
        
        with open("schema.sql", "r") as file:
            schema = file.read()

        await self.pool.execute(schema)  # type: ignore

        file.close()

        # Initializing other essential clients

        self.session = aiohttp.ClientSession()
        self.mystbin = mystbin_library.Client(session=self.session)
        self.uptime: datetime = discord.utils.utcnow()

        # Loading extensions

        for extension in self.config.EXTENSIONS:
            try:
                await self.load_extension(extension)
                logging.info(f"[EXT] Loaded {extension}")

            except Exception as error:
                logging.error(f"[EXT] Failed to load {extension}", exc_info=error)

    async def shorten_text(self, text: str, length: int | None = None, code: int | None = None, link: bool = False):
        """ A function to shorten text
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

    def yes_no(self, bool: bool):
        """ Returns yes if the value is True and no if the value is False """
        if bool:
            return "Yes"
        
        return "No"

    @discord.utils.copy_doc(yes_no)
    def yn(self, bool: bool):
        return self.yes_no(bool)