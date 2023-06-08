import os
import logging
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes, InlineQueryHandler, PicklePersistence


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)

TOKEN = '6087048986:AAFSoEq1zJefaTgVv3sgUK6jAFYZOCLSu0Y'
PORT = int(os.environ.get('PORT', '8443'))


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['caps_number'] = 0
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['caps_number'] += 1
    text_caps = ' '.join(context.args).upper()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

async def inline_caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query
    if not query:
        return
    results = []
    results.append(
        InlineQueryResultArticle(
            id=query.upper(),
            title='Caps',
            input_message_content=InputTextMessageContent(query.upper())
        )
    )
    await context.bot.answer_inline_query(update.inline_query.id, results)

async def ncaps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"You used caps {context.user_data['caps_number']} times.")

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")



if __name__ == '__main__':

    persistence = PicklePersistence(filepath="/workspaces/get_the_password_bot/persistent_data/data.pkl")
    application = ApplicationBuilder().token('6087048986:AAFSoEq1zJefaTgVv3sgUK6jAFYZOCLSu0Y').persistence(persistence).build()
    

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    application.add_handler(echo_handler)

    caps_handler = CommandHandler('caps', caps)
    application.add_handler(caps_handler)

    inline_caps_handler = InlineQueryHandler(inline_caps)
    application.add_handler(inline_caps_handler)

    ncaps_handler = CommandHandler('ncaps', ncaps)
    application.add_handler(ncaps_handler)

    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    application.add_handler(unknown_handler)

    application.run_webhook(
        listen="0.0.0.0",
        port=int(PORT),
        url_path=TOKEN,
        webhook_url='https://telegram-bot-wedding.herokuapp.com/' + TOKEN
    )