from bot import Korii
from utils import Cog
from aiohttp import web
from aiohttp.web import Response, json_response


class IPC(Cog):
    def __init__(self, bot: Korii):
        app = web.Application()
        self.app = app
        app.add_routes(routes)
        self.bot.loop.create_task(self._start())

    async def _start(self):
        await self.bot.wait_until_ready()
        await web._run_app(self.app, port=6969, print=None)


routes = web.RouteTableDef()


@routes.get("/")
async def ping(_) -> Response:
    return json_response({"message": f"PONG! {IPC.bot.latency * 1000}"})
