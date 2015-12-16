# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ComicsItem(scrapy.Item):
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


class ChaptersItem(scrapy.Item):
    comic_url = scrapy.Field()
    chapter_order = scrapy.Field()
    chapter_url = scrapy.Field()
    name = scrapy.Field()
    images = scrapy.Field()
