from .join_leave import JoinLeaveLogs
from .member import MemberLogs
from .message import MessageLogs
from .server import ServerLogs
from .voice import VoiceLogs


class Logging(JoinLeaveLogs, MemberLogs, MessageLogs, ServerLogs, VoiceLogs):
    pass


async def setup(bot):
    await bot.add_cog(Logging(bot))
