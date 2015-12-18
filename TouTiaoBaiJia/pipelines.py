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

    from settings import POSTGRES
    from sqlalchemy.ext.automap import automap_base
    from sqlalchemy.orm import Session
    from sqlalchemy import create_engine
    Base = automap_base()
    engine = create_engine(POSTGRES)
    Base.prepare(engine, reflect=True)
    Comics = Base.classes.comics
    Chapters = Base.classes.chapters
    Comments = Base.classes.comments
    session = Session(engine)

    def __init__(self):
        self.comics_urls = set(self.session.query(self.Comics.comic_url).all())

    def process_item(self, item, spider):
        if isinstance(item, ComicsItem):
            self.store_chapters(item)
        elif isinstance(item, CommentsItem):
            self.store_comments(item)
        else:
            _logger.error("not support this item %s" % type(item))

    def store_chapters(self, item):
        comic = dict(item)
        chapter = comic["chapter"]
        if comic["comic_url"] not in self.comics_urls:
            self.comics_urls.add(comic["comic_url"])
            del comic["chapter"]
            self.session.add(self.Comics(**comic))
            self.session.commit()
            _logger.info("insert comic %s" % comic["name"])
        self.session.add(self.Chapters(**chapter))
        self.session.commit()
        _logger.info("insert chapter %s %s" % (comic["name"], chapter["name"]))

    def store_comments(self, item):
        comment = dict(item)
        self.session.add(self.Comments(**comment))
        self.session.commit()
        _logger.info("insert comment %s" % comment["nickname"])


class RedisPipeline(object):

    comic_url = "http://api.deeporiginalx.com/bdp/spider/pipeline/comic/"
    comment_url = "http://api.deeporiginalx.com/bdp/comic/comment"

    def __init__(self):
        host = REDIS_HOST
        port = REDIS_PORT
        db = REDIS_DB
        password = REDIS_PASSWORD
        self.r = redis.Redis(host=host, port=port, db=db, password=password)

    def process_item(self, item, spider):
        if isinstance(item, ComicsItem):
            self.store_chapters(item)
        elif isinstance(item, CommentsItem):
            self.store_comments(item)
        else:
            _logger.error("not support this item" % type(item))

    def store_chapters(self, item):
        dict_item = dict(item)
        chapter = dict_item["chapter"]
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
            _logger.error("code: %s, key: %" % (r.status_code, redis_name))
        else:
            _logger.info(redis_name)

    def store_comments(self, item):
        comment = dict()
        comment["comicUrl"] = item["comic_url"]
        comment["commentId"] = item["comment_id"]
        comment["uid"] = item["uid"]
        comment["nickName"] = item["nickname"]
        comment["avatarUrl"] = item["avatar_url"]
        comment["pid"] = item["pid"]
        comment["comicId"] = item["comic_id"]
        comment["authorId"] = item["author_id"]
        comment["author"] = item["author"]
        comment["content"] = item["content"]
        comment["createTime"] = item["createtime"]
        comment["countReply"] = item["count_reply"]
        comment["up"] = item["up"]
        comment["source"] = item["source"]
        comment["place"] = item["place"]
        comment["ip"] = item["ip"]
        comment["sourceName"] = item["source_name"]
        r = requests.post(url=self.comment_url, json=comment)
        if r.status_code != 200:
            _logger.error("code: %s, %s" % (r.status_code, item["nickname"]))
        else:
            _logger.info("insert comment: %s" % item["nickname"])
