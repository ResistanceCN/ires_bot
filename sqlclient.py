#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pg import DB
import yaml
import logging
import logging.config
import sys

# LOG_FILENAME = 'logging.conf'
# LOG_CONTENT_NAME = 'pg_log'

class Push:
    def __init__(self, ingress_id, telegram_username, area, **kwrags):
        self.ingress_id = ingress_id
        self.telegram_username = telegram_username
        self.area = area

    def pushToSql(self):
        check = db.query("SELECT id FROM joininfo WHERE ingress_id=\'{}\'".format(self.ingress_id))
        check_id = check.getresult()
        if len(check_id) == 0:
            db.insert('joininfo', ingress_id=self.ingress_id, telegram_username=self.telegram_username, area=self.area)
        else:
            db.query("UPDATE joininfo SET area=\'{}\' WHERE ingress_id=\'{}\'".format(self.area, self.ingress_id))

    def pushToAdmin(self):
        print("ingress_id: %s \ntelegram_username: @%s \narea: %s" %(self.ingress_id, self.telegram_username, self.area))
        pass

# def log_init(log_config_filename, logname):
#   logging.config.fileConfig(log_config_filename)
#   logger = logging.getLogger(logname)
#   return logger

def creatTable(db):
    if 'public.joininfo' not in db.get_tables():
        status = "Creat"
        db.query('''CREATE TABLE joininfo (
        id SERIAL PRIMARY KEY,
        ingress_id VARCHAR(35) NOT NULL,
        telegram_username VARCHAR(35) NOT NULL,
        area VARCHAR(2) NOT NULL,
        relationship VARCHAR(35),
        created_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP)''')
        # TODO: Dynamically create data tables
    else:
        status = "Existed"
        pass
    return status

def parse(path):
    try:
        with open(path, 'r+') as f:
            content = yaml.load(f)
        return content
    except FileNotFoundError:
        print("No such file or directory: " + path)
        sys.exit(1)
    return content

path = 'example.config.yml' # TODO: check the config file
config = parse(path)
sql = config['postgres']

try:
    db = DB(
        dbname=sql['database'], user=sql['user'],
        passwd=sql['password'], host=sql['host'])
    # pgdb_logger.debug("operate postgresql table product...")
except ConnectionError:
    print("conntect postgre database failed")
    sys.exit(1)
    # print(e.args[0])
    # pgdb_logger.error("conntect postgre database failed, ret = %s" % e.args[0])

_creat_table_status = creatTable(db)
# print(_creat_table_status)

content = Push("ArielAxionL", "ADA_Refactor", "T")
content.pushToSql()
content.pushToAdmin()

content = Push("Balthild", "Balthildires", "T")
content.pushToSql()
content.pushToAdmin()

content = Push("ArielAxionL", "ADA_Refactor", "E")
content.pushToSql()
content.pushToAdmin()

content = Push("DrielAxionL", "ADA_Refactor", "E")
content.pushToSql()
content.pushToAdmin()
# a = Push('1', 'aaaaa')
