import json
import logging

import aiohttp
from aiohttp import web

logger = logging.getLogger(__name__)


async def handler(request):
    """
    Handle WebSocket connections
    """
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    ws['user_id'] = request['user_id']
    request.app['websockets'].append(ws)
    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            data = None
            try:
                data = json.loads(msg.data)
            except Exception:
                pass
            if msg.data == 'close':
                await ws.close()
            elif data:
                await ws.send_str(data.get('message', 'no message'))
        elif msg.type == aiohttp.WSMsgType.ERROR:
            logger.info(f'ws connection closed with exception {ws.exception()}')
    logger.info('websocket connection closed')
    return ws
