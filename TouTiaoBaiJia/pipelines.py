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
from scrapy.exceptions import DropItem
from TouTiaoBaiJia.items import ComicsItem, ChaptersItem

_logger = logging.getLogger(__name__)

class DebugPipeline(object):

    def __init__(self):
        self.comics = {u"少年漫画": set(),
                       u"少女漫画": set(),
                       u"青年漫画": set()}

    def process_item(self, item, spider):
        if isinstance(item, ComicsItem):
            cate = item["category"]
            if cate in self.comics:
                if item["name"] in self.comics[cate]:
                    raise DropItem()
                else:
                    self.comics[cate].add(item["name"])
            else:
                print("#" * 30 + cate + "#" * 30)
                raise DropItem()
            # print("\t".join(["%s: %s" % (k, len(v)) for k, v in self.comics.iteritems()]))
            print(item["comic_url"])
            print(", ".join([url.split("/")[-1] for url in item["chapter_urls"]]))
            return item
        elif isinstance(item, ChaptersItem):
            # print("\t".join([str(item["comic_id"]), str(item["id"]), item["name"]]))
            # print(",".join([img.split("/")[-1] for img in item["images"]]))
            return
        else:
            raise DropItem()


class RedisPipeline(object):

    def __init__(self):
        HOST = "ccd827d637514872.m.cnhza.kvstore.aliyuncs.com"
        PORT = 6379
        DB = 0
        PASSWORD = "ccd827d637514872:LYcache2015"
        self.r = redis.Redis(host=HOST, port=PORT, db=DB, password=PASSWORD)

    def process_item(self, item, spider):
        dict_item = dict(item)
        chapter = dict_item["chapter"]
        del dict_item["chapter"]
        for key, value in chapter.iteritems():
            dict_item[key] = value
        print dict_item
        dict_item["tags"] = json.dumps(dict_item["tags"])
        dict_item["images"] = json.dumps(dict_item["images"])
        key = "||".join([dict_item["comic_url"], chapter["chapter_url"]])
        redis_name = base64.encodestring(key).replace('=', '')
        redis_value = dict_item
        self.r.hmset(redis_name, redis_value)
        self.r.expire(redis_name, 10*60)
        url = "http://api.deeporiginalx.com/bdp/spider/pipeline/comic/" + redis_name
        r = requests.get(url=url)
        if r.status_code != 200:
            _logger.error("code: %s, key: %s" % (r.status_code, redis_name))
        _logger.info(redis_name)
