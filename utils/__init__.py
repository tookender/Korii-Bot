from typing import TYPE_CHECKING, TypeAlias

if TYPE_CHECKING:
    from bot import Korii
else:
    from discord.ext.commands import bot as Korii

from .bases import *
from .constants import *
from .utils import *

Interaction: TypeAlias = discord.Interaction[Korii]


class Invalid(Exception): ...


class BlacklistedError(Exception): ...
