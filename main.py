# #!/usr/bin/env python
# # coding=utf-8
# '''Based on python-telegram-bot'''
#
# from telegram.ext import Updater
# from telegram.ext import CommandHandler
# from telegram.ext import MessageHandler
# from telegram.ext import Filters
# from telegram.ext import RegexHandler
# from telegram.ext import ConversationHandler
# from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
# from functools import wraps
# import logging
#
#
# logging.basicConfig(
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     level=logging.INFO)
# logger = logging.getLogger(__name__)
# LIST_OF_ADMINS = [11111111]  # Just for test.
# TUTORIALS = range(1)
# CHECK_DATA = range(1)
# CONTENT = range(1)
#
#
# def restricted(func):
#     @wraps(func)
#     def wrapped(bot, update, *args, **kwargs):
#         user_id = update.effective_user.id
#         if user_id not in LIST_OF_ADMINS:
#             print('Unauthorized access denied for {}.'.format(user_id))
#             return
#         return func(bot, update, *args, **kwargs)
#     return wrapped
#
#
# def start(bot, update):
#     user_id = update.effective_user.id
#     if user_id not in LIST_OF_ADMINS:
#         update.message.reply_text("""
# 生鱼忧患，死鱼安乐，欢迎加入蓝色咸鱼军~
# 你的 telegram id 是：%s
# (・ω・`| 使用 /help 查看教程
# (・ω・`| 使用 /join 填写表格""" % user_id)
#     else:
#         update.message.reply_text("""
# 欢迎管理员回来~
# (・ω・`| 使用 /help 查看教程
# (・ω・`| 使用 /check 查看表格""")
#
#
# def join(bot, update):
#     reply_keyboard = [['ingress_id', 'area', 'relationship']]
#     update.message.reply_text(
#         "Select the tags: ",
#         reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True))
#     return CONTENT
#
# def content(bot, update):
#     telegram_id = update.message.from_user['id']
#     telegram_username = update.message.from_user['username']
#
#
#
# def help(bot, update):
#     reply_keyboard = [['Summary', 'Ingress', 'Telegram', 'Website']]
#     update.message.reply_text(
#         '欢迎查看教程，教程分类如下：',
#         reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True))
#     return TUTORIALS
#
#
# def tutorials(bot, update):
#     if update.message.text == 'Summary':
#         update.message.reply_text(
#             'https://github.com/ResistanceCN/Tutorials')
#     if update.message.text == 'Ingress':
#         update.message.reply_text(
#             'https://github.com/ResistanceCN/Tutorials/tree/master/ingress')
#     if update.message.text == 'Telegram':
#         update.message.reply_text(
#             'https://github.com/ResistanceCN/Tutorials/tree/master/telegram')
#     if update.message.text == 'Website':
#         update.message.reply_text(
#             'https://github.com/ResistanceCN/Tutorials/tree/master/website')
#
#
# def cancel(bot, update):
#     user = update.message.from_user
#     user_id = update.effective_user.id
#     logger.info('%s (id: %s) canceled the conversation.' %
#                 (user.first_name, user_id))
#     update.message.reply_text('你已经是 dalao 了，快去和萌新打招呼吧~')
#
# @restricted
# def error(bot, update):
#     logger.warn('Update "%s" caused error "%s"' % (update, error))
#
#
# @restricted
# def check(bot, update):
#     '''Connect to sql.'''
#     reply_keyboard = [['Show_all', 'Check_update']]
#     update.message.reply_text(
#         '欢迎查看表格，查看命令如下：',
#         reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True))
#     return CHECK_DATA
#
#
# @restricted
# def check_data(bot, update):
#     if update.message.text == 'Show_all':
#         update.message.reply_text('下面是这个月的新人列表：\n ⁄(⁄ ⁄•⁄ω⁄•⁄ ⁄)⁄ 假装我是表')
#     if update.message.text == 'Check_update':
#         update.message.reply_text('已经没有可添加的新人了 ⁽⁽٩(๑˃̶͈̀ ᗨ ˂̶͈́)۶⁾⁾')
#
#
# def main():
#     updater = Updater(token='265836060:AAFUAYbxHfYgVbrOx8R3bOJMxPPBM-2IO_M')
#     dp = updater.dispatcher
#
#     join_conv_handler = ConversationHandler(
#         entry_points=[CommandHandler('join', join)],
#         states={
#             CONTENT: [RegexHandler(
#                 '^(ingress_id|area|relationship)$', content)]
#         },
#         fallbacks=[CommandHandler('cancel', cancel)]
#     )
#
#     help_conv_handler = ConversationHandler(
#         entry_points=[CommandHandler('help', help)],
#         states={
#             TUTORIALS: [RegexHandler(
#                 '^(Summary|Ingress|Telegram|Website)$', tutorials)]
#         },
#         fallbacks=[CommandHandler('cancel', cancel)]
#     )
#
#     check_conv_handler = ConversationHandler(
#         entry_points=[CommandHandler('check', check)],
#         states={
#             CHECK_DATA: [RegexHandler(
#                 '^(Check_update|Show_all)$', check_data)]
#         },
#         fallbacks=[CommandHandler('cancel', cancel)]
#     )
#
#     dp.add_handler(CommandHandler('start', start))
#     dp.add_handler(help_conv_handler)
#     dp.add_handler(check_conv_handler)
#     dp.add_handler(join_conv_handler)
#     dp.add_error_handler(error)
#     updater.start_polling()
#     updater.idle()
#
#
# if __name__ == '__main__':
#     main()
