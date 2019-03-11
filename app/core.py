import asyncio
import json

import aiohttp
import aioredis
from aiojobs.aiohttp import setup

from app import settings
from app.logger import logger
from app.middlewares import authentication_handler
from app.routes import setup_routes
from app.settings import REDIS_NOTIFICATIONS_QUEUE


async def close_redis(app):
    """
    Close redis connection on shutdown
    """
    logger.info('close_redis called')
    await app['redis'].close()


async def close_all_ws_connections(app):
    """
    Close all ws connections on shutdown
    """
    logger.info('close_all_connections called')
    for ws in app['websockets']:
        await ws.close(code=1001, message='Server shutdown')


async def cleanup_background_tasks(app):
    logger.info('cleanup_background_tasks called')
    app['redis_listener'].cancel()
    await app['redis_listener']


async def listen_to_redis(app):
    try:
        sub = await aioredis.create_redis(
            f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}',
            loop=app.loop,
        )
        ch, *_ = await sub.subscribe(REDIS_NOTIFICATIONS_QUEUE)
        while True:
            try:
                while await ch.wait_message():
                    msg = await ch.get(encoding='utf-8')
                    logger.info(f'got message: {msg}')
                    data = json.loads(msg)
                    for ws in app['websockets']:
                        if ws['user_id'] == data['user_id']:
                            txt = data['text']
                            logger.info(f'sending {txt} to {ws}')
                            await ws.send_str(txt)
            except Exception as e:
                logger.error(str(e))
                continue
    except asyncio.CancelledError:
        pass
    finally:
        await sub.unsubscribe(ch.name)
        await sub.quit()


async def start_background_tasks(app):
    app['redis_listener'] = app.loop.create_task(listen_to_redis(app))


async def get_app():
    """
    Create and configure our app
    """
    logger.info('get_app called')
    app = aiohttp.web.Application(middlewares=[authentication_handler])

    app['channels'] = {}
    app['websockets'] = []
    logger.info(f'REDIS: {settings.REDIS_HOST}/{settings.REDIS_PORT}')
    app['redis'] = await aioredis.create_redis(
        f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}'
    )

    # infrastructure
    app.on_startup.append(start_background_tasks)

    app.on_cleanup.append(close_redis)
    app.on_cleanup.append(close_all_ws_connections)
    app.on_cleanup.append(cleanup_background_tasks)

    # routing
    setup_routes(app)
    setup(app)
    return app
