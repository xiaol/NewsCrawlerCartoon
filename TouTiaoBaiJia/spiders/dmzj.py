import json
import logging
from urlparse import urlparse, parse_qs
import scrapy
from scrapy_redis import spiders

from TouTiaoBaiJia.constants import COMIC_SPIDER_NAME
from TouTiaoBaiJia.constants import CHAPTER_SPIDER_NAME
from TouTiaoBaiJia.constants import COMMENT_SPIDER_NAME
from TouTiaoBaiJia.constants import COMMENT_URLS_QUEUE
from TouTiaoBaiJia.extract import parse_meta_info, parse_comic_mobile
from TouTiaoBaiJia.extract import re_load_data
from TouTiaoBaiJia.items import ComicsList, CommentsItem
from TouTiaoBaiJia.utils import rds, append_start_url
from TouTiaoBaiJia.url_factory import g_comment_url

_logger = logging.getLogger(__name__)


class ComicSpider(spiders.RedisSpider):

    name = COMIC_SPIDER_NAME

    def parse(self, response):
        comic_list = ComicsList()
        parse_query = parse_qs(urlparse(response.request.url).query)
        current_page = int(parse_query["p"][0])
        group = parse_query["reader_group"][0]
        status = int(parse_query["status"][0])
        comics, total_page = parse_meta_info(response)
        comic_list["total_page"] = total_page
        comic_list["current_page"] = current_page
        comic_list["group"] = group
        comic_list["status"] = status
        comic_list["comics"] = comics
        yield comic_list


class ChapterSpider(spiders.RedisSpider):

    name = CHAPTER_SPIDER_NAME

    def parse(self, response):
        detail = parse_comic_mobile(response)
        chapters = detail["chapters"]
        detail_dict = dict(detail)
        del detail_dict["chapters"]
        detail_dict["last_chapter_url"] = chapters[0]["chapter_url"]
        if not rds.exists(detail_dict["comic_url"]):
            _logger.error("comic url changed: %s" % detail_dict["comic_url"])
            return
        rds.hmset(detail_dict["comic_url"], detail_dict)    # update comic info
        for chapter in chapters:
            yield scrapy.Request(chapter["chapter_url"],
                                 callback=self.parse_chapter,
                                 meta={"chapter": chapter})

    def parse_chapter(self, response):
        data = re_load_data(response.body_as_unicode(), "init_data")
        if data is None:
            return
        chapter = response.meta["chapter"]
        chapter["images"] = json.dumps(data["page_url"])
        yield chapter


class CommentSpider(spiders.RedisSpider):

    name = COMMENT_SPIDER_NAME

    def parse(self, response):
        data = re_load_data(response.body_as_unicode(), "comment")
        if data is None or data.get("result") != 1000:
            return
        comments = data["data"]
        for comment in comments:
            item = self.build_comment_item(comment)
            yield item
            if item["count_reply"] != 0:
                for d in comment["reply"]["data"]:
                    item = self.build_comment_item(d)
                    yield item
        parse_query = parse_qs(urlparse(response.request.url).query)
        page = int(parse_query["cur_page"][0])
        append_start_url(g_comment_url(item["comic_id"], page+1),
                         COMMENT_URLS_QUEUE)

    @staticmethod
    def build_comment_item(comment):
        item = CommentsItem()
        item["comic_url"] = ""
        item["comment_id"] = comment["id"]
        item["uid"] = comment["uid"]
        item["nickname"] = comment["nickname"]
        item["avatar_url"] = comment["avatar_url"]
        item["pid"] = comment["pid"]
        item["comic_id"] = comment["comic_id"]
        item["author_id"] = comment["author_id"]
        item["author"] = comment["author"]
        item["content"] = comment["content"]
        item["createtime"] = comment["createtime"]
        item["count_reply"] = comment["count_reply"]
        item["up"] = int(comment.get("up", 0))
        item["source"] = int(comment.get("source", 0))
        item["place"] = comment.get("place", "")
        item["ip"] = comment.get("ip", "")
        item["source_name"] = comment.get("source_name", "")
        return item

