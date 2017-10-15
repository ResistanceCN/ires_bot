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
import logging

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

logger = logging.getLogger(__name__)

LANG, INGRESS_ID, AREA, RELATIONSHIP, PUSH, TUTORIALS = range(6)

LIST_OF_ADMINS = [11111111]


def start(bot, update):
    user_id = update.effective_user.id
    if user_id not in LIST_OF_ADMINS:
        update.message.reply_text("""
生鱼忧患，死鱼安乐，欢迎加入蓝色咸鱼军~
你的 telegram id 是：%s
(・ω・`| 使用 /help 查看教程
(・ω・`| 使用 /join 填写表格""" % user_id)
    else:
        update.message.reply_text("""
欢迎管理员回来~
(・ω・`| 使用 /help 查看教程
(・ω・`| 使用 /check 查看表格""")

def help(bot, update):
    reply_keyboard = [['Summary', 'Ingress', 'Telegram', 'Website']]
    update.message.reply_text(
        '欢迎查看教程，教程分类如下：',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, resize_keyboard=True))
    return TUTORIALS

def tutorials(bot, update):
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
    reply_keyboard = [['English', 'Chinese']]
    update.message.reply_text(
        "Choose language",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True))
    return LANG


def get_language(bot, update):
    user = update.message.from_user
    logger.info("Language of %s: %s" % (user.id, update.message.text))
    global language
    language = update.message.text
    if update.message.text == 'English':
        update.message.reply_text(
            "Welcome to join us \n Enter your ingress_id: ",
            reply_markup=ReplyKeyboardRemove())
    elif update.message.text == 'Chinese':
        update.message.reply_text("欢迎加入我们! 请输入你的 Ingress_id: ")
    return INGRESS_ID


def get_ingress_id(bot, update):
    user = update.message.from_user
    ingress_id = update.message.text
    logger.info("Ingress_id of %s: %s" % (user.id, ingress_id))
    if language == 'English':
        update.message.reply_text(
            'Map here: https://google.map.com&token \nEnter the area tag:')
    if language == 'Chinese':
        update.message.reply_text(
            '区域地图: https://google.map.com&token \n输入你所在的区域编号')
    return AREA

def get_location(bot, update):
    user = update.message.from_user
    area = update.message.text
    logger.info("Location of %s: %s" % (user.id, area))
    if language == 'English':
        update.message.reply_text(
            'You may already know some players, please enter their names')
    if language == 'Chinese':
        update.message.reply_text('你可能已经认识一些玩家，请输入他们的名字')
    return RELATIONSHIP

def get_relationship(bot, update):
    user = update.message.from_user
    relationship = update.message.text
    logger.info("Other players of %s: %s" % (user.id, update.message.text))
    if language == 'Chinese':
        reply_keyboard = [['是', '否']]
        update.message.reply_text(
            '确认是否提交信息',
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True))

    if language == 'English':
        reply_keyboard = [['Yes', 'No']]
        update.message.reply_text(
            'Confirm whether to submit a message',
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True))

    return PUSH

def push(bot, update):
    user = update.message.from_user
    pushstat = update.message.text
    print(language)
    print(pushstat)
    logger.info("%s's message push status: %s" % (user.id, update.message.text))

    if language == "Chinese":
        if pushstat == "是":
            update.message.reply_text(
                '提交成功', reply_markup=ReplyKeyboardRemove())
        elif pushstat == "否":
            update.message.reply_text(
                '已取消', reply_markup=ReplyKeyboardRemove())

    if language == "English":
        if pushstat == "Yes":
            update.message.reply_text(
                'push success', reply_markup=ReplyKeyboardRemove())
        elif pushstat == "No":
            update.message.reply_text(
                'cancel success', reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

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
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    updater = Updater("265836060:AAFUAYbxHfYgVbrOx8R3bOJMxPPBM-2IO_M")

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
            LANG: [RegexHandler('^(English|Chinese)$', get_language)],

            INGRESS_ID: [MessageHandler(Filters.text, get_ingress_id)],

            AREA: [MessageHandler(Filters.text, get_location)],

            RELATIONSHIP: [MessageHandler(Filters.text, get_relationship)],

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
    main()
