'''
@Author: MengHan
@Go big or Go home
@Date: 2020-09-29 15:47:31
@LastEditTime: 2020-09-29 15:47:40
'''
# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GetImgSpidersItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    mid = scrapy.Field()
    uuid = scrapy.Field()
    day = scrapy.Field()
    url = scrapy.Field()
    image_url = scrapy.Field()
    plate = scrapy.Field()
