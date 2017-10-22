#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

"""
This bot is used to collect agents information as a tables.
"""

from telegram import ReplyKeyboardMarkup
from telegram import ReplyKeyboardRemove
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters
from telegram.ext import RegexHandler
from telegram.ext import ConversationHandler
from parseCfg import parseCfg
from dbServer import dbControl
from cacheServer import cacheControl
from functools import wraps
import telegram
import logging

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)

LANG, INGRESS_ID, AREA, OTHER, PUSH, TUTORIALS = range(6)


def restricted(func):
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        content['user_id'] = update.effective_user.id
        if not db.checkAdmin(content):
            logger.info('Unauthorized access denied for {}.'.format(content['user_id']))
            return
        return func(bot, update, *args, **kwargs)

    return wrapped


def start(bot, update):
    """Start the bot and check admin."""
    telegram_id = update.effective_user.id
    if db.checkAdmin(telegram_id):
        update.message.reply_text("""
欢迎管理员回来~
(・ω・`| 使用 /help 查看教程
(・ω・`| 使用 /check 查看表格""")
    else:
        update.message.reply_text("""
生鱼忧患，死鱼安乐，欢迎加入蓝色咸鱼军~
你的 telegram id 是：%s
(・ω・`| 使用 /help 查看教程
(・ω・`| 使用 /join 填写表格
(・ω・`| 使用 /cancel 取消填写
""" % telegram_id)


def help(bot, update):
    """Get the help."""
    reply_keyboard = [['Summary', 'Ingress', 'Telegram', 'Website']]
    update.message.reply_text(
        '欢迎查看教程，教程分类如下：',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, resize_keyboard=True))
    return TUTORIALS


def tutorials(bot, update):
    """Show tutorial articles."""
    # TODO: Connect to wiki page.
    if update.message.text == 'Summary':
        update.message.reply_text(
            'https://github.com/ResistanceCN/Tutorials',
            reply_markup=ReplyKeyboardRemove())
    if update.message.text == 'Ingress':
        update.message.reply_text(
            'https://github.com/ResistanceCN/Tutorials/tree/master/ingress',
            reply_markup=ReplyKeyboardRemove())
    if update.message.text == 'Telegram':
        update.message.reply_text(
            'https://github.com/ResistanceCN/Tutorials/tree/master/telegram',
            reply_markup=ReplyKeyboardRemove())
    if update.message.text == 'Website':
        update.message.reply_text(
            'https://github.com/ResistanceCN/Tutorials/tree/master/website',
            reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def join(bot, update):
    """Start to fill in the form."""
    reply_keyboard = [['English', 'Chinese']]
    update.message.reply_text(
        "Choose language",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True))
    return LANG


def language(bot, update):
    """Get env language."""
    user = update.message.from_user
    cache.hashset(user.id, language=update.message.text)
    logger.info("Language of %s: %s" % (user.id, update.message.text))

    if update.message.text == 'English':
        update.message.reply_text(
            "Welcome to join us \n Enter your ingress_id: ",
            reply_markup=ReplyKeyboardRemove())
    elif update.message.text == 'Chinese':
        update.message.reply_text("欢迎加入我们! 请输入你的 Ingress_id: ")
    return INGRESS_ID


def ingress_id(bot, update):
    "Get agent's ingress_id."
    user = update.message.from_user
    ingress_id = update.message.text
    if "@" in ingress_id:
        ingress_id = ingress_id.replace('@', '')
    cache.hashset(user.id, ingress_id=ingress_id)
    logger.info("Ingress_id of %s: %s" % (user.id, ingress_id))
    language = cache.hashget(user.id, 'language')

    if language == 'English':
        update.message.reply_text(
            'Map here: https://google.map.com&token \n\
            Enter the area tag, multiple area are separated by \',\'')
    if language == 'Chinese':
        update.message.reply_text(
            '区域地图: https://google.map.com&token \n\
            输入你所在的区域编号，多个区域请以英文逗号分隔')
    return AREA


def location(bot, update):
    """Get the agent's area."""
    user = update.message.from_user
    cache.hashset(user.id, area=update.message.text)
    logger.info("Location of %s: %s" % (user.id, update.message.text))
    language = cache.hashget(user.id, 'language')

    if language == 'English':
        update.message.reply_text(
            'You may already know some players, please enter their names')
    if language == 'Chinese':
        update.message.reply_text('你可能已经认识一些玩家，请输入他们的名字')
    return OTHER


def other(bot, update):
    user = update.message.from_user
    cache.hashset(user.id, other=update.message.text)
    logger.info("Other players of %s: %s" % (user.id, update.message.text))

    str_tmp = ''
    for key, value in cache.hashgetall(user.id).items():
        str_tmp += key + ':' + value + '\n'
    update.message.reply_text(str_tmp)

    language = cache.hashget(user.id, 'language')
    if language == 'Chinese':
        reply_keyboard = [['是', '否']]
        update.message.reply_text(
            '确认是否提交信息，/cancel 退出填表',
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True))

    if language == 'English':
        reply_keyboard = [['Yes', 'No']]
        update.message.reply_text(
            'Confirm whether to submit a message or /cancel ',
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True))

    return PUSH


def push(bot, update):
    user = update.message.from_user
    cache.hashset(user.id, telegram_username=user.username)
    logger.info("%s's message push status: %s" %
                (user.id, update.message.text))
    pushstat = update.message.text
    language = cache.hashget(user.id, 'language')

    if pushstat == "否":
        update.message.reply_text(
            '已取消', reply_markup=ReplyKeyboardRemove())
    elif pushstat == "No":
        update.message.reply_text(
            'Cancel success', reply_markup=ReplyKeyboardRemove())
    elif pushstat == "Yes" or "是":
        content = cache.hashgetall(user.id)
        content['telegram_id'] = user.id
        db.push(content)  # push to database
        cache.hashclean(user.id)  # clean cache
        telegram_id = db.getAdminId(content)
        if telegram_id == []:
            if language == 'English':
                update.message.reply_text(
                    "Area does not exist, /join again",
                    reply_markup=ReplyKeyboardRemove())
            elif language == 'Chinese':
                update.message.reply_text(
                    "区域不存在，请重新 /join",
                    reply_markup=ReplyKeyboardRemove())
        else:
            if language == 'English':
                update.message.reply_text(
                    'Submit success!', reply_markup=ReplyKeyboardRemove())
            if language == 'Chinese':
                update.message.reply_text(
                    '提交成功', reply_markup=ReplyKeyboardRemove())
            for i in telegram_id:
                bot.send_message(
                    i,
                    text="ingress_id: {}\ntelegram_username: {}\narea: {}\nother: {}"
                        .format(
                        content['ingress_id'],
                        "@" + content['telegram_username'],
                        content['area'],
                        content['other']))
    return ConversationHandler.END


# @restricted
# def check(bot, update):
#     # TODO: Get the unchecked info from database.


def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation." % user.id)
    if language == 'English':
        update.message.reply_text(
            'Has been out of state',
            reply_markup=ReplyKeyboardRemove())
    if language == 'Chinese':
        update.message.reply_text(
            '已退出状态',
            reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"' % (update, error))


def main(path):
    db.creat()  # creat tables
    db.creatAdmin()
    updater = Updater(config.token())
    dp = updater.dispatcher
    help_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('help', help)],
        states={
            TUTORIALS: [RegexHandler(
                '^(Summary|Ingress|Telegram|Website)$', tutorials)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    join_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('join', join)],
        states={
            LANG: [RegexHandler('^(English|Chinese)$', language)],
            INGRESS_ID: [MessageHandler(Filters.text, ingress_id)],
            AREA: [MessageHandler(Filters.text, location)],
            OTHER: [MessageHandler(Filters.text, other)],
            PUSH: [RegexHandler('^(Yes|No|是|否)$', push)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(help_conv_handler)
    dp.add_handler(join_conv_handler)
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    path = '../config.example.yml'
    global cache, config, db, bot
    # TODO: Resolve variable conflicts
    content = {}
    config = parseCfg(path)
    db = dbControl(config)
    cache = cacheControl(config)
    main(path)
