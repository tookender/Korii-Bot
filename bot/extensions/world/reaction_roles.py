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

from typing import List, Set, Any

import discord
from discord.ext import commands

from bot import Embed
            

class RoleSelector(discord.ui.Select[discord.ui.View]):
    def __init__(self, available_roles: List[discord.Role], thing: str, max_valuess: int):
        options = [discord.SelectOption(label=role.name, value=str(role.id)) for role in available_roles]

        super().__init__(
            placeholder=f"Choose your {thing}...", min_values=0, max_values=len(available_roles), options=options
        )

    async def callback(self, interaction: discord.Interaction):
        if not interaction.guild or isinstance(interaction.user, discord.User):
            return

        def _id_getter(option: discord.SelectOption) -> int:
            role_id = option.value
            print(f'returning role: {role_id}')
            return int(role_id)

        role_ids = list(map(_id_getter, self.options))
        role_ids_to_add = list(map(int, self.values))

        user_roles: List[discord.Role] = [role for role in interaction.user.roles if role.id not in role_ids]

        roles_to_keep: Set[discord.Role | Any] = {interaction.guild.get_role(role_id) for role_id in role_ids_to_add}
        roles_to_keep.discard(None)

        try:
            user_roles.extend(roles_to_keep)
            await interaction.user.edit(roles=user_roles)

            role_names = "\n` + `".join([role.name for role in roles_to_keep])

            if interaction.message:
                embed = interaction.message.embeds[0]
                embed = embed.copy()
                embed.description = f"` + ` {role_names}"
                return await interaction.response.edit_message(embed=embed, view=None)

        except discord.HTTPException as e:
            await interaction.response.send_message(str(e), ephemeral=True)


class PronounsView(discord.ui.View):
    def __init__(self, roles: List[discord.Role]):
        super().__init__()
        self.add_item(RoleSelector(roles, "pronouns", 1))


class ContinentsView(discord.ui.View):
    def __init__(self, roles: List[discord.Role]):
        super().__init__()
        self.add_item(RoleSelector(roles, "continent", 1))


class PlatformsView(discord.ui.View):
    def __init__(self, roles: List[discord.Role]):
        super().__init__()
        self.add_item(RoleSelector(roles, "platforms", 3))


class PingsView(discord.ui.View):
    def __init__(self, roles: List[discord.Role]):
        super().__init__()
        self.add_item(RoleSelector(roles, "pings", len(roles)))


class ReactionRoleView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=360)
    
    @discord.ui.button(label="Pronouns", emoji="🎭", style=discord.ButtonStyle.blurple)
    async def pronouns(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not interaction.guild:
            return

        role_ids = [1069280060659486742, 1069280196160671765, 1069280245770887348, 1069280277383352360, 1069280309570449479]
        roles: List[discord.Role | Any] = [interaction.guild.get_role(role) for role in role_ids]

        embed = Embed(title="🎭 Select your pronouns!")

        return await interaction.response.send_message(embed=embed, view=PronounsView(roles), ephemeral=True)

    @discord.ui.button(label="Continents", emoji="🌍", style=discord.ButtonStyle.blurple)
    async def continents(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not interaction.guild:
            return

        role_ids = [1069280591142465638, 1069280657974501396, 1069280470858219561, 1069280630929637486, 1069280543851675709, 1069280570875580466]
        roles: List[discord.Role | Any] = [interaction.guild.get_role(role) for role in role_ids]

        embed = Embed(title="🌍 Select your continents!")

        return await interaction.response.send_message(embed=embed, view=PronounsView(roles), ephemeral=True)

    @discord.ui.button(label="Platforms", emoji="🎮", style=discord.ButtonStyle.blurple)
    async def platforms(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not interaction.guild:
            return

        role_ids = [1069280895627964416, 1069280851608735785, 1069280927521460234]
        roles: List[discord.Role | Any] = [interaction.guild.get_role(role) for role in role_ids]

        embed = Embed(title="🎮 Select your platforms!")

        return await interaction.response.send_message(embed=embed, view=PronounsView(roles), ephemeral=True)

    @discord.ui.button(label="Pings", emoji="🏓", style=discord.ButtonStyle.blurple)
    async def pings(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not interaction.guild:
            return

        role_ids = [1069281116651008000, 1069281033809309767, 1069281133805711401, 1069281155297325249]
        roles: List[discord.Role | Any] = [interaction.guild.get_role(role) for role in role_ids]

        embed = Embed(title="🏓 Select your pings!")

        return await interaction.response.send_message(embed=embed, view=PronounsView(roles), ephemeral=True)