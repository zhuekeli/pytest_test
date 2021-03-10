import random

units = ['台', '支', '把', '套', '辆', '千克', '只', '个', '片', '件', '米', '份', '付', '块', '根', '板', '个', '卷', '套', '条', '本', '盒',
         '副', '包', '顶', '版', '对', '组', '桶', '架', '小盒', '卡', '双', '箱', '公斤', '袋', '张', '瓶', '盘', '斤', '捆', '粒', '筒', '圈',
         '罐']


def random_unit():
    return units[random.randint(0, len(units))]


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
