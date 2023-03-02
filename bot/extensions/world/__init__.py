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

from .faq import FAQCog, FAQView
from .verify import VerifyCog, VerifyView
from .welcome import WelcomeCog, WelcomeView


class World(FAQCog, VerifyCog, WelcomeCog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.add_view(FAQView())
        self.bot.add_view(VerifyView())
        self.bot.add_view(WelcomeView())
        
    pass


async def setup(bot):
    await bot.add_cog(World(bot))
