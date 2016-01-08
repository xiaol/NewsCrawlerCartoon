from TouTiaoBaiJia.url_factory import g_start_url
from TouTiaoBaiJia.constants import STATUS
from TouTiaoBaiJia.constants import CATEGORY
from TouTiaoBaiJia.constants import CHAPTER_URLS_QUEUE
from TouTiaoBaiJia.constants import COMIC_URLS_QUEUE
from TouTiaoBaiJia.constants import COMMENT_URLS_QUEUE
from TouTiaoBaiJia.utils import append_start_url


def start_comic():
    start_urls = map(g_start_url, [STATUS["complete"]]*3, CATEGORY.values(), [1]*3)
    # for url in start_urls:
    #     append_start_url(url, COMIC_URLS_QUEUE)
    append_start_url(start_urls[0], COMIC_URLS_QUEUE)


if __name__ == '__main__':
    start_comic()






