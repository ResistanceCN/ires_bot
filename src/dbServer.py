#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pg import DB
import logging
import logging.config

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)



class creatTable():
    def __init__(self, config):
        self.config = config
        try:
            self.db = DB(
                dbname=config.database(), user=config.user(),
                passwd=config.password(), host=config.host())
        except ConnectionError:
            logger.info("conntect postgre db failed")
            sys.exit(1)

    def creat(self):
        if 'public.joininfo' not in self.db.get_tables():
            logger.info("Table joininfo created")
            self.db.query(self.config.joininfo_table())
        else:
            logger.info("Table joininfo existed")
            pass

        if 'public.admininfo' not in self.db.get_tables():
            logger.info("Table admininfo created")
            self.db.query(self.config.admininfo_table())
        else:
            logger.info("Table admininfo existed")
            pass

class pushDB():
    def __init__(self, config):
        self.config = config
        try:
            self.db = DB(
                dbname=config.database(), user=config.user(),
                passwd=config.password(), host=config.host())
        except ConnectionError:
            logger.info("conntect postgre db failed")
            sys.exit(1)

    def push(self, content):
        check = self.db.query(
            "SELECT id FROM joininfo WHERE ingress_id=\'{}\'".format(content['ingress_id']))
        check_id = check.getresult()
        check_id = []
        if len(check_id) == 0:
            self.db.insert('joininfo', ingress_id=content['ingress_id'], telegram_id=content['telegram_id'],
                      telegram_username=content['telegram_username'], area=content['area'], other=content['other'])
        else:
            self.db.query("UPDATE joininfo SET telegram_username=\'{}\' area=\'{}\' other=\'{}\' WHERE ingress_id=\'{}\'".format(
                content['telegram_username'], content['area'], content['other'], content['telegram_id']))

class dbControl(pushDB, creatTable):
    pass

if __name__ == '__main__':
    from parseCfg import parseCfg
    path = 'example.config.yml'
    config = parseCfg(path)
    db = dbControl(config)
    db.creat()
    content = {
        'area': 'T',
        'ingress_id': 'ArielAxionL',
        'other': 'Balthild',
        'telegram_id': '11111111',
        'telegram_username': 'ADA_Refactor'}
    db.push(content)
