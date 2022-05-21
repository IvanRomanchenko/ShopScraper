from scrapy.item import Item, Field


class Clothes(Item):
    title = Field()
    price = Field()
    img_url = Field()
