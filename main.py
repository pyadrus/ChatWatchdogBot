from aiogram import executor
from loguru import logger

from handlers.admin_handlers import admin_handlers
from system.dispatcher import dp

logger.add("settings/log/log.log", rotation="1 MB", compression="zip")


def main():
    executor.start_polling(dp, skip_updates=True)
    admin_handlers()


if __name__ == '__main__':
    try:
        main()  # Запуск бота
    except Exception as e:
        logger.exception(e)
        print("[bold red][!] Произошла ошибка, для подробного изучения проблемы просмотрите файл log.log")
