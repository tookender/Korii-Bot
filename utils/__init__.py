from typing import TypeAlias

from bot import Korii

from .bases import *
from .utils import *
from .constants import *

Interaction: TypeAlias = discord.Interaction[Korii]


class Invalid(Exception):
    ...


class BlacklistedError(Exception):
    ...
