# -*- coding: utf-8 -*-

# Scrapy settings for zhihuuser project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'zhihuuser'

SPIDER_MODULES = ['zhihuuser.spiders']
NEWSPIDER_MODULE = 'zhihuuser.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'zhihuuser (+http://www.yourdomain.com)'

# Obey robots.txt rules
# 是否遵循robots协议
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
    'cookie': 'q_c1=c4d08dee2eb348d598c3c3a3a46da1f6|1526212849000|1526212849000; d_c0="AFChU6lrlg2PTrogG2jQSHfwoLTGDOBlC2s=|1526212851"; __utma=51854390.671172007.1526212855.1526212855.1526212855.1; __utmz=51854390.1526212855.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmv=51854390.000--|3=entry_date=20180513=1; _zap=aff0a0e0-589d-4df3-abe4-cd69c4dd6b38; l_cap_id="M2E4MDI5MWIyYWZmNDkyMmJmYzY4MzQ1MjI1OTM2NGU=|1526803454|847a9a3b4464fec0dc9abb5d19a93a7bd8ab68f4"; r_cap_id="MGMxZDQ2ODRlMDY3NGVjNTllMDlhODYxY2U1YWRkZmI=|1526803454|2409b851b651e23e704080a967f326f522582053"; cap_id="YTUxN2ZlZWU2OWMzNDAwNzkxYTAyOTBjZjBhNWZjMzY=|1526803454|827bcc4c83feed37c45b5728f098b4364c0856c8"; capsion_ticket="2|1:0|10:1526951501|14:capsion_ticket|44:OGFhODU5YTIwZDRiNGU1ZWFkMjNkZDBjNWI1Y2U0ZjQ=|a503ee8d32f7bb1360eb6bc9dd244f30500b20c94b4d15848fa6c8520e0535e9"; z_c0="2|1:0|10:1526951511|4:z_c0|92:Mi4xYjJjV0F3QUFBQUFBVUtGVHFXdVdEU1lBQUFCZ0FsVk5WN3p3V3dBVE12LTQtbmxuVEtFY0h2YldrSTZvZ29IcllB|16c2af92cb18f08845ec4114117897e082b9596a81f147c54b9dda2bafa5aa00"; _xsrf=1b4a9266-4be6-4b0a-8a2e-cd680b549ced; tgw_l7_route=1c2b7f9548c57cd7d5a535ac4812e20e',
    'authorization': 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20',
}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'zhihuuser.middlewares.ZhihuuserSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'zhihuuser.middlewares.ZhihuuserDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'zhihuuser.pipelines.MongoPipeline': 300,
    # items存到redis
    #'scrapy_redis.pipelines.RedisPipeline': 301,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'


MONGO_URI = 'localhost'
MONGO_DATABASE = 'zhihu'

# 主调度器
# Enables scheduling storing requests queue in redis.
SCHEDULER = "scrapy_redis.scheduler.Scheduler"

# 去重
# Ensure all spiders share same duplicates filter through redis.
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"

# redis连接信息
# Specify the full Redis URL for connecting (optional).
# If set, this takes precedence over the REDIS_HOST and REDIS_PORT settings.
REDIS_URL = 'redis://ubuntu:123456@58.87.120.212:6379'

# 爬虫起始时清空指纹及请求队列
SCHEDULER_FLUSH_ON_START = True
