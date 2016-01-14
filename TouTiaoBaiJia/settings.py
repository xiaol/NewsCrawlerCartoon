# -*- coding: utf-8 -*-

# Scrapy settings for TouTiaoBaiJia project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'TouTiaoBaiJia'

SPIDER_MODULES = ['TouTiaoBaiJia.spiders']
NEWSPIDER_MODULE = 'TouTiaoBaiJia.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'TouTiaoBaiJia (+http://www.yourdomain.com)'

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS=32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 1
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN=16
#CONCURRENT_REQUESTS_PER_IP=16

# Disable cookies (enabled by default)
#COOKIES_ENABLED=False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED=False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'TouTiaoBaiJia.middlewares.MyCustomSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.UserAgentMiddleware': None,
    'TouTiaoBaiJia.middleware.RotateUserAgentMiddleware': 400,
}

# download handlers, if not set this, an error will occur
DOWNLOAD_HANDLERS = {'s3': None}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    # 'scrapy.pipelines.images.ImagesPipeline': 1,
    'TouTiaoBaiJia.pipelines.StorePipeline': 500,
    # 'TouTiaoBaiJia.pipelines.RedisPipeline': 400,
}
# IMAGES_STORE = "/Users/lee/work/downloads/comics"

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
# NOTE: AutoThrottle will honour the standard settings for concurrency and delay
#AUTOTHROTTLE_ENABLED=True
# The initial download delay
#AUTOTHROTTLE_START_DELAY=5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY=60
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG=False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED=True
#HTTPCACHE_EXPIRATION_SECS=0
#HTTPCACHE_DIR='httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES=[]
#HTTPCACHE_STORAGE='scrapy.extensions.httpcache.FilesystemCacheStorage'

# FEED_URI = "/home/lee/Work/TouTiaoBaiJia/comics.jl"
# FEED_FORMAT = "jsonlines"
# FEED_STORAGES = {
#     'file': 'scrapy.extensions.feedexport.FileFeedStorage',
# }
# FEED_EXPORTERS = {
#     'jsonlines': 'scrapy.exporters.JsonLinesItemExporter',
# }

LOG_FILE = "TouTiaoBaiJia.log"
LOG_LEVEL = "INFO"

REDIS_HOST = "ccd827d637514872.m.cnhza.kvstore.aliyuncs.com"
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_PASSWORD = "ccd827d637514872:LYcache2015"
REDIS_URL = 'redis://ccd827d637514872:LYcache2015@ccd827d637514872.m.cnhza.kvstore.aliyuncs.com:6379'

# POSTGRES = "postgresql://postgres:lee@localhost/test"

CRAWL_COMICS = True
CRAWL_COMMENTS = True

