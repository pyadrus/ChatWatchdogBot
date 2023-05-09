import configparser

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup

config = configparser.ConfigParser(empty_lines_in_values=False, allow_no_value=True)
# Считываем токен бота с файла config.ini
config.read("setting/config.ini")
bot_token = config.get('BOT_TOKEN', 'BOT_TOKEN')
time_del = config.get('TIME_DEL', 'TIME_DEL')

bot = Bot(token=bot_token)  # Инициализируем бота и диспетчер
dp = Dispatcher(bot, storage=MemoryStorage())


class AddAndDelBadWords(StatesGroup):
    """Создаем состояние для добавления плохих слов"""
    waiting_for_bad_word = State()
    waiting_for_check_word = State()
    del_for_bad_word = State()


