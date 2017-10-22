#!/usr/bin/env python
# -*- coding: utf-8 -*-

import redis
import logging
import sys

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)


class cacheControl(object):
    def __init__(self, config):
        self.config = config
        try:
            self.cache = redis.Redis(
                host=config.addr(),
                password=config.redispasswd(),
                charset="utf-8",
                decode_responses=True)

        except ConnectionError:
            logger.info("connecting redis service failed")
            sys.exit(1)

    def hashset(self, telegram_id, **kwargs):
        if kwargs is not None:
            for key, value in kwargs.items():
                self.cache.hset(
                    "{}".format(telegram_id),
                    "{}".format(key),
                    "{}".format(value))

    def hashget(self, telegram_id, *args):
        cache = ''
        for arg in args:
            cache = self.cache.hget(telegram_id, arg)
        return cache

    def hashgetall(self, telegram_id):
        cache = self.cache.hgetall(telegram_id)
        return cache

    def hashclean(self, telegram_id):
        self.cache.delete(telegram_id)
        logger.info("clean %s's cache from redis" % telegram_id)

    def hashflush(self):
        self.cache.flushdb()
        logger.info("flush all cache")


if __name__ == '__main__':
    from parseCfg import parseCfg

    path = 'src/config.example.yml'
    config = parseCfg(path)
    cache = cacheControl(config)
    telegram_id = 11111111
    cache.hashset(telegram_id, ingress_id='ArielAxionL', area='T', other='Balthild')
    print(cache.hashget(telegram_id, 'ingress_id'))
    print(cache.hashgetall(telegram_id))
    cache.hashclean(telegram_id)
    print(cache.hashgetall(telegram_id))
    cache.hashflush()
