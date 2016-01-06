import urllib

from constants import START_URL_PREFIX

_PARAMS = {
    "c": "category",
    "m": "doSearch",
    "zone": 0,
    "initial": "all",
    "type": 0,
    "callback": "search.renderResult",
    "_order": "t",
    "status": None,
    "reader_group": None,
    "p": None,
}


def g_start_url(status, group, page):
    param = _PARAMS.copy()
    param["status"] = status
    param["reader_group"] = group
    param["p"] = page
    return START_URL_PREFIX + urllib.urlencode(param)


if __name__ == "__main__":
    from constants import CATEGORY, STATUS
    start_urls = map(g_start_url,
                  [STATUS["complete"]]*3,
                  CATEGORY.values(),
                  [1]*3)
    print start_urls
