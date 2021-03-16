#!/usr/bin/python3
# coding=utf-8
import configparser
import os

cur_path = os.path.split(os.path.realpath(__file__))[0]
configPath = os.path.join(cur_path, "../../resources/application.ini")


class ApplicationConfig:
    def __init__(self):
        self.cf = configparser.ConfigParser()
        self.cf.read(configPath, encoding='UTF-8')

    def get_value(self, section, key):
        return self.cf.get(section, key)

    def get_token(self, name):
        token_id = self.cf.get("BASE", name)
        return token_id

    def set_value(self, section, key, value):
        self.cf.set(section, key, value)
        config = open(configPath, 'w', encoding='UTF-8')
        with config as conf:
            self.cf.write(conf)
        config.close()


if __name__ == "__main__":
    r = ApplicationConfig()
    s = r.get_value("API", "base_url")
    print(s)
