"""Based on python-telegram-bot"""
# coding=utf-8
#!/usr/bin/env python

from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters
from functools import wraps
import logging


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
LIST_OF_ADMINS = [11111111]  # Just for test.


def restricted(func):
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in LIST_OF_ADMINS:
            print("Unauthorized access denied for {}.".format(user_id))
            return
        return func(bot, update, *args, **kwargs)
    return wrapped


def start(bot, update):
    update.message.reply_text("It's time to move. Join Resistance!")
    update.message.reply_text("Your id is %s" % update.effective_user.id)
    pass


def help(bot, update):
    update.message.reply_text("what can I do for you? If you are not the admins, please tell your user_id to @ADA_Refactor.")


@restricted
def echo(bot, update):
    """Connect to sql."""
    update.message.reply_text(update.message.text)


@restricted
def error(bot, update):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    updater = Updater(token='TOKEN')
    dp = updater.dispatcher()
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(MessageHandler(Filters.text, echo))
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle


if __name__ == '__main__':
    main()
