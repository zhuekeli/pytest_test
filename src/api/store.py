from src.common import http
from src.config.readConfig import ReadConfig

config = ReadConfig()


def clear_all_cache() -> None:
    """清除所有的缓存记录
    """
    url = '{}/clear/system-cache'.format(config.get_value('API', 'base_url'))
    http.delete(url)
