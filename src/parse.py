#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import yaml
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)

class Parse():
    def __init__(self, path):
        self.path = path
        try:
            with open(self.path, 'r+') as f:
                self.content = yaml.load(f)
        except FileNotFoundError:
            logger.info("No such file or directory: %s" % (self.path))
            sys.exit(1)

class PsqlCfg(Parse):
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

    def index(self):
        try:
            index = self.content['postgres']['index']
        except IndexError:
            logger.info("Table index is None")
        return index

    def adinfo(self):
        """Admins info."""
        try:
            adminsindex = self.content['postgres']['adinfo']
        except IndexError:
            logger.info("Admins index is None")
        return adminsindex

class TgBot(Parse):
    def token(self):
        try:
            token = self.content['bot']['token']
        except IndexError:
            logger.info("Telegram bot token error")
        return token


if __name__ == '__main__':
    path = 'src/example.config.yml'
    config = PsqlCfg(path)
    print(
        "host: ", config.host(), "\n",
        "database: ", config.database(), "\n",
        "user: ", config.user(), "\n",
        "password: ", config.password(), "\n",
        "index: ", config.index()), "\n",
    config = TgBot(path)
    print("token: ", config.token())
