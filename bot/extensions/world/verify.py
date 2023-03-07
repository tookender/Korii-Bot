"""
Korii Bot: A multipurpose bot with swag 😎
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

import discord
from discord.ext import commands
from multicolorcaptcha import CaptchaGenerator

from bot import Embed, Korii


class AnswerModal(discord.ui.Modal, title="🤖 Human Verification"):
    def __init__(self, answer: str):
        super().__init__(timeout=360)
        self.answer = answer
    
    code = discord.ui.TextInput(
        label="Code",
        placeholder="The code here...",
        min_length=4,
        max_length=4,
        required=True,
        style=discord.TextStyle.paragraph,
    )

    async def on_submit(self, interaction: discord.Interaction):
        if not interaction.guild or isinstance(interaction.user, discord.User):
            return

        if self.answer == self.code.value:
            role = interaction.guild.get_role(1063913058558296134)

            if not role:
                return

            await interaction.user.add_roles(role)
            return await interaction.response.edit_message(content="✅ | You have been verified! Go check out <#1069276775055638548>.", view=None, attachments=[])
        
        return await interaction.response.edit_message(content="❌ | Wrong! Try again.", view=None, attachments=[])


    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        return
        

class AnswerView(discord.ui.View):
    def __init__(self, answer: str):
        super().__init__(timeout=360)
        self.answer = answer
    
    async def on_timeout(self, interaction: discord.Interaction):
        for child in self.children:
            if isinstance(child, discord.ui.Button):
                child.disabled = True
        
        return await interaction.response.edit_message(view=self)

    @discord.ui.button(emoji="❓", label="Answer", style=discord.ButtonStyle.green)
    async def answer_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        return await interaction.response.send_modal(AnswerModal(self.answer))


class VerifyView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(emoji="🤖", label="Verify", style=discord.ButtonStyle.green, custom_id="world:verify")
    async def verify(self, interaction: discord.Interaction, button: discord.ui.Button):
        captcha = CaptchaGenerator(6).gen_captcha_image(chars_mode="ascii")
        image = captcha.image
        answer = captcha.characters

        image.save("bot/assets/captcha.png", "png")

        return await interaction.response.send_message(
            file=discord.File("bot/assets/captcha.png", filename="captcha.png", description="Captcha image."),
            ephemeral=True,
            view=AnswerView(answer=answer),
        )


class VerifyCog(commands.Cog):
    def __init__(self, bot: Korii):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def verify(self, ctx: commands.Context):
        if not ctx.message.reference:
            return await ctx.send("No reply.")
        
        message = ctx.message.reference.resolved

        if not isinstance(message, discord.Message):
            return await ctx.send("Invalid reply.")

        embed = Embed(
            title="🤖 Human verification",
            description="Click the **✅ Verify** button below and solve the captcha to verify.",
            color=0x10b981)
        
        return await message.edit(content=None, embed=embed, view=VerifyView())