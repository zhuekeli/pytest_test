"""读取 yaml 文件示例
"""
import logging

import yaml
from jsonpath import jsonpath

logger = logging.getLogger(__name__)


class ReadYaml(object):

    def __init__(self, filename):
        # 指定编码格式解决，win下跑代码抛出错误
        with open(filename, 'r', encoding='utf-8') as file:
            self.config_dict = yaml.load(file.read(), Loader=yaml.FullLoader)

    def read_config(self, expr: str = '.') -> dict:
        """默认读取config目录下的config.yaml配置文件，根据传递的expr jsonpath表达式可任意返回任何配置项
        :param expr: 提取表达式, 使用jsonpath语法,默认值提取整个读取的对象
        return 根据表达式返回的值
        """
        try:
            result = jsonpath(self.config_dict, expr)[0]
        except Exception as e:
            logger.error(f'读取配置文件内容失败 {e}')
            result = None
        return result
