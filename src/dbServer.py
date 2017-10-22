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
            _check = cur.execute(
                "SELECT id FROM joininfo WHERE telegram_id=%s",
                (content['telegram_id'],))
            _check_id = cur.fetchall()

            # TODO: Verify the google account.
            if len(_check_id) == 0:
                cur.execute(
                    'INSERT INTO joininfo (ingress_id,telegram_id,telegram_username,area,other) VALUES (%s,%s,%s,%s,%s)',
                    (content['ingress_id'], content['telegram_id'],
                     content['telegram_username'], content['area'],
                     content['other'],))
            else:
                cur.execute("UPDATE joininfo SET ingress_id=%s, telegram_username=%s, area=%s, other=%s WHERE telegram_id=%s",
                            (content['ingress_id'], content['telegram_username'], content['area'], content['other'], content['telegram_id'],))
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
        """Creat admin info from config file."""
        with self.db.cursor() as cur:
            for i in self.config.admin():
                _check = cur.execute(
                    "SELECT telegram_id FROM admininfo WHERE telegram_id=%s",
                    (i['telegram_id'],))
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
        """Check user is admin or not."""
        with self.db.cursor() as cur:
            _check = cur.execute(
                "SELECT telegram_id FROM admininfo WHERE telegram_id=%s",
                (telegram_id,))
            _check_id = cur.fetchall()
            if _check_id == []:
                logger.info("telegram_id: %s is not admin" %
                            telegram_id)
                return False
            else:
                return True

    def getAdminId(self, content):
        """Get admin telegram_id."""
        telegram_id = []
        columns = ['telegram_id']

        with self.db.cursor() as cur:
            for i in list(set(content['area'].replace(' ', '').split(','))):
                if i != []:
                    _check = cur.execute(
                        "SELECT telegram_id FROM admininfo WHERE area ILIKE \'{}\'"
                        .format('%' + i.upper() + '%'))
                    for row in cur.fetchall():
                        if len(row) == 0:
                            logger.info(
                                "telegram_id: {}, area {} doesn't existed"
                                .format(content['telegram_id'], content['area']))
                            pass
                        else:
                            telegram_id.append(dict(zip(columns, row))['telegram_id'])
            return telegram_id

    def checkNew(self, area):
        """Check new form"""
        results = []
        with self.db.cursor() as cur:
            columns = ['ingress_id', 'telegram_id', 'telegram_username', 'area', 'other']
            _check = cur.execute(
                "SELECT ingress_id, telegram_id, telegram_username, \
                area, other FROM joininfo WHERE area ILIKE \'{}\' \
                ORDER BY created_time DESC LIMIT 3;".format(area))
            for row in cur.fetchall():
                if len(row) == 0:
                    pass
                else:
                    results.append(dict(zip(columns, row)))
            return results

class dbControl(pushDB, creatTable, admin):
    pass


if __name__ == '__main__':
    from parseCfg import parseCfg

    path = 'config.example.yml'
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
    print(db.checkNew('%B%'))
