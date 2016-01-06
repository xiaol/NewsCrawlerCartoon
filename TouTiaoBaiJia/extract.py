import json
from urlparse import urlparse, parse_qs
import re
import logging

from utils import rds
from TouTiaoBaiJia.items import ComicsItem, ChaptersItem
from TouTiaoBaiJia.constants import M_DOMAIN, M_DOMAIN_INFO, M_DOMAIN_VIEW
from TouTiaoBaiJia.constants import DOMAIN, ABNORMAL_DOMAIN

_logger = logging.getLogger(__name__)


PATTERN = {
        "init_data": re.compile("initData\((\{.*\})"),
        "init_intro_data": re.compile('"data":(\[.*?\])'),
        "search": re.compile("search\.renderResult\((.*)\)"),
        "comment": re.compile("success_jsonpCallback_201508281031\((.*)\)"),
        "comment_count": re.compile("jQuery18204413729028310627_1450254773485\((.*)\)")
}


def re_load_data(body, key):
    pattern = PATTERN[key]
    data = re.search(pattern, body)
    try:
        data = json.loads(data.groups()[0])
    except:
        data = None
    return data


def parse_meta_info(response):
    cache = rds
    comics = list()
    data = re_load_data(response.body_as_unicode(), "search")
    if data is None:
        _logger.error("parse error url: %s" % response.url)
        return comics, 0
    elif data["status"] != "OK":
        return comics, 0
    results = data["result"]
    p = int(data["page_count"])
    page = p
    for r in results:
        comic = ComicsItem()
        comic["comic_id"] = int(r["id"])
        comic["pub_status"] = 1     # complete
        comic["name"] = r["name"]
        comic["author"] = r["author"]
        comic["tags"] = r["type"].split("/")
        comic["title_image"] = r["comic_cover"]
        comic["last_update_date"] = r["last_update_date"]
        url = r["comic_url"]
        if ABNORMAL_DOMAIN in url:
            mobile_url = M_DOMAIN + urlparse(url).path
            comic["comic_url"] = comic["download_url"] = mobile_url
            comic["mobile"] = True
        else:
            mobile_url = M_DOMAIN_INFO + url[:-1] + ".html"
            comic["comic_url"] = mobile_url
            comic["download_url"] = DOMAIN + url
            comic["mobile"] = False
        status = cache.hget(comic["comic_url"], "pub_status")
        if status == "1":
            page = 0    # if already crawled in cache
            print("url: %s alread in crawled" % comic["comic_url"])
        else:
            page = p
            comics.append(comic)
            cache_comic = dict(comic)
            cache_comic["tags"] = json.dumps(cache_comic["tags"])
            cache.hmset(comic["comic_url"], cache_comic)
    return comics, page


def parse_comic_mobile(response):
    comic = response.meta["comic"]
    a_xpath = "//div[@class='sub_r']/p[@class='txtItme']"
    ps = [p for p in response.xpath(a_xpath)]
    a_texts = ps[2].xpath("a[@class='pd']/text()").extract()
    if len(a_texts) < 3:
        a_texts = ["", "", ""]
    comic["origin_name"] = ""
    comic["popularity"] = ""
    comic["category"] = a_texts[0]
    comic["area_location"] = a_texts[1]
    summary_xpath = "//p[@class='txtDesc autoHeight']/text()"
    comic["summary"] = "".join(response.xpath(summary_xpath).extract()[0])
    data = re_load_data(response.body_as_unicode(), "init_intro_data")

    chapters = list()
    if data is None:
        return chapters
    comic["chapter_num"] = len(data)
    for i, d in enumerate(data[::-1]):
        chapter = ChaptersItem()
        chapter["comic_url"] = comic["comic_url"]
        url_words = [M_DOMAIN_VIEW, str(d["comic_id"]), str(d["id"])+".html"]
        chapter["chapter_url"] = "/".join(url_words)
        chapter["chapter_name"] = d["chapter_name"]
        chapter["chapter_order"] = d["chapter_order"]
        chapter["comic"] = comic
        chapters.append(chapter)
    return chapters






