# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item,Field


#class UserItem(scrapy.Item):(原写法)
# 以下为简写，，引入 Item,Field
class UserItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = Field()
    name = Field()
    type = Field()
    headline = Field()
    url = Field()
    answer_count = Field()
    articles_count = Field()
    allow_message = Field()
    avatar_url = Field()
    avatar_url_template = Field()
    badge= Field()
    employments = Field()
    follower_count = Field()
    gender = Field()
    is_advertiser = Field()
    is_blocking = Field()
    is_followed = Field()
    is_following = Field()
    is_org = Field()
    url_token = Field()
    user_type = Field()