# -*- coding: utf-8 -*-
import json
from urlparse import urlparse, parse_qs
import re
import scrapy

from TouTiaoBaiJia.items import ComicsItem, ChaptersItem, CommentsItem
from TouTiaoBaiJia.settings import CRAWL_COMICS, CRAWL_COMMENTS


class ComicsSpider(scrapy.Spider):
    """
    抓取漫画分类网站的漫画数据
    """
    name = "Comics"
    pc_index = "http://manhua.dmzj.com"
    m_index = "http://m.dmzj.com"
    pc_info = "http://www.dmzj.com"
    m_info = m_index + "/info"
    m_view = m_index + "/view"
    re_dict = {
        "init_data_pattern": re.compile("initData\((\{.*\})"),
        "init_intro_data_pattern": re.compile('"data":(\[.*?\])'),
        "search_pattern": re.compile("search\.renderResult\((.*)\)"),
        "comment_pattern": re.compile("success_jsonpCallback_201508281031\((.*)\)"),
        "comment_count_pattern": re.compile("jQuery18204413729028310627_1450254773485\((.*)\)")
    }
    incomplete = 2309
    complete = 2310
    category = [3262, 3263, 3264]
    comment_request_url = "http://interface.dmzj.com/api/comment/getComment?" \
                          "callback=success_jsonpCallback_201508281031&type=0" \
                          "&type_id=%s&cur_page=%s"
    comment_count_url = "http://interface.dmzj.com/api/comment/commentTotal?" \
                        "callback=jQuery18204413729028310627_1450254773485" \
                        "&type=0&type_id=%s"
    ajax_request_url = "http://s.acg.178.com/mh/index.php?c=category" \
                       "&m=doSearch&status=%s&reader_group=%s&zone=0" \
                       "&initial=all&type=0&p=%s&callback=search.renderResult"
    start_urls = tuple([ajax_request_url % (complete, c, 1) for c in category])

    def start_requests(self):
        headers = {"Host": "s.acg.178.com",
                   "Referer": "http://manhua.dmzj.com/tags/category_search"
                              "/0-0-0-all-0-0-0-1.shtml"}
        return [scrapy.Request(url, callback=self.parse, headers=headers)
                for url in self.start_urls]

    def parse(self, response):
        """ parse http://manhua.dmzj.com """
        data = self.re_load_data(response, "search_pattern")
        if data is None:
            return
        result = data["result"]
        for r in result:
            comic = ComicsItem()
            comic["comic_id"] = int(r["id"])
            comic["pub_status"] = 1
            comic["name"] = r["name"]
            comic["author"] = r["author"]
            comic["tags"] = r["type"].split("/")
            comic["title_image"] = r["comic_cover"]
            comic["last_update_date"] = r["last_update_date"]
            if self.pc_info in r["comic_url"]:
                #   change pc url to mobile
                m_d_url = self.m_index + urlparse(r["comic_url"]).path
                comic["download_url"] = m_d_url
                comic["comic_url"] = m_d_url
                mobile = True
            else:
                m_d_url = self.m_info + r["comic_url"][:-1] + ".html"
                comic["comic_url"] = m_d_url
                pc_d_url = self.pc_index + r["comic_url"]
                comic["download_url"] = pc_d_url
                mobile = False
            if CRAWL_COMICS:
                if mobile:
                    callback = self.parse_m_info
                    meta = {"comic": comic, "mobile": 1}
                else:
                    callback = self.parse_detail_default
                    meta = {"comic": comic}
                yield scrapy.Request(comic["download_url"],
                                     callback=callback,
                                     meta=meta)
            if CRAWL_COMMENTS:
                yield scrapy.Request(
                    self.comment_count_url % comic["comic_id"],
                    callback=self.parse_comment_count,
                    meta={"type_id": comic["comic_id"],
                          "mobile": 1,
                          "comic_url": comic["comic_url"]}
                )

        if "type=0&p=1&callback" in response.request.url:
            pages = int(data["page_count"])
            reader_group = parse_qs(
                    urlparse(response.request.url).query)["reader_group"][0]
            for i in range(2, pages+1):
                yield scrapy.Request(self.ajax_request_url %
                                     (self.complete, reader_group, i),
                                     callback=self.parse)

    def parse_m_info(self, response):
        """ parse http://m.dmzj.com/xxxx """
        comic = response.meta["comic"]
        a_xpath_string = "//div[@class='sub_r']/p[@class='txtItme']"
        ps = [p for p in response.xpath(a_xpath_string)]
        a_texts = ps[2].xpath("a[@class='pd']/text()").extract()
        if len(a_texts) < 3:
            a_texts = ["", "", ""]
        comic["origin_name"] = ""
        comic["popularity"] = ""
        comic["category"] = a_texts[0]
        comic["area_location"] = a_texts[1]
        summary_xpath_string = "//p[@class='txtDesc autoHeight']/text()"
        comic["summary"] = "".join(response.xpath(
                summary_xpath_string).extract()[0])
        data = self.re_load_data(response, "init_intro_data_pattern")
        if data is None:
            return
        comic["chapter_num"] = len(data)
        chapters = []
        for i, d in enumerate(data[::-1]):
            chapter = ChaptersItem()
            chapter["comic_url"] = comic["comic_url"]
            chapter["chapter_url"] = "/".join([self.m_view,
                                               str(d["comic_id"]),
                                               str(d["id"])+".html"])
            chapter["chapter_name"] = d["chapter_name"]
            chapter["chapter_order"] = d["chapter_order"]
            chapters.append(chapter)
        for chapter in chapters:
            yield scrapy.Request(chapter["chapter_url"],
                                 callback=self.parse_image_page,
                                 meta={"comic": comic,
                                       "chapter": chapter,
                                       "mobile": 1})

    def parse_detail_default(self, response):
        """ parse http://manhua.dmzj.com/xxxx """
        comic = response.meta["comic"]
        info_xpath_string = "//div[@class='anim-main_list']/table/tr"
        trs = [tr for tr in response.xpath(info_xpath_string)]
        if len(trs) != 9:
            yield scrapy.Request(response.request.url,
                                 callback=self.parse_m_info,
                                 meta={"comic": comic,
                                       "mobile": 1})
            return
        comic["origin_name"] = "".join(trs[1].xpath("td/text()").extract())
        comic["area_location"] = "".join(trs[3].xpath("td/a/text()").extract())
        comic["popularity"] = "".join(trs[5].xpath("td/text()").extract())
        comic["category"] = "".join(trs[7].xpath("td/a/text()").extract())

        summary_xpath_string = "//div[@class='line_height_content']/text()"
        summary = response.xpath(summary_xpath_string).extract()[0]
        comic["summary"] = summary[:summary.find("<br>")].strip()

        chapter_string = "//div[@class='middleright_mr']/" \
                         "div[@class='cartoon_online_border']/ul/li/a"
        chapter_urls = []
        chapters = []
        for i, a in enumerate(response.xpath(chapter_string), 1):
            chapter = ChaptersItem()
            chapter["comic_url"] = comic["comic_url"]
            url = a.xpath("@href").extract()[0]
            url = self.m_view + url[:-5] + url[-4:]
            chapter["chapter_url"] = url
            chapter_urls.append(url)
            chapter["name"] = a.xpath("text()").extract()[0]
            chapter["chapter_order"] = i
            chapters.append(chapter)
        comic["chapter_num"] = len(chapter_urls)
        for chapter in chapters:
            yield scrapy.Request(chapter["chapter_url"],
                                 callback=self.parse_image_page,
                                 meta={"comic": comic,
                                       "chapter": chapter,
                                       "mobile": 1})

    def parse_image_page(self, response):
        """ parse http://m.dmzj.com/view """
        chapter = response.meta["chapter"]
        comic = response.meta["comic"]
        data = self.re_load_data(response, "init_data_pattern")
        if data is None:
            return
        chapter["images"] = data["page_url"]
        comic["chapter"] = chapter
        yield comic

    @classmethod
    def re_load_data(cls, response, key):
        pattern = cls.re_dict[key]
        data = re.search(pattern, response.body)
        try:
            data = data.groups()[0]
            data = json.loads(data)
        except Exception:
            data = None
        return data

    def parse_comment_count(self, response):
        type_id = response.meta["type_id"]
        comic_url = response.meta["comic_url"]
        data = self.re_load_data(response, "comment_count_pattern")
        try:
            count = int(data["page_data"])
        except Exception:
            return
        pages = (count + 9) / 10
        for page in range(1, pages+1):
            yield scrapy.Request(
                self.comment_request_url % (type_id, page),
                callback=self.parse_comment,
                meta={"type_id": type_id, "mobile": 1, "comic_url": comic_url}
            )

    def parse_comment(self, response):
        comic_url = response.meta["comic_url"]
        data = self.re_load_data(response, "comment_pattern")
        if data is None:
            return
        comments = data["data"]
        for comment in comments:
            item = self.build_comment_item(comment, comic_url)
            yield item
            if item["count_reply"] != 0:
                for d in comment["reply"]["data"]:
                    item = self.build_comment_item(d, comic_url)
                    yield item

    @staticmethod
    def build_comment_item(comment, comic_url):
        item = CommentsItem()
        item["comic_url"] = comic_url
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
        item["up"] = comment["up"]
        item["source"] = comment["source"]
        item["place"] = comment["place"]
        if "ip" in comment:
            item["ip"] = comment["ip"]
        else:
            item["ip"] = ""
        item["source_name"] = comment["source_name"]
        return item

