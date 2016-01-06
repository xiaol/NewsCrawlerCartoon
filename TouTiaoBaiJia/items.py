# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ComicsItem(scrapy.Item):
    comic_id = scrapy.Field()   # comic id for crawl comment
    comic_url = scrapy.Field()
    pub_status = scrapy.Field()     # 1: 已完结, 0: 未完结
    download_url = scrapy.Field()
    name = scrapy.Field()
    author = scrapy.Field()
    title_image = scrapy.Field()
    last_update_date = scrapy.Field()

    tags = scrapy.Field()  # 体裁
    origin_name = scrapy.Field()     # 原名
    category = scrapy.Field()   # 分类标签
    area_location = scrapy.Field()   # 所属地域
    popularity = scrapy.Field()     # 人气
    summary = scrapy.Field()    # 简介
    chapter_num = scrapy.Field()
    chapter = scrapy.Field()

    mobile = scrapy.Field()     # use mobile user agent or not


class ChaptersItem(scrapy.Item):
    comic_url = scrapy.Field()
    chapter_order = scrapy.Field()
    chapter_url = scrapy.Field()
    chapter_name = scrapy.Field()   # move name to chapter_name
    images = scrapy.Field()

    comic = scrapy.Field()  # add comic meta info


class CommentsItem(scrapy.Item):
    comic_url = scrapy.Field()
    comment_id = scrapy.Field()
    uid = scrapy.Field()
    nickname = scrapy.Field()
    avatar_url = scrapy.Field()
    pid = scrapy.Field()
    comic_id = scrapy.Field()
    author_id = scrapy.Field()
    author = scrapy.Field()
    content = scrapy.Field()
    createtime = scrapy.Field()
    count_reply = scrapy.Field()
    up = scrapy.Field()
    source = scrapy.Field()
    place = scrapy.Field()
    ip = scrapy.Field()
    source_name = scrapy.Field()
