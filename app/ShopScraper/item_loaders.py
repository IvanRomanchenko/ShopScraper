from scrapy.loader import ItemLoader
from itemloaders.processors import MapCompose, TakeFirst


def price_remove_excess(value):
    return value.replace('$', '').strip()


def title_remove_excess(value):
    return value.replace(", Created for Macy's", "").strip()


def img_url_remove_excess(value):
    return value.split('?')[0]


class ClothesLoader(ItemLoader):
    default_output_processor = TakeFirst()

    title_in = MapCompose(title_remove_excess)
    price_in = MapCompose(price_remove_excess)
    img_url_in = MapCompose(img_url_remove_excess)
