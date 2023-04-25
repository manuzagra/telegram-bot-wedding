import logging
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import ConversationHandler, filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes, InlineQueryHandler, PicklePersistence, CallbackQueryHandler


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG
)

logger = logging.getLogger()


# states
MAIN_OPTIONS, INTRO_NUMBER_SAVE_NAME_REQ_NUMBER, INTRO_NUMBER_SAVE_NUMBER, GUESS_GAME_REQ_ORDER, GUESS_GAME_INTRO_NUMBER, END = range(6)

# participants
PARTICIPANTS = ['Manuel', 'Alfonsito', 'Carlos Ropero', 'Xulo']

# texts
INTRO_NUMBERS = 'Introducir un número/letra que has conseguido'
GUESS_GAME = 'Jugar para adivinar el orden'


async def init(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    
    logger.debug(context.user_data.get('numbers', ''))

    if context.user_data.get('new_interaction', True):
        if not context.user_data.get('numbers', False):
            context.user_data['numbers'] = {p: '-' for p in PARTICIPANTS}
            context.user_data['numbers'] = {'Manuel': '1', 'Alfonsito': '2', 'Carlos Ropero': '3', 'Xulo': '4'}
        message = 'Bienvenido al juego de tu boda!!!\nPrimero tendrás que conseguir una serie de carácteres de los participantes en el juego, después tendrás que jugar a un juego para averiguar el orden.\n¿Qué quieres hacer?'
        context.user_data['new_interaction'] = False
    else:
        message = '¿Qué quieres hacer ahora?'
    
    logger.debug(context.user_data['numbers'])

    reply_keyboard = [
        [INTRO_NUMBERS],
        [GUESS_GAME],
        ['Salir'],
    ]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

    await update.message.reply_text(message, reply_markup=markup,)

    return MAIN_OPTIONS

async def intro_number_req_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    reply_keyboard = [[p] for p in PARTICIPANTS]

    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

    await update.message.reply_text(
        '¿De quién has conseguido el carácter?',
        reply_markup=markup,
    )
    return INTRO_NUMBER_SAVE_NAME_REQ_NUMBER

async def intro_number_save_name_req_number(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['numbers'][update.message.text] = -1
    context.user_data['last_person'] = update.message.text

    await update.message.reply_text('¿Qué carácter te ha dicho?')

    return INTRO_NUMBER_SAVE_NUMBER

async def intro_number_save_number(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['numbers'][context.user_data['last_person']] = update.message.text.upper()

    await update.message.reply_text('Guardado!!!\nEscribe /menu para volver al menu principal o /salir para acabar el juego.')

    return END

async def guess_number_intro_number(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    digits = ''.join(context.user_data['numbers'].values())

    await update.message.reply_text(f'Los caracteres guardados son los siguientes:\n{digits}\nEscríbelos en el orden que creas correcto.')

    return GUESS_GAME_REQ_ORDER
    

async def guess_number_check_number(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    truth = '1234'

    digits = ''.join(context.user_data['numbers'].values())

    for d in update.message.text:
        if d not in digits:
            message = 'Hay uno o más carácteres incorrectos, por favor usa solo los carácteres que te ha dado la gente.\n¿Quieres intentarlo otra vez ( /si o /no)?'

            await update.message.reply_text(message)

            return GUESS_GAME_INTRO_NUMBER

    easy_mode = False

    if easy_mode:

        message = ''
        for i in range(min(len(update.message.text), len(truth))):
            message += 'o' if update.message.text[i].upper() == truth[i] else 'x'

        if 'x' in message:
            message = str(update.message.text) + '\n' + message + '\n¿Quieres intentarlo otra vez ( /si o /no)?'

            await update.message.reply_text(message)

            return GUESS_GAME_INTRO_NUMBER
        else:
            message = str(update.message.text) + '\n' + message + '\nCORRECTO!!!\nYa tienes el código!!! Escribe /salir para finalizar o /instrucciones para obtener instrucciones de que hacer con el código que acabas de conseguir.'

            await update.message.reply_text(message)

            return END
    else:
        correct_position = 0
        for i in range(min(len(update.message.text), len(truth))):
            correct_position += 1 * (update.message.text[i].upper() == truth[i])

        if correct_position < len(truth):
            message = f'{correct_position} carácteres están en la posicion correcta.\n¿Quieres intentarlo otra vez ( /si o /no)?'

            await update.message.reply_text(message)

            return GUESS_GAME_INTRO_NUMBER
        else:
            message = '\nCORRECTO!!!\nYa tienes el código!!! Escribe /salir para finalizar o /instrucciones para obtener instrucciones de que hacer con el código que acabas de conseguir.'

            await update.message.reply_text(message)

            return END

async def instructions(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    INSTRUCTIONS = 'Here you would see the instructions'

    await update.message.reply_text(INSTRUCTIONS + '\n\nPara volver a comenzar escribe /start.')

    return ConversationHandler.END

async def end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.debug(context.user_data['numbers'])

    context.user_data['new_interaction'] = True

    await update.message.reply_text('Para volver a comenzar escribe /start.')

    return ConversationHandler.END


def get_state_machine():
    handler = ConversationHandler(
        entry_points=[CommandHandler('start', init), MessageHandler(filters.TEXT, init)],
        states={
            MAIN_OPTIONS: [
                MessageHandler(filters.Regex(f'^{INTRO_NUMBERS}'), intro_number_req_name),
                MessageHandler(filters.Regex(f'^{GUESS_GAME}'), guess_number_intro_number)
            ],
            INTRO_NUMBER_SAVE_NAME_REQ_NUMBER: [MessageHandler(filters.TEXT, intro_number_save_name_req_number)],
            INTRO_NUMBER_SAVE_NUMBER: [MessageHandler(filters.TEXT, intro_number_save_number)],
            GUESS_GAME_INTRO_NUMBER: [MessageHandler(filters.Regex(f'^No|no$'), init), MessageHandler(filters.TEXT & ~filters.Regex(f'^No|no$'), guess_number_intro_number)],
            GUESS_GAME_REQ_ORDER: [MessageHandler(filters.TEXT, guess_number_check_number)],
            END: [CommandHandler('menu', init), CommandHandler('salir', end), CommandHandler('instrucciones', instructions), MessageHandler(filters.TEXT, init)],
        },
        fallbacks=[MessageHandler(filters.Regex('^[Ss]alir$'), end), MessageHandler(filters.Regex('^[Mm]enu|[Ss]tart$'), init)],
    )

    return handler


if __name__ == '__main__':

    TOKEN = '6087048986:AAFSoEq1zJefaTgVv3sgUK6jAFYZOCLSu0Y'

    persistence = PicklePersistence(filepath='/workspaces/get_the_password_bot/persistent_data/bot_data.pkl')
    application = ApplicationBuilder().token('6087048986:AAFSoEq1zJefaTgVv3sgUK6jAFYZOCLSu0Y').persistence(persistence).build()

    application.add_handler(get_state_machine())

    application.run_polling()