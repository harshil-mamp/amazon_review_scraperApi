# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AmazonProItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    rating = scrapy.Field()
    username = scrapy.Field()
    description = scrapy.Field()
    date = scrapy.Field()
    image_urls = scrapy.Field()
    asin_number = scrapy.Field()
    product_url = scrapy.Field()
    # images = scrapy.Field()

    
