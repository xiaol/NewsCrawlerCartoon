import json
import logging
from urlparse import urlparse, parse_qs
import scrapy
from scrapy_redis import spiders

from TouTiaoBaiJia.constants import COMIC_SPIDER_NAME
from TouTiaoBaiJia.constants import CHAPTER_SPIDER_NAME
from TouTiaoBaiJia.constants import COMMENT_SPIDER_NAME
from TouTiaoBaiJia.extract import parse_meta_info, parse_comic_mobile
from TouTiaoBaiJia.extract import re_load_data
from TouTiaoBaiJia.items import ComicsList
from TouTiaoBaiJia.utils import rds

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
        rds.hmset(detail_dict["comic_url"], detail_dict)
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
        pass

