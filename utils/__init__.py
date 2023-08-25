from typing import TypeAlias

from bot import Korii

from .subclasses.embed import *

Interaction: TypeAlias = discord.Interaction[Korii]
