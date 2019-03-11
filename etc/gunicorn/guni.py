import os

bind = '127.0.0.1:8001'
accesslog = errorlog = '-'
loglevel = 'info'
timeout = 180
graceful_timeout = 180
worker_class = 'aiohttp.worker.GunicornWebWorker'
workers = os.environ.get('GUNI_WORKERS', 1)
max_requests = os.environ.get('GUNI_WORKERS_MAX_REQUESTS_ADMIN', 100)
max_requests_jitter = os.environ.get(
    'GUNI_WORKERS_MAX_REQUESTS_JITTER_ADMIN', 10
)
