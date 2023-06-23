# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
# from dataclasses import dataclass, field
import scrapy


class LuxonisSrealityItem(scrapy.Item):
    title = scrapy.Field(serialize=str)
    img_url = scrapy.Field(serialize=str)
