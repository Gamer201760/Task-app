import os
level = os.getenv('LOG_LEVEL', 'INFO')

LOG_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'root': {
        'handlers': ['async_handler', ],
        'level': level,
        'propagate': False,
    },
    'formatters': {
        'json': {
            '()': 'lib.log.utils.JSONLogFormatter',
        }
    },
    'handlers': {
        'async_handler': {
            'level': level,
            'formatter': 'json',
            'class': 'asynclog.AsyncLogDispatcher',
            'func': 'lib.log.utils.write_log',
        },
    },
    'loggers': {
        'uvicorn': {
            'handlers': ['async_handler', ],
            'level': 'INFO',
            'propagate': False,
        },
        'uvicorn.access': {
            'handlers': ['async_handler', ],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}
