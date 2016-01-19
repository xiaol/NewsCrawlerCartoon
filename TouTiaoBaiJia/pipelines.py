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

from TouTiaoBaiJia.items import CommentsItem
from TouTiaoBaiJia.items import ComicsList, ChaptersItem
from TouTiaoBaiJia.constants import STATIC_HIT, HIT
from TouTiaoBaiJia.constants import COMIC_URLS_QUEUE
from TouTiaoBaiJia.constants import CHAPTER_URLS_QUEUE
from TouTiaoBaiJia.constants import COMMENT_URLS_QUEUE
from TouTiaoBaiJia.constants import STATUS
from TouTiaoBaiJia.constants import CHAPTER_STORE_URL, COMMENT_STORE_URL
from TouTiaoBaiJia.url_factory import g_start_url
from TouTiaoBaiJia.url_factory import g_comment_url
from TouTiaoBaiJia.utils import append_start_url
from utils import rds
# from settings import REDIS_HOST, REDIS_PORT, REDIS_DB, REDIS_PASSWORD

_logger = logging.getLogger(__name__)


class StorePipeline(object):

    def __init__(self):
        self.r = rds
        self.day = 60*60*24

    def process_item(self, item, spider):
        if isinstance(item, ComicsList):
            self.process_comics_list(item)
        elif isinstance(item, ChaptersItem):
            self.process_chapters_item(item)
        elif isinstance(item, CommentsItem):
            self.process_comments_item(item)
        else:
            pass

    def process_comics_list(self, item):
        total_page = item["total_page"]
        current_page = item["current_page"]
        group = item["group"]
        status = item["status"]
        comics = item["comics"]
        pub_status = 1 if status == STATUS["complete"] else 0
        has_next_page = False
        for comic in comics:
            comic["pub_status"] = pub_status
            has_next_page = self.process_comics_item(comic)
        # if has_next_page and current_page <= total_page:
        #     url = g_start_url(status, group, current_page+1)
        #     append_start_url(url, COMIC_URLS_QUEUE)

    def process_comics_item(self, item):
        """ store comic info in cache, then start crawl comics detail,comments """
        comic = dict(item)
        url = comic["comic_url"]
        status = self.r.hget(url, "pub_status")
        if status == "1":   # complete crawled
            _logger.info("name: %s already crawled" % comic["name"])
            return False
        elif status == "0":     # todo: incomplete crawled
            _logger.info("name: %s incomplete crawled" % comic["name"])
            return True
        # if not crawled
        p_url = STATIC_HIT if item["mobile"] else HIT
        p_url = p_url % item["comic_id"]
        try:
            response = requests.get(p_url)  # get popularity
            comic["popularity"] = json.loads(response.content)["hot_hits"]
        except:
            _logger.warn("get popularity for %s failed" % comic["comic_url"])
        _logger.info("name: %s, url: %s" % (comic["name"], url))
        self.r.hmset(url, comic)
        self.r.expire(url, self.day*7)
        append_start_url(url, CHAPTER_URLS_QUEUE)   # crawl chapters
        append_start_url(g_comment_url(comic["comic_id"]),
                         COMMENT_URLS_QUEUE)    # crawl comments
        return True

    def process_chapters_item(self, item):
        """ store chapter info in cache """
        chapter = dict(item)
        if not self.r.exists(chapter["comic_url"]):
            raise DropItem("comic url changed")
        comic = self.r.hgetall(chapter["comic_url"])
        key = "||".join([chapter["comic_url"], chapter["chapter_url"]])
        key = base64.encodestring(key).replace("=", "")
        for k, v in comic.iteritems():
            chapter[k] = v
        self.r.hmset(key, chapter)
        self.r.expire(key, self.day*7)
        try:
            r = requests.get(url=CHAPTER_STORE_URL+key)
            if r.status_code != 200:
                _logger.error("code: %s, key: %s" % (r.status_code, key))
            else:
                _logger.debug("store chapter: %s" % chapter["chapter_name"])
        except:
            _logger.error("store chapter exception: %s" % key)

    def process_comments_item(self, item):
        if not item["content"].strip() or not item["nickname"].strip():
            raise DropItem("empty comment content or nickname")
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
        try:
            r = requests.post(url=COMMENT_STORE_URL, json=comment)
            if r.status_code != 200:
                _logger.error("code: %s, %s" % (r.status_code, item["nickname"]))
            else:
                _logger.info("insert comment: %s" % item["nickname"])
        except:
            _logger.error("store comment exception")




