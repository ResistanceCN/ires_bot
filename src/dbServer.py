#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pg import DB
import sys
import logging

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
            logger.info("conntecting postgresql service failed")
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
        _check = self.db.query(
            "SELECT id FROM joininfo WHERE ingress_id=\'{}\';".format(content['ingress_id']))
        _check_id = _check.getresult()
        if len(_check_id) == 0:
            self.db.insert('joininfo', ingress_id=content['ingress_id'], telegram_id=content['telegram_id'],
                           telegram_username=content['telegram_username'], area=content['area'], other=content['other'])
        else:
            self.db.query("UPDATE joininfo SET telegram_username=\'{}\', area=\'{}\', other=\'{}\' WHERE ingress_id=\'{}\';".format(
                content['telegram_username'], content['area'], content['other'], content['ingress_id']))


class admin():
    def __init__(self, config):
        self.config = config
        try:
            self.db = DB(
                dbname=config.database(), user=config.user(),
                passwd=config.password(), host=config.host())
        except ConnectionError:
            logger.info("conntect postgre db failed")
            sys.exit(1)

    def creatAdmin(self):
        for i in self.config.admin():
            _check = self.db.query(
                "SELECT telegram_id FROM admininfo WHERE telegram_id=\'{}\';".format(i['telegram_id']))
            _check_id = _check.getresult()
            if len(_check_id) == 0:
                self.db.insert(
                    'admininfo', telegram_id=i['telegram_id'],
                    telegram_username=i['telegram_username'], area=i['area'])
                logger.info("add admin member: %s" % i)
            else:
                self.db.query(
                    "UPDATE admininfo SET telegram_username=\'{}\', area=\'{}\' WHERE telegram_id=\'{}\';".format(i['telegram_username'], i['area'], i['telegram_id']))
                logger.info(
                    "admin: %s update telegram_username: %s area: %s" %
                    (i['telegram_id'], i['telegram_username'],i['area']))

    def checkAdmin(self, telegram_id):
        _check = self.db.query(
            "SELECT telegram_id, area FROM admininfo WHERE telegram_id=\'{}\'"
            .format(telegram_id))
        _check_id = _check.getresult()
        if _check_id == []:
            logger.info("telegram_id: %s is not admin" %
                        telegram_id)
            return False
        else:
            logger.info("telegram_id: %s is admin" % telegram_id)
            return True

    def getAdminId(self, content):
        telegram_id = []
        for i in list(set(content['area'].replace(' ', '').split(','))):
            _check = self.db.query(
                "SELECT telegram_id FROM admininfo WHERE area=\'{}\'"
                .format(i.upper()))
            _check_id = _check.getresult()
            if len(_check_id) == 0:
                logger.info("telegram_id: {}, area {} doesn't existed"
                    .format(content['telegram_id'], content['area']))
            else:
                for j in _check_id:
                    telegram_id.append(j[0])
        return telegram_id

class dbControl(pushDB, creatTable, admin):
    pass


if __name__ == '__main__':
    from .parseCfg import parseCfg
    path = 'src/config.example.yml'
    config = parseCfg(path)
    db = dbControl(config)
    db.creat()
    content = {
        'area': 'T, b',
        'ingress_id': 'ArielAxionL',
        'other': 'Balthild',
        'telegram_id': '82814392',
        'telegram_username': 'ADA_Refactor'}
    db.push(content)
    db.creatAdmin()
    db.checkAdmin(content['telegram_id'])
    telegram_id = db.getAdminId(content)
    print(telegram_id)
