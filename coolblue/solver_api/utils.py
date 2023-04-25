
import math
import redis
from django.conf import settings


def get_redis():
    """ Returns Redis connection """
    return redis.Redis(
        host=settings.REDIS_HOST, port=settings.REDIS_PORT, decode_responses=True
    )

def calculate_distance(point1, point2):
    """Returns Eucledian distance"""
    return math.dist((
        point1["lat"], point1["lon"]), (point2["lat"], point2["lon"])
        )
