import asyncio
import logging

from aiojobs.aiohttp import spawn

from .index import get_response

logger = logging.getLogger(__name__)


async def coro():
    logger.info(f'coro start')
    await asyncio.sleep(2)
    logger.info(f'coro end')


async def view(request):
    await spawn(request, coro())
    return get_response()
