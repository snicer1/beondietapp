import os

from aiohttp import web
from tartiflette_aiohttp import register_graphql_handlers
import asyncio

app = web.Application()


def run() -> None:
    """
    Entry point of the application.
    """
    web.run_app(
        register_graphql_handlers(
            app=app,
            engine_sdl=os.path.dirname(os.path.abspath(__file__)) + "/sdl",
            engine_modules=[
                "beondiet.query_resolvers",
                "beondiet.mutation_resolvers",
                "beondiet.subscription_resolvers",
                "beondiet.directives.rate_limiting",
                "beondiet.directives.auth",
            ],
            executor_http_endpoint="/graphql",
            executor_http_methods=["POST"],
            graphiql_enabled=True,
        )
    )


@asyncio.coroutine
async def hello(request):
    return web.Response(text="Test application on 0.0.0.0/graphiql")


app.add_routes([web.get('/', hello)])

# query_resolvers.resolve_query_hello()

# from db import db_conn
# from beondiet import views
