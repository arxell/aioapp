import os

HOST = os.getenv('HOST', '0.0.0.0')
REDIS_HOST = os.getenv('REDIS_GLOBAL_HOST', 'localhost')
REDIS_PORT = os.getenv('REDIS_GLOBAL_PORT', '6379')
REDIS_SUBSCRIBER_CHANNEL = os.getenv(
    'REDIS_SUBSCRIBER_CHANNEL', 'subscriber:{}'
)
REDIS_NOTIFICATIONS_QUEUE = 'notifications'
PORT = int(os.getenv('PORT', 8080))
