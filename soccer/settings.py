# -*- coding: utf-8 -*-

BOT_NAME = 'soccer'

SPIDER_MODULES = ['soccer.spiders']
NEWSPIDER_MODULE = 'soccer.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'scrapy-soccer (https://github.com/zseta/scrapy-soccer)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

#LOG_LEVEL = 'INFO'

#DB_SETTINGS = {
#    'db': 'soccer_db',
#    'user': 'soccer_user',
#    'passwd': 'soccer_pass',
#    'host': '0.0.0.0',
#}

# Cleaning pipeline enabled
# To use database pipeline set host, user+pass in the pipeline and uncomment it below
ITEM_PIPELINES = {
    'soccer.pipelines.CleaningPipeline': 300,
    #'soccer.pipelines.DatabasePipeline': 301
}

# Http-caching enabled so scrapy requests the website only once in 24 hours
# at the same time you can scrape data from the cached html files
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 60*60*24
HTTPCACHE_DIR = 'httpcache'
