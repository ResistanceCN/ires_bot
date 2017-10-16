#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pg import DB
from parse import (PsqlCfg, TgBot)
import yaml
import logging
import logging.config
import sys

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)

class Push:
    def __init__(self, ingress_id, telegram_id ,telegram_username, area, *args):
        self.ingress_id = ingress_id
        self.telegram_id = telegram_id
        self.telegram_username = telegram_username
        self.area = area
        self.other = []
        for arg in args:
            self.other.append(arg)

    def pushToSql(self):
        check = db.query("SELECT id FROM joininfo WHERE ingress_id=\'{}\'".format(self.ingress_id))
        check_id = check.getresult()
        if len(check_id) == 0:
            db.insert('joininfo', ingress_id=self.ingress_id, telegram_id=self.telegram_id ,telegram_username=self.telegram_username, area=self.area, other=self.other)
        else:
            db.query("UPDATE joininfo SET telegram_username=\'{}\' area=\'{}\' other=\'{}\' WHERE ingress_id=\'{}\'".format(self.telegram_username, self.area, self.other, self.ingress_id))

    def pushToAdmin(self):
        logger.info("ingress_id: %s \ntelegram_username: @%s \narea: %s" %(self.ingress_id, self.telegram_username, self.area))
        pass
    # TODO: select telegram_id, area from admins_info

def creatTable(db, index):
    if 'public.joininfo' not in db.get_tables():
        status = "Creat"
        db.query(index)
    else:
        status = "Existed"
        pass
    return status

if __name__ == '__main__':
    path = 'src/example.config.yml' # TODO: check the config file
    sqlcfg = PsqlCfg(path)

    try:
        db = DB(
            dbname=sqlcfg.database(), user=sqlcfg.user(),
            passwd=sqlcfg.password(), host=sqlcfg.host())
    except ConnectionError:
        logger.info("conntect postgre database failed")
        sys.exit(1)

    print(sqlcfg.adinfo())
    _creat_table_status = creatTable(db, sqlcfg.adinfo())
    logger.info("adinfo table status: %s" % _creat_table_status)

    _creat_table_status = creatTable(db, sqlcfg.index())
    logger.info("joininfo table status: %s" % _creat_table_status)

    content = Push("ArielAxionL", 11111111, "ADA_Refactor", "T", "relationship: Balthild", "bike: yes")
    content.pushToSql()
    content.pushToAdmin()

    content = Push("BrielAxionL", 11111111, "ADA_Refactor", "T", "relationship: Balthild", "bike: yes")
    content.pushToSql()
    content.pushToAdmin()
