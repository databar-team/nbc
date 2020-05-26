import os


LOG_FORMAT = '[%(asctime)s] %(levelname)-8s in %(module)s:%(lineno)d: %(message)s'

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': LOG_FORMAT
        },
    },
    'handlers': {
        'default': {
            'level': os.getenv('LOG_LEVEL', 'INFO'),
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',  # Default is stderr
        },
    },
    'loggers': {
        '': {  # root logger
            'handlers': ['default'],
            'level': os.getenv('LOG_LEVEL', 'INFO'),
            'propagate': False
        }
    }
}