#!/usr/bin/python3
# coding=utf-8
import configparser
import os

proDir = os.path.split(os.path.realpath(__file__))[0]
configPath = os.path.join(proDir, "application.ini")


class ReadConfig:
    def __init__(self):
        self.cf = configparser.ConfigParser()
        self.cf.read(configPath)

    def get_value(self, section, key):
        return self.cf.get(section, key)

    def get_token(self, name):
        token_id = self.cf.get("TOKEN", name)
        return token_id

    def write_token(self, token_key, token):
        self.cf.set("TOKEN", token_key, token)
        config = open(configPath, 'w')
        with config as conf:
            self.cf.write(conf)
        config.close()


if __name__ == "__main__":
    r = ReadConfig()
    s = r.get_value("API", "base_url")
    print(s)
