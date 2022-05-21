from itemadapter import ItemAdapter

from .storages import JsonStorage, RedisStorage


class JsonWriterPipeline(JsonStorage):
    """
        Creates a JSON-file with written in it items
         (for a small amount of items)
    """

    def __init__(self):
        self.item_list = None
        super().__init__()

    def open_spider(self, spider):
        self.open_file(f"{spider.name}.json", mode='w')
        self.item_list = []

    def close_spider(self, spider):
        self.dump_n_close(self.item_list)

    def process_item(self, item, spider):
        self.item_list.append(ItemAdapter(item).asdict())
        return item


class JsonLineWriterPipeline(JsonStorage):
    """
        Creates a JSONLine-file with written in it items
         (for a large amount of items)
    """

    def open_spider(self, spider):
        self.open_file(f"{spider.name}.jl", mode='w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        self.write_item(ItemAdapter(item).asdict())
        return item


class RedisWriterPipeline(RedisStorage):
    """
        Writes all items to Redis DB
         (for a large amount of items)
    """

    def open_spider(self, spider):
        super().__init__(spider.name)

    def process_item(self, item, spider):
        self.write_item(ItemAdapter(item).asdict())
        return item
