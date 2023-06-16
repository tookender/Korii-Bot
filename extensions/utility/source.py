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

import inspect
import os
from typing import Optional

from discord import app_commands
from discord.ext import commands

from bot import Korii
from utils import Embed, Interaction


class SourceCog(commands.Cog):
    def __init__(self, bot: Korii):
        self.bot: Korii = bot

    @app_commands.command(description="Get the source code of a command or the bot.")
    @app_commands.checks.cooldown(1, 5)
    async def source(self, interaction: Interaction, command: Optional[str] = None):
        url = "https://github.com/Korino-Development/Korii-Bot"

        if not command:
            embed = Embed(
                title="Here is my source code.",
                url=url,
                description="This source code is licensed under the **[`AGPLv3`](https://www.gnu.org/licenses/agpl-3.0.de.html) license**.\n"
                "Read more in the **[`README.md`](https://github.com/Korino-Development/Korii-Bot/README.md)**",
            )

            return await interaction.response.send_message(embed=embed)

        object = self.bot.tree.get_command(command)

        if not object:
            embed = Embed(
                title="Here is my source code.",
                url=url,
                description="This source code is licensed under the **[`AGPLv3`](https://www.gnu.org/licenses/agpl-3.0.de.html) license**.\n"
                "Read more in the **[`README.md`](https://github.com/Korino-Development/Korii-Bot/README.md)**",
            )
            embed.set_author(name="Invalid command.")

            return await interaction.response.send_message(embed=embed)

        source = object.callback.__code__
        module = object.callback.__module__
        filename = source.co_filename

        lines, first_line_number = inspect.getsourcelines(source)
        if not module.startswith("discord"):
            if filename is None:
                embed = Embed(
                    title="Here is my source code.",
                    url=url,
                    description="This source code is licensed under the **[`AGPLv3`](https://www.gnu.org/licenses/agpl-3.0.de.html) license**.\n"
                    "Read more in the **[`README.md`](https://github.com/Korino-Development/Korii-Bot/README.md)**",
                )
                embed.set_author(name="Invalid command.")

                return await interaction.response.send_message(embed=embed)

            location = os.path.relpath(filename).replace("\\", "/")

        else:
            location = module.replace(".", "/") + ".py"
            url = "https://github.com/Rapptz/discord.py"

        final_url = f"{url}/blob/master/{location}#L{first_line_number}-L{first_line_number + len(lines) - 1}"
        embed = Embed(
            title=f"Here is {command}.",
            url=final_url,
            description="This source code is licensed under the **[`AGPLv3`](https://www.gnu.org/licenses/agpl-3.0.de.html) license**.\n"
            "Read more in the **[`README.md`](https://github.com/Korino-Development/Korii-Bot/README.md)**.",
        )

        return await interaction.response.send_message(embed=embed)
