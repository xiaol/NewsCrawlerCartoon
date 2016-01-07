# coding: utf8

DOMAIN = "http://manhua.dmzj.com"
M_DOMAIN = "http://m.dmzj.com"
M_DOMAIN_INFO = M_DOMAIN + "/info"
M_DOMAIN_VIEW = M_DOMAIN + "/view"

ABNORMAL_DOMAIN = "http://www.dmzj.com"

START_URL_PREFIX = "http://s.acg.178.com/mh/index.php?"
HIT = "http://manhua.dmzj.com/hits/%s.json"     # use for popularity
STATIC_HIT = "http://www.dmzj.com/static/hits/%s.json"


COMMENT_REQUEST_URL = "http://interface.dmzj.com/api/comment/getComment?" \
                      "callback=success_jsonpCallback_201508281031&type=0" \
                      "&type_id=%s&cur_page=%s"
COMMENT_COUNT_URL = "http://interface.dmzj.com/api/comment/commentTotal?" \
                    "callback=jQuery18204413729028310627_1450254773485" \
                    "&type=0&type_id=%s"


CATEGORY = {
    "juvenile": 3262,   # 少年
    "maiden": 3263,     # 少女
    "youth": 3264,      # 青年
}

STATUS = {
    "complete": 2310,
    "incomplete": 2309,
}


COMIC_SPIDER_NAME = "dmzj_comic_spider"
CHAPTER_SPIDER_NAME = "dmzj_chapter_spider"
COMMENT_SPIDER_NAME = "dmzj_image_spider"

COMIC_URLS_QUEUE = "{0}:{1}".format(COMIC_SPIDER_NAME, "start_urls")
CHAPTER_URLS_QUEUE = "{0}:{1}".format(CHAPTER_SPIDER_NAME, "start_urls")
COMMENT_URLS_QUEUE = "{0}:{1}".format(COMMENT_SPIDER_NAME, "start_urls")
