import asyncio

from app.core import get_app

loop = asyncio.get_event_loop()
app = loop.run_until_complete(get_app())
