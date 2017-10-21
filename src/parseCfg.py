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
    def host(self):
        try:
            host = self.content['postgres']['host']
        except IndexError:
            logger.info("Postgresql host config error")
        return host

    def database(self):
        try:
            database = self.content['postgres']['database']
        except IndexError:
            logger.info("Postgresql database config error")
        return database

    def user(self):
        try:
            user = self.content['postgres']['user']
        except IndexError:
            logger.info("Postgresql user config error")
        return user

    def password(self):
        try:
            password = self.content['postgres']['password']
        except IndexError:
            logger.info("Postgresql password error")
        return password

    def joininfo_table(self):
        try:
            index = self.content['postgres']['joininfo_table']
        except IndexError:
            logger.info("Table index is None")
        return index

    def admininfo_table(self):
        """Admins info."""
        try:
            adminsindex = self.content['postgres']['admininfo_table']
        except IndexError:
            logger.info("Admins index is None")
        return adminsindex

class tgBotCfg():
    def token(self):
        try:
            token = self.content['bot']['token']
        except IndexError:
            logger.info("Telegram bot token error")
        return token

    def admin(self):
        admin = []
        try:
            for i in self.content['bot']['admin']:
                admin.append(i)
        except IndexError:
            logger.info("Telegram admin_id doesn't existed")
        return admin

class redisCfg():
    def addr(self):
        try:
            addr = self.content['redis']['addr']
        except IndexError:
            logger.info("Redis addr error")
        return addr

    def redispasswd(self):
        try:
            redispasswd = self.content['redis']['redispasswd']
        except IndexError:
            logger.info("Redis password error")
        return redispasswd

class parseCfg(psqlCfg, tgBotCfg, redisCfg):
    def __init__(self, path):
        self.path = path
        try:
            with open(self.path, 'r+') as f:
                self.content = yaml.load(f)
        except FileNotFoundError:
            logger.info("No such file or directory: %s" % (self.path))
            sys.exit(1)

if __name__ == '__main__':
    path = 'src/config.example.yml'
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
