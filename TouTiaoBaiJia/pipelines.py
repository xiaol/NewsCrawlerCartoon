# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import logging
import base64
import redis
import requests

from TouTiaoBaiJia.items import ComicsItem, CommentsItem
from settings import REDIS_HOST, REDIS_PORT, REDIS_DB, REDIS_PASSWORD

_logger = logging.getLogger(__name__)


class DebugPipeline(object):

    def __int__(self):
        pass

    def process_item(self, item, spider):
        if isinstance(item, ComicsItem):
            print item
        elif isinstance(item, CommentsItem):
            print item
        else:
            pass


class RedisPipeline(object):

    comic_url = "http://api.deeporiginalx.com/bdp/spider/pipeline/comic/"

    def __init__(self):
        host = REDIS_HOST
        port = REDIS_PORT
        db = REDIS_DB
        password = REDIS_PASSWORD
        self.r = redis.Redis(host=host, port=port, db=db, password=password)

    def process_item(self, item, spider):
        dict_item = dict(item)
        chapter = dict_item["chapter"]
        del dict_item["comic_id"]
        del dict_item["chapter"]
        for key, value in chapter.iteritems():
            dict_item[key] = value
        dict_item["tags"] = json.dumps(dict_item["tags"])
        dict_item["images"] = json.dumps(dict_item["images"])
        key = "||".join([dict_item["comic_url"], chapter["chapter_url"]])
        redis_name = base64.encodestring(key).replace('=', '')
        redis_value = dict_item
        self.r.hmset(redis_name, redis_value)
        self.r.expire(redis_name, 7*24*60*60)
        r = requests.get(url=self.comic_url+redis_name)
        if r.status_code != 200:
            _logger.error("code: %s, key: %, conent: %s" % (r.status_code, redis_name, str(r.content)))
        else:
            _logger.info(redis_name)
