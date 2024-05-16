from typing import TypeAlias

from bot import Korii

from .bases import *
from .constants import *
from .utils import *

Interaction: TypeAlias = discord.Interaction[Korii]


class Invalid(Exception):
    ...


class BlacklistedError(Exception):
    ...
