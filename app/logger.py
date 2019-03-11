import logging
from logging.config import dictConfig

logging_config = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'basic': {'format': '%(asctime)s %(levelname)s %(name)s %(message)s'},
        'color': {
            '()': 'colorlog.ColoredFormatter',
            'format': '%(log_color)s%(levelname)-4s %(asctime)-4s %(name)s %(message)s',
            'log_colors': {
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            },
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'color',
        }
    },
    'root': {'handlers': ['console'], 'level': logging.INFO},
}
dictConfig(logging_config)
logger = logging.getLogger()
