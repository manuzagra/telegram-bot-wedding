import logging
from telegram.ext import *
from telegram import *
import os





# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

TOKEN = '6087048986:AAFSoEq1zJefaTgVv3sgUK6jAFYZOCLSu0Y'
PORT = int(os.environ.get('PORT', '8443'))


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')

def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')

def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    application = ApplicationBuilder().token('6087048986:AAFSoEq1zJefaTgVv3sgUK6jAFYZOCLSu0Y').build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.text, echo))

    # log all errors
    application.add_error_handler(error)

    # Start the Bot
    application.run_webhook(
        listen="0.0.0.0",
        port=int(PORT),
        url_path=TOKEN,
        webhook_url='https://telegram-bot-wedding.herokuapp.com/' + TOKEN
    )

if __name__ == '__main__':
    main()
