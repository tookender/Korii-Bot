from collections import defaultdict
from typing import Any, DefaultDict

import asyncpg
from discord.ext import tasks


__all__: tuple[str, ...] = ("LevellingCacheManager",)


class LevellingCacheManager:
    def __init__(self, pool: asyncpg.Pool) -> None:
        self.levels: DefaultDict[int, DefaultDict[int, int]] = defaultdict(lambda: defaultdict())
        self.disabled: list[int] = []
        self.pool: asyncpg.Pool = pool
        # Dict[GuildID, Dict[UserID, XP]] 

    async def update_all(self):
        queries: list[tuple[Any, ...]] = []
        
        for guild_id, levels in self.levels.items():
            for user_id, xp in levels.items():
                queries.append((guild_id, user_id, xp))
        
        query = """
            INSERT INTO levels (guild_id, user_id, xp) VALUES ($1, $2, $3)
            ON CONFLICT (guild_id, user_id) DO UPDATE SET xp = levels.xp + excluded.xp
        """
        await self.pool.executemany(query, queries)

    @tasks.loop(minutes=5)
    async def update_database(self):
        await self.update_all()

    async def __aenter__(self):
        self.update_database.start()
        return self
    
    async def __aexit__(self, *_: Any):
        await self.update_all()
        self.update_database.cancel()