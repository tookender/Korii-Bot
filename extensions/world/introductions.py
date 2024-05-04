import discord
from discord.ext import commands

from bot import Korii
from utils import Embed, Interaction


class IntroductionsView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Template",
        emoji="📋",
        custom_id="world:view_example",
        style=discord.ButtonStyle.blurple,
    )
    async def template(self, interaction: Interaction, button: discord.ui.Button):
        template = [
            "👋 Hello my name is **[name]**",
            "⏰ I am **[age]** years old.",
            "🌎 I am from **[country]**.",
            "🎮 My hobbies are **[hobbies]**.",
        ]

        embed = Embed(
            title="🎭 Template",
            description="\n".join(template),
        )

        embed.set_footer(text="You can modify this template as much as you like. You also don't have to use it, and you can just make your own.")

        return await interaction.response.send_message(embed=embed, ephemeral=True)


class IntroductionsCog(commands.Cog):
    def __init__(self, bot: Korii):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def introductions(self, ctx: commands.Context):
        if not ctx.message.reference:
            return await ctx.send("No reply.")

        message = ctx.message.reference.resolved

        if not isinstance(message, discord.Message):
            return await ctx.send("Invalid reply.")

        embed = Embed(
            title="🎭 Introductions",
            description="Here you can introduce yourself to the rest of the server.\n"
            "Click the button below for a template you can use, you can also make your own if you wanna get creative.",
            color=0x10B981,
        )

        return await message.edit(content=None, embed=embed, view=IntroductionsView())
