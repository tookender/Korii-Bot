from dataclasses import dataclass


@dataclass
class Configuration:
    BOT_TOKEN: str
    POSTGRESQL: str
    