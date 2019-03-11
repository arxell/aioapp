import aioredis
from aiohttp_sse import sse_response

from app import settings
from app.logger import logger


async def handler(request):
    """
    Subscribe on server side events handler
    """
    logger.info('subscribe called')
    _id = request.rel_url.query.get('id')

    redis = await aioredis.create_redis(
        'redis://{}:{}'.format(settings.REDIS_HOST, settings.REDIS_PORT)
    )
    channel = await redis.subscribe(
        settings.REDIS_SUBSCRIBER_CHANNEL.format(_id)
    )
    if channel:
        channel = channel[0]

    # TODO (anton.ogorodnikov):
    # 1) Auth! Need to think about authorization step&
    # 2) duplicate connection error

    async with sse_response(request) as response:
        logger.info('{} subscribe'.format(_id))
        request.app['channels'][_id] = channel
        try:
            while not response.task.done():
                while await channel.wait_message():
                    msg = await channel.get(encoding='utf-8')
                    logger.info('{} got wait_message {}'.format(_id, msg))
                    await response.send(msg)
        finally:
            logger.info('{} unsubscribe'.format(_id))
            redis.close()
            del request.app['channels'][_id]
    return response
