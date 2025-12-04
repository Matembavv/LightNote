import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.error import TelegramError

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Токен из переменных окружения
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Проверка токена
if not TOKEN:
    logger.error("Токен не найден! Установите переменную TELEGRAM_BOT_TOKEN")
    exit(1)

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"Привет, {user.first_name}! Я бот, работающий на Render! 🚀\n"
        f"Просто отправь мне любое сообщение."
    )

# Ответ на текстовые сообщения
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    await update.message.reply_text(f"Вы написали: {text}")

# Команда /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Доступные команды:\n/start - Начать работу\n/help - Помощь")

# Обработчик ошибок
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Ошибка при обработке обновления {update}: {context.error}")

def main():
    try:
        # Создаем приложение с токеном
        application = Application.builder().token(TOKEN).build()
        
        # Регистрируем обработчики команд
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("help", help_command))
        
        # Регистрируем обработчик текстовых сообщений
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
        
        # Регистрируем обработчик ошибок
        application.add_error_handler(error_handler)
        
        logger.info("Бот запускается...")
        
        # Запускаем бота в режиме polling
        application.run_polling(
            allowed_updates=Update.ALL_TYPES,
            drop_pending_updates=True
        )
        
    except TelegramError as e:
        logger.error(f"Ошибка Telegram API: {e}")
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")

if __name__ == '__main__':
    main()
