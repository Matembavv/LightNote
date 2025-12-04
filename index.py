import json
import os
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters

TOKEN = os.environ.get('8385518515:AAGC1PhOgdkj2HQ72pCgHW9307LEprYZnV4')
bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot, None, workers=0)


def start(update, context):
    update.message.reply_text('Привет! Я работаю в Яндекс Облаке!')


def echo(update, context):
    update.message.reply_text(update.message.text)


# Регистрируем обработчики
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))


def handler(event, context):
    """Точка входа для Cloud Functions."""
    try:
        # Обновление от Telegram приходит в теле запроса
        update = Update.de_json(json.loads(event['body']), bot)
        dispatcher.process_update(update)
    except Exception as e:
        print(f"Error: {e}")

    return {
        'statusCode': 200,
        'body': 'OK',
    }