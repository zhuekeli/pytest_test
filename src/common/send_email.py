#!/usr/bin/python3
# coding=utf-8
import logging
import smtplib
from datetime import datetime
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# 路径
from src.config.application_config import ApplicationConfig

logger = logging.getLogger(__name__)


class SendEmail:

    def __init__(self):
        self.config = ApplicationConfig()
        self.host = self.config.get_value('MAIL', 'host')  # 邮箱服务器
        self.user = self.config.get_value('MAIL', 'user')  # 发件人用户名
        self.password = self.config.get_value('MAIL', 'password')  # 发件人邮箱授权码，非登录密码
        self.sender = self.config.get_value('MAIL', 'sender')  # 发件人邮箱
        self.title = self.config.get_value('MAIL', 'title') + str(datetime.now().strftime("%Y%m%d"))  # 邮件标题
        self.receive_user = self.config.get_value('MAIL', 'receive_user')  # 收件人邮箱
        self.receive_user_list = []

        for i in str(self.receive_user).split(';'):
            self.receive_user_list.append(i)

    def send_email(self, content=None):
        """把最新的测试报告以邮件的方式发送"""
        # 构造邮件
        if content is None:
            content = "<a>http://{}:{}</a>".format(self.config.get_value('BASE', 'test_service_host'),
                                                   self.config.get_value('BASE', 'test_service_port'))
        message = MIMEMultipart()
        message['From'] = "{}".format(self.sender)  # 发件人
        message['To'] = ",".join(self.receive_user_list)  # 收件人
        message['Subject'] = Header(self.title, 'utf-8')  # 标题
        message.attach(MIMEText(content, 'html', 'utf-8'))

        # 发送邮件
        try:
            server = smtplib.SMTP()
            server.connect(self.host)
            server.login(self.user, self.password)  # 登录验证
            server.sendmail(self.sender, self.receive_user_list, message.as_string())  # 发送
            server.quit()  # 关闭
            logger.info("邮件发送成功！")
        except smtplib.SMTPException as e:
            logger.error("邮件发送失败！请检查邮件配置%s" % e)


if __name__ == "__main__":
    s = SendEmail()
    s.send_email("搜索测试")
