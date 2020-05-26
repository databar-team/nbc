import logging
from logging.config import dictConfig
from config.logger import LOGGING_CONFIG


dictConfig(LOGGING_CONFIG)

logger = logging.getLogger(__name__)