#!/usr/bin/python3
# coding=utf-8
import configparser
import os

configPath = os.path.join(os.getcwd(), "resources/application.ini")


class ReadConfig:
    def __init__(self):
        self.cf = configparser.ConfigParser()
        self.cf.read(configPath, encoding='UTF-8')

    def get_value(self, section, key):
        return self.cf.get(section, key)

    def get_token(self, name):
        token_id = self.cf.get("BASE", name)
        return token_id

    def write_token(self, token_key, token):
        self.cf.set("BASE", token_key, token)
        config = open(configPath, 'w',  encoding='UTF-8')
        with config as conf:
            self.cf.write(conf)
        config.close()


if __name__ == "__main__":
    r = ReadConfig()
    s = r.get_value("API", "base_url")
    print(s)
