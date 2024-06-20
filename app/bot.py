from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, CallbackQueryHandler
import requests

# Импорт токена из config.py
from config import TELEGRAM_TOKEN


# Использование токена
TOKEN = TELEGRAM_TOKEN


def get_url(link):
    contents = requests.get(link).json()
    url = contents[0]['url']
    return url


async def dog(update: Update, context: CallbackContext) -> None:
    url = get_url('https://api.thedogapi.com/v1/images/search')
    await update.message.reply_photo(photo=url)


async def cat(update: Update, context: CallbackContext) -> None:
    url = get_url('https://api.thecatapi.com/v1/images/search')
    await update.message.reply_photo(photo=url)


async def start(update: Update, context: CallbackContext) -> None:
    # Создаем inline keyboard
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("котики!!", callback_data='button1'),
            InlineKeyboardButton("сабачьки!!", callback_data='button2'),
        ]
    ])

    await update.message.reply_text('Выберите опцию:', reply_markup=keyboard)


async def button_click(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    # Обработка нажатия кнопок
    if query.data == 'button1':
        url = get_url('https://api.thecatapi.com/v1/images/search')
        await context.bot.send_photo(chat_id=query.message.chat_id, photo=url)
    elif query.data == 'button2':
        url = get_url('https://api.thedogapi.com/v1/images/search')
        await context.bot.send_photo(chat_id=query.message.chat_id, photo=url)

async def pizda(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('1')
    await update.message.reply_text('4')
    await update.message.reply_text('8')
    await update.message.reply_text('8')


async def echo(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(update.message.text)


def main():
    application = Application.builder().token(TOKEN).build()

    # Обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("pizda", pizda))
    application.add_handler(CommandHandler('dog', dog))
    application.add_handler(CommandHandler('cat', cat))

    # Обработчик сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Обработчик нажатия кнопок в inline keyboard
    application.add_handler(CallbackQueryHandler(button_click))

    application.run_polling()


if __name__ == '__main__':
    main()
