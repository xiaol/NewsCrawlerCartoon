from TouTiaoBaiJia.url_factory import g_start_url
from TouTiaoBaiJia.constants import STATUS
from TouTiaoBaiJia.constants import CATEGORY
from TouTiaoBaiJia.constants import CHAPTER_URLS_QUEUE
from TouTiaoBaiJia.constants import COMIC_URLS_QUEUE
from TouTiaoBaiJia.constants import COMMENT_URLS_QUEUE
from TouTiaoBaiJia.utils import append_start_url


def start_comic():
    start_urls = list()
    juvenile = CATEGORY["juvenile"]
    maiden = CATEGORY["maiden"]
    youth = CATEGORY["youth"]
    # for page in range(1, 375):
    #     start_urls.append(g_start_url(STATUS["complete"], juvenile, page))
    # for page in range(1, 123):
    #     start_urls.append(g_start_url(STATUS["complete"], maiden, page))
    # for page in range(1, 22):
    #     start_urls.append(g_start_url(STATUS["complete"], youth, page))
    start_urls.append(g_start_url(STATUS["complete"], juvenile, 1))
    start_urls.append(g_start_url(STATUS["complete"], maiden, 1))
    start_urls.append(g_start_url(STATUS["complete"], youth, 1))
    for url in start_urls:
        append_start_url(url, COMIC_URLS_QUEUE)


if __name__ == '__main__':
    start_comic()






