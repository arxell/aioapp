from aiohttp import web

from app.logger import logger


async def handler(request):
    """
    Show active connections
    """
    logger.info('show_handler called')

    result = {'status': 'ok', 'data': [*request.app['channels'].keys()]}
    return web.Response(text=result)
