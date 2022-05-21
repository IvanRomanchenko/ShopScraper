from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from loguru import logger

from ..items import Clothes
from ..item_loaders import ClothesLoader


class MacysCrawlSpider(CrawlSpider):
    name = 'macys'
    allowed_domains = ['macys.com']
    start_urls = ['https://www.macys.com']

    rules = (
        # women`s clothing
        Rule(LinkExtractor(
            allow=('shop/womens-clothing/all-womens-clothing',)),
            callback='parse_clothes'
        ),
        # men`s clothing
        Rule(LinkExtractor(
            allow=('shop/mens-clothing/all-mens-clothing',)),
            callback='parse_clothes'
        ),
    )

    def parse_clothes(self, response):
        for item in response.xpath("//div[@class='productThumbnail "
                                   "redesignEnabled']"):
            yield self.parse_item(item)

        yield from response.follow_all(
            response.xpath("//li[@class='next-page']/div[1]/a"),
            self.parse_clothes
        )

    @staticmethod
    def parse_item(inp_item):
        loader = ClothesLoader(item=Clothes())

        prod_descr_xpath = "div[@class='productDetail']/" \
                           "div[@class='productDescription']/"
        loader.add_value(
            'title', inp_item.xpath(
                f"{prod_descr_xpath}"
                f"a/@title").get()
        )
        loader.add_value(
            'price', inp_item.xpath(
                f"{prod_descr_xpath}"
                f"div[@class='priceInfo']/div[@class='prices']/"
                f"div[last()]/span[1]/text()[2]").get()
        )
        img_url = inp_item.xpath(
                "div[1]/a/div/picture/img/@data-lazysrc").get()
        loader.add_value(
            'img_url', img_url
        )
        if not img_url:
            logger.success(inp_item.xpath(
                "div[1]/a/div/picture/img").get())

        return loader.load_item()
