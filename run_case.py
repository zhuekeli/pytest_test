#!/usr/bin/python3
# coding=utf-8
import logging
import os
import sys
import unittest

from src.common import global_variable
from src.common.HTMLTestRunner import HTMLTestRunner
from src.common.send_email import SendEmail
from src.config.readConfig import ReadConfig
from src.common.reset_env import ResetEnv

proDir = os.path.split(os.path.realpath(__file__))[0]
test_case_path = os.path.join(proDir, "src/case")
logger = logging.getLogger(__name__)


class RunCase:

    def __init__(self):
        self.readconfig = ReadConfig()
        self.send_mail = SendEmail()
        self.env = ResetEnv()
        self.is_send = self.readconfig.get_value("MAIL", "is_send")

        # 测试报告基本信息
        self.testers = "skoyi tester"
        self.title = "弘机云商城 API测试报告"
        self.description = "测试环境：Test"

        # 导入TestCase目录下的全部测试用例
        self.discover = unittest.defaultTestLoader.discover(test_case_path, pattern='test*.py', top_level_dir=None)
        # 重置测试环境
        self.is_env = self.env.clean_all()
        self.env.init_data()

    def run_test(self):
        """执行测试"""
        if self.is_env:
            try:
                public_path = os.path.dirname(os.path.abspath(sys.argv[0]))
                filename = public_path + "/report/" + "index.html"  # 保存的报告路径和名称
                print("测试报告目录：%s" % filename)
                fp = open(filename, 'wb')
                runner = HTMLTestRunner(stream=fp,
                                        title=self.title,
                                        tester=self.testers,
                                        description=self.description)
                runner.run(self.discover)  # 执行TestCase目录下的全部测试用例
            except Exception as e:
                logger.error(str(e))
            finally:
                logger.warning("---------------All Test End---------------")
                fp.close()
                # 发送电子邮件
                if self.is_send == 'yes':
                    self.send_mail.send_email()
                    logger.warning("测试报告已发送电子邮件！")
                elif self.is_send == 'no':
                    logger.warning("测试报告不发送电子邮件！")
                else:
                    logger.error("测试报告发送电子邮件为未知状态，请检查配置！")
        else:
            logger.warning("Tenant DB清理失败的，无法继续执行测试！！！")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M',
                        filename='logs/skoyi_store.log',
                        filemode='w')
    global_variable.init()
    run = RunCase()

    run.run_test()
