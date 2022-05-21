from abc import ABC, abstractmethod
from os import getenv
from redis import Redis
import ujson


class Storage(ABC):
    """ Abstract class for all storages """

    @classmethod
    @abstractmethod
    def get_data(cls, db_key: str) -> list:
        return []

    @abstractmethod
    def write_item(self, item: dict):
        pass


class RedisStorage(Redis, Storage):
    """ Storage based on Redis """

    def __init__(self, spider_name: str):
        self.spider_name = spider_name

        host = getenv('REDIS_HOST', 'localhost')
        username = getenv('REDIS_USER', None)
        password = getenv('REDIS_PASSWORD', None)

        super().__init__(host=host, username=username, password=password)

    @classmethod
    def get_data(cls, spider_name: str) -> list:
        self = cls(spider_name)
        return [
            ujson.loads(self.lindex(spider_name, i))
                for i in range(self.llen(spider_name))
        ]

    def write_item(self, item: dict):
        self.rpush(self.spider_name, ujson.dumps(item))


class JsonStorage(Storage):
    """ Storage for work with JSON """

    def __init__(self):
        self.file = None

    def open_file(self, file_name: str, mode: str = 'r'):
        """ Open file for work """
        self.file = open(file_name, mode=mode)

    @classmethod
    def get_data(cls, file_name: str) -> list:
        self = cls()
        self.open_file(file_name)

        if file_name.endswith('.json'):
            data = ujson.load(self.file)
        else:
            data = [ujson.loads(item) for item in self.file.readlines()]

        self.file.close()

        return data

    def dump_n_close(self, item_list: list,
                     ensure_ascii: bool = False, indent: int = 2):
        """ Dump list with items to json-file and close it after that """
        ujson.dump(item_list, self.file, ensure_ascii=ensure_ascii, indent=indent)
        self.file.close()

    def write_item(self, item: dict):
        self.file.write(ujson.dumps(item) + "\n")
