#!/usr/bin/python3
# coding=utf-8
import logging
import os
import smtplib
from datetime import datetime
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from src.config.readConfig import ReadConfig

# 路径
report_path = os.path.join(os.getcwd(), 'report')

local_readConfig = ReadConfig()
logger = logging.getLogger(__name__)


class SendEmail:
    def __init__(self):
        global host, user, password, sender, title
        host = local_readConfig.get_value('MAIL', 'host')  # 邮箱服务器
        user = local_readConfig.get_value('MAIL', 'user')  # 发件人用户名
        password = local_readConfig.get_value('MAIL', 'password')  # 发件人邮箱授权码，非登录密码
        sender = local_readConfig.get_value('MAIL', 'sender')  # 发件人邮箱
        title = local_readConfig.get_value('MAIL', 'title') + str(datetime.now().strftime("%Y%m%d"))  # 邮件标题
        self.receive_user = local_readConfig.get_value('MAIL', 'receive_user')  # 收件人邮箱
        self.receive_user_list = []
        for i in str(self.receive_user).split('/'):
            self.receive_user_list.append(i)

    def send_email(self):
        """把最新的测试报告以邮件的方式发送"""
        # 构造邮件
        content = "<a>http://{}:{}</a>".format(local_readConfig.get_value('BASE', 'test_service_host'),
                                               local_readConfig.get_value('BASE', 'test_service_port'))
        message = MIMEMultipart()
        message['From'] = "{}".format(sender)  # 发件人
        message['To'] = ",".join(self.receive_user_list)  # 收件人
        message['Subject'] = Header(title, 'utf-8')  # 标题
        message.attach(MIMEText(content, 'html', 'utf-8'))

        # 发送邮件
        try:
            server = smtplib.SMTP()
            server.connect(host)
            server.login(user, password)  # 登录验证
            server.sendmail(sender, self.receive_user_list, message.as_string())  # 发送
            server.quit()  # 关闭
            logger.info("邮件发送成功！")
        except smtplib.SMTPException as e:
            # print("邮件发送失败！")
            logger.error("邮件发送失败！请检查邮件配置%s" % e)


if __name__ == "__main__":
    s = SendEmail()
    s.send_email("搜索测试")
