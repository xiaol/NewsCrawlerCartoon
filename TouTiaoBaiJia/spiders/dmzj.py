import json
import logging
from urlparse import urlparse, parse_qs
import scrapy

from TouTiaoBaiJia.constants import HIT, STATIC_HIT
from TouTiaoBaiJia.extract import parse_meta_info, parse_comic_mobile
from TouTiaoBaiJia.extract import re_load_data
from TouTiaoBaiJia.constants import CATEGORY, STATUS
from TouTiaoBaiJia.url_factory import g_start_url

_logger = logging.getLogger(__name__)


class DMZJSpider(scrapy.Spider):
    name = "Spider_DMZJ_Comics"
    start_urls = map(g_start_url, [STATUS["complete"]]*3,
                     CATEGORY.values(), [1]*3)

    def parse(self, response):
        parse_query = parse_qs(urlparse(response.request.url).query)
        p = int(parse_query["p"][0])
        group = parse_query["reader_group"][0]
        comics, page = parse_meta_info(response)
        print("page: %s" % p)
        for comic in comics:
            print("name: %s, comic: %s" % (comic["name"], comic["comic_url"]))
            url = STATIC_HIT if comic["mobile"] else HIT
            url = url % comic["comic_id"]
            yield scrapy.Request(url,
                                 callback=self.parse_popularity,
                                 meta={"comic": comic})
        if p <= page:
            url = g_start_url(STATUS["complete"], group, p+1)
            yield scrapy.Request(url, callback=self.parse)

    def parse_popularity(self, response):
        comic = response.meta["comic"]
        try:
            comic["popularity"] = json.loads(response.body)["hot_hits"]
        except:
            pass
        yield scrapy.Request(comic["comic_url"],
                             callback=self.parse_comic,
                             meta={"comic": comic, "mobile": 1})

    def parse_comic(self, response):
        chapters = parse_comic_mobile(response)
        for chapter in chapters:
            yield scrapy.Request(chapter["chapter_url"],
                                 callback=self.parse_chapter,
                                 meta={"chapter": chapter, "mobile": 1})

    def parse_chapter(self, response):
        data = re_load_data(response.body_as_unicode(), "init_data")
        if data is None:
            return
        chapter = response.meta["chapter"]
        chapter["images"] = data["page_url"]
        yield chapter




