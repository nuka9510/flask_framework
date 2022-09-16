import os, logging
from application.config import log

logger = logging.getLogger(__name__)

if not os.path.exists(log['LOG_PATH']):
    os.makedirs(log['LOG_PATH'])

file_handler = logging.FileHandler(filename=os.path.join(log['LOG_PATH'], log['LOG_NAME']))

file_handler.setFormatter(log['LOG_FORMAT'])
logger.setLevel(log['LOG_LEVEL'])
logger.addHandler(file_handler)