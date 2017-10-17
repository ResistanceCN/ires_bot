#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from parseConfig import psqlCfg, tgBotCfg
from pushServer import creatTable
from pg import DB
import logging
import logging.config

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)

def main():
    path = 'src/example.config.yml'

    # Get the config from file
    try:
        config = parseConfig(path)
    except:
        logger.info("Parse config file failed")

    # Connect to database
    try:
        db = DB(
            dbname=config.database(), user=config.user(),
            passwd=config.password(), host=config.host())
    except ConnectionError:
        logger.info("conntect postgre database failed")
        sys.exit(1)

    # Check table status, if table doesn't existed, creat it
    _creat_table_status = creatTable(db, sqlcfg.admininfo())
    logger.info("admininfo table status: %s" % _creat_table_status)

    _creat_table_status = creatTable(db, sqlcfg.index())
    logger.info("joininfo table status: %s" % _creat_table_status)

    # Get the telegram bot config from file


    # run the telegram bot

if __name__ == '__main__':
    main()
