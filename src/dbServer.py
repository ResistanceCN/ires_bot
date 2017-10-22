#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pg import InternalError
from pgdb import connect as DB
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
                database=config.database(), user=config.user(),
                password=config.password(), host=config.host())
        except InternalError:
            logger.info("conntecting postgresql service failed")
            sys.exit(1)

    def creat(self):
        with self.db.cursor() as cur:
            logger.info('Creating joininfo and adminifo table')
            cur.execute(self.config.joininfo_table())
            cur.execute(self.config.admininfo_table())
            self.db.commit()


class pushDB():
    def __init__(self, config):
        self.config = config
        try:
            self.db = DB(
                database=config.database(), user=config.user(),
                password=config.password(), host=config.host())
        except InternalError:
            logger.info("conntect postgre db failed")
            sys.exit(1)

    def push(self, content):
        with self.db.cursor() as cur:
            _check = cur.execute("SELECT id FROM joininfo WHERE ingress_id=%s", (content['ingress_id'],))
            _check_id = cur.fetchall()
            if len(_check_id) == 0:
                cur.execute(
                    'INSERT INTO joininfo (ingress_id,telegram_id,telegram_username,area,other) VALUES (%s,%s,%s,%s,%s)',
                    (content['ingress_id'], content['telegram_id'],
                     content['telegram_username'], content['area'],
                     content['other'],))
            else:
                cur.execute("UPDATE joininfo SET telegram_username=%s, area=%s, other=%s WHERE ingress_id=%s",
                            (content['telegram_username'], content['area'], content['other'], content['ingress_id'],))
            self.db.commit()


class admin():
    def __init__(self, config):
        self.config = config
        try:
            self.db = DB(
                dbname=config.database(), user=config.user(),
                passwd=config.password(), host=config.host())
        except InternalError:
            logger.info("conntect postgre db failed")
            sys.exit(1)

    def creatAdmin(self):
        with self.db.cursor() as cur:
            for i in self.config.admin():
                _check = cur.execute("SELECT telegram_id FROM admininfo WHERE telegram_id=%s", (i['telegram_id'],))
                _check_id = cur.fetchall()
                if len(_check_id) == 0:
                    cur.execute(
                        'INSERT INTO admininfo (telegram_id,telegram_username,area) VALUES (%s,%s,%s)',
                        (i['telegram_id'], i['telegram_username'], i['area'],))
                    logger.info("add admin member: %s" % i)
                else:
                    cur.execute(
                        "UPDATE admininfo SET telegram_username=%s, area=%s WHERE telegram_id=%s",
                        (i['telegram_username'], i['area'], i['telegram_id'],))
                    logger.info(
                        "admin: %s update telegram_username: %s area: %s" %
                        (i['telegram_id'], i['telegram_username'], i['area']))
            self.db.commit()

    def checkAdmin(self, telegram_id):
        with self.db.cursor() as cur:
            _check = cur.execute("SELECT telegram_id, area FROM admininfo WHERE telegram_id=%s", (telegram_id,))
            _check_id = cur.fetchall()
            if _check_id == []:
                logger.info("telegram_id: %s is not admin" %
                            telegram_id)
                return False
            else:
                logger.info("telegram_id: %s is admin" % telegram_id)
                return True

    def getAdminId(self, content):
        telegram_id = []
        with self.db.cursor() as cur:
            for i in list(set(content['area'].replace(' ', '').split(','))):
                _check = cur.execute("SELECT telegram_id FROM admininfo WHERE area=%s", (i.upper(),))
                _check_id = cur.fetchall()
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
    from parseCfg import parseCfg

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
