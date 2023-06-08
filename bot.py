from telegram.ext import *
from telegram import *
import os

TOKEN = '6087048986:AAFSoEq1zJefaTgVv3sgUK6jAFYZOCLSu0Y'
PORT = int(os.environ.get('PORT', '8443'))

def echo_message(update, context):
    update.message.reply_text(f'{update.message.text}')


def main():
    updater = Updater(TOKEN, use_context=True)
    disp = updater.dispatcher
    disp.add_handler(MessageHandler(Filters.regex(r'.*'), echo_message))
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN,
                          webhook_url='https://telegram-bot-wedding.herokuapp.com/' + TOKEN)

    updater.idle()


if __name__ == '__main__':
    main()
