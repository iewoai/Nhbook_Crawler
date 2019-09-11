# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NhbookItem(scrapy.Item):
	# define the fields for your item here like:
	# name = scrapy.Field()
	bookname = scrapy.Field()
	imgurl = scrapy.Field()
	imgname = scrapy.Field()
