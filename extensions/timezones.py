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


from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands

from utils import Interaction
from dateutil.zoneinfo import get_zonefile_instance

timezone_choices = []
valid_timezones: set[str] = set(get_zonefile_instance().zones)

for valid_timezone in valid_timezones:
    timezone_choices.append(Choice(name=str(valid_timezone), value=str(valid_timezone)))

class Timezones(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    group = app_commands.Group(name="timezone", description="Everything related to timezones")
            
    @group.command(description="Sets your timezone.")
    @app_commands.describe(timezone="Your timezone.")
    async def set(self, interaction: Interaction, timezone: str):
        await interaction.response.send_message(f"Timezone: {timezone}")

    @set.autocomplete("timezone")
    async def autocomplete_callback(self, interaction: Interaction, current: str):
        return timezone_choices


async def setup(bot):
    await bot.add_cog(Timezones(bot))
    