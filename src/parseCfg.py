#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import yaml
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)


class psqlCfg():
    def __init__(self):
        self.content = {}

    def host(self):
        try:
            host = self.content['postgres']['host']
            return host
        except IndexError:
            logger.info("Postgresql host config error")

    def database(self):
        try:
            database = self.content['postgres']['database']
            return database
        except IndexError:
            logger.info("Postgresql database config error")

    def user(self):
        try:
            user = self.content['postgres']['user']
            return user
        except IndexError:
            logger.info("Postgresql user config error")

    def password(self):
        try:
            password = self.content['postgres']['password']
            return password
        except IndexError:
            logger.info("Postgresql password error")

    def joininfo_table(self):
        try:
            index = self.content['postgres']['joininfo_table']
            return index
        except IndexError:
            logger.info("Table index is None")

    def admininfo_table(self):
        """Admins info."""
        try:
            adminsindex = self.content['postgres']['admininfo_table']
            return adminsindex
        except IndexError:
            logger.info("Admins index is None")


class tgBotCfg():
    def __init__(self):
        self.content = {}

    def token(self):
        try:
            token = self.content['bot']['token']
            return token
        except IndexError:
            logger.info("Telegram bot token error")

    def admin(self):
        admin = []
        try:
            for i in self.content['bot']['admin']:
                admin.append(i)
            return admin
        except IndexError:
            logger.info("Telegram admin_id doesn't existed")


class redisCfg():
    def __init__(self):
        self.content = {}

    def addr(self):
        try:
            addr = self.content['redis']['addr']
            return addr
        except IndexError:
            logger.info("Redis addr error")

    def redispasswd(self):
        try:
            redispasswd = self.content['redis']['redispasswd']
            return redispasswd
        except IndexError:
            logger.info("Redis password error")


class parseCfg(psqlCfg, tgBotCfg, redisCfg):
    def __init__(self, path):
        super().__init__()
        self.path = path
        try:
            with open(self.path, 'r+') as f:
                self.content = yaml.load(f)
        except FileNotFoundError:
            logger.info("No such file or directory: %s" % (self.path))
            sys.exit(1)


if __name__ == '__main__':
    path = '../config.example.yml'
    config = parseCfg(path)
    print(
        "host: ", config.host(), "\n",
        "database: ", config.database(), "\n",
        "user: ", config.user(), "\n",
        "password: ", config.password(), "\n",
        "joininfo_table: ", config.joininfo_table(), "\n",
        "admininfo_table: ", config.admininfo_table())
    print("token: ", config.token())
    print("admin: ", config.admin())
