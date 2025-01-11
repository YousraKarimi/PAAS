import redis

from applogger import logger
from notificationmanager.models import RedisParams


def write_to_redis(params : RedisParams, key : str, value : str):
    try:
        r = redis.Redis(host=params.host, port=params.port, db=0)
        r.set(key, value)
        logger.info(f"Successfully set {key} to {value} in Redis.")
    except Exception as e:
        logger.error(f"Failed to write to Redis: {e}")