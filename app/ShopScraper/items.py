from scrapy.item import Item, Field


class Clothes(Item):
    title = Field()
    price = Field()

    image_urls = Field()
    images = Field()
