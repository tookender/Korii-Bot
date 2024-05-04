from aiohttp.web_routedef import route
from bot import Korii
from utils import Cog
from aiohttp import web
from aiohttp.web import Response, json_response


class IPC(Cog):
    def __init__(self, bot: Korii):
        self.bot = bot
        app = web.Application()
        self.app = app
        self.router = app.router
        self.router.add_route("get", "/", self.ping)
        self.bot.loop.create_task(self._start())

    async def ping(self, _) -> Response:
        return json_response({"message": f"PONG! {self.bot.latency * 1000}"})

    async def _start(self):
        await self.bot.wait_until_ready()
        await web._run_app(self.app, host="0.0.0.0", port=6969, print=None)


async def setup(bot):
    await bot.add_cog(IPC(bot))
