# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CambridgeDictScraperItem(scrapy.Item):
    word=scrapy.Field()
    part_of_speech=scrapy.Field()
    synonym=scrapy.Field()
    definition=scrapy.Field()
    examples=scrapy.Field()

class VanDaleDictScraperItem(scrapy.Item):
    word=scrapy.Field()
    definition_en = scrapy.Field()
    example_nl = scrapy.Field()
    example_en = scrapy.Field()
