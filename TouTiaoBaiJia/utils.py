import redis


rds = redis.Redis()


def append_start_url(url, queue_name):
    rds.lpush(queue_name, url)




