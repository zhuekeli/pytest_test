import os

import yaml


def read_case_data():
    """加载case 测试数据"""
    cur_path = os.path.split(os.path.realpath(__file__))[0]
    file_name = os.path.join(cur_path, "../../resources/test_case_data.yaml")
    with open(file_name, 'r', encoding='utf-8') as file:
        yaml_dict = yaml.load(file.read(), Loader=yaml.FullLoader)

    result = []
    for suite in yaml_dict:
        for case in suite['cases']:
            case['suite_name'] = suite['name']
            result.append(case)
    return result
