# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ForumItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    threadReplies = scrapy.Field()
    threadTitle = scrapy.Field()
    userName = scrapy.Field()
    userPosts = scrapy.Field()
    userPolitics = scrapy.Field()
    userMoney = scrapy.Field()
    postDateTime = scrapy.Field()
    postText = scrapy.Field()