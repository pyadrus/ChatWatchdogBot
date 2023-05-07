import sqlite3
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode

# Установите ваш токен Telegram
BOT_TOKEN = '6030769434:AAH6I8EolvOSpBQppNv1wtu91d1sD7GPeDs'

# Инициализируем бота и диспетчер
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

# Инициализируем базу данных sqlite
conn = sqlite3.connect('bad_words.db')
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS bad_words (id INTEGER PRIMARY KEY AUTOINCREMENT, word TEXT)')
conn.commit()


# Создаем состояние для добавления плохих слов
class AddBadWords(StatesGroup):
    waiting_for_bad_word = State()


# Обработчик команды /add_bad
@dp.message_handler(Command('add_bad'))
async def cmd_add_bad(message: types.Message):
    await message.answer('Введите слово, которое нужно добавить в список плохих слов:')
    # Переходим в состояние ожидания плохого слова
    await AddBadWords.waiting_for_bad_word.set()


# Обработчик текстовых сообщений в состоянии ожидания плохого слова
@dp.message_handler(state=AddBadWords.waiting_for_bad_word)
async def process_bad_word(message: types.Message, state: FSMContext):
    # Получаем слово от пользователя
    bad_word = message.text.strip().lower()

    # Добавляем слово в базу данных sqlite
    cursor.execute('INSERT INTO bad_words (word) VALUES (?)', (bad_word,))
    conn.commit()

    # Выводим сообщение об успешном добавлении слова
    await message.reply(f'Слово "{bad_word}" успешно добавлено в список плохих слов.', parse_mode=ParseMode.HTML)

    # Сбрасываем состояние
    await state.finish()


if __name__ == '__main__':
    # Запускаем бота
    from aiogram import executor

    executor.start_polling(dp, skip_updates=True)
