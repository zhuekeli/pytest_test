import random
import string

from run_case import logger

units = ['台', '支', '把', '套', '辆', '千克', '只', '个', '片', '件', '米', '份', '付', '块', '根', '板', '个', '卷', '套', '条', '本', '盒',
         '副', '包', '顶', '版', '对', '组', '桶', '架', '小盒', '卡', '双', '箱', '公斤', '袋', '张', '瓶', '盘', '斤', '捆', '粒', '筒', '圈',
         '罐']


def random_unit():
    return units[random.randint(0, len(units) - 1)]


def random_price():
    """
    随机价格
    """
    return random.randint(100, 100000) * 0.01


def random_number():
    """
    随机数量
    """
    return random.randint(1, 1000)


def random_phone():
    """
    随机手机号
    """
    num_start = ['141', '142', '143', '144', '145', '146', '147', '148', '149']
    start = random.choice(num_start)
    end = ''.join(random.sample(string.digits, 8))
    phone_number = start + end
    logger.info(f'随机手机号码已经生成:{phone_number}')
    return phone_number
