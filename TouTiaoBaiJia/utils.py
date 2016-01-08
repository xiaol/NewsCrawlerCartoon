import redis

from TouTiaoBaiJia.settings import REDIS_HOST
from TouTiaoBaiJia.settings import REDIS_PORT, REDIS_DB, REDIS_PASSWORD


rds = redis.Redis(host=REDIS_HOST,
                  port=REDIS_PORT,
                  db=REDIS_DB,
                  password=REDIS_PASSWORD
                  )


def append_start_url(url, queue_name):
    rds.lpush(queue_name, url)




