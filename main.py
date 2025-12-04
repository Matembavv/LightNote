import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Токен вашего бота (замените на свой)
TOKEN = "8385518515:AAGC1PhOgdkj2HQ72pCgHW9307LEprYZnV4"


# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отправляет приветственное сообщение при команде /start"""
    user = update.effective_user
    await update.message.reply_text(
        f"Привет, {user.first_name}! Я простой бот, который отвечает на твои сообщения.\n"
        "Просто напиши мне что-нибудь, и я отвечу!"
    )


# Команда /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отправляет справку"""
    await update.message.reply_text(
        "Я простой бот-эхо. Просто напиши мне любое сообщение, и я отвечу!"
    )


# Обработка текстовых сообщений
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Повторяет сообщение пользователя с небольшим изменением"""
    user_message = update.message.text
    response = f"Вы написали: \"{user_message}\"\n\nЯ получил ваше сообщение! 👍"
    await update.message.reply_text(response)


# Обработка не-текстовых сообщений (фото, стикеры и т.д.)
async def handle_other_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатывает медиафайлы"""
    if update.message.photo:
        await update.message.reply_text("Классное фото! 📷")
    elif update.message.sticker:
        await update.message.reply_text("Интересный стикер! 😊")
    elif update.message.voice:
        await update.message.reply_text("Я получил ваше голосовое сообщение! 🎤")
    elif update.message.document:
        await update.message.reply_text("Документ получен! 📄")
    else:
        await update.message.reply_text("Я получил ваше сообщение! 😊")


def main():
    """Запуск бота"""
    # Создаем приложение
    application = Application.builder().token(TOKEN).build()

    # Регистрируем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # Регистрируем обработчик текстовых сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Регистрируем обработчик для всех остальных типов сообщений
    application.add_handler(MessageHandler(
        filters.ALL & ~filters.TEXT & ~filters.COMMAND,
        handle_other_messages
    ))

    # Запускаем бота
    print("Бот запущен...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
