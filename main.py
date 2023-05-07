import asyncio
import sqlite3
import io
from aiogram import Bot, Dispatcher, types
from aiogram import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode

from system.sqlite import reading_from_the_database_of_forbidden_words, writing_bad_words_to_the_database, \
    delete_bad_word, recording_actions_in_the_database

BOT_TOKEN = '6030769434:AAH6I8EolvOSpBQppNv1wtu91d1sD7GPeDs'  # Установите ваш токен Telegram

bot = Bot(token=BOT_TOKEN)  # Инициализируем бота и диспетчер
dp = Dispatcher(bot, storage=MemoryStorage())


class AddAndDelBadWords(StatesGroup):
    """Создаем состояние для добавления плохих слов"""
    waiting_for_bad_word = State()
    del_for_bad_word = State()


async def deleting_a_bot_message(del_bot_mes):
    """Удаление сообщений бота"""
    await asyncio.sleep(5)  # Спим 5 секунд
    await del_bot_mes.delete()  # Удаляем сообщение от бота


@dp.message_handler(commands=['add_bad'])
async def cmd_add_bad(message: types.Message):
    """Обработчик команды /add_bad"""
    # Проверяем, вызвал ли команду админ чата
    chat_member = await bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)
    if not chat_member.is_chat_admin():
        del_bot_mes = await message.reply('Эту команду может использовать только администратор чата.')
        await deleting_a_bot_message(del_bot_mes)  # Удаляем сообщение от бота
        await message.delete()  # Удаляем сообщение с командой
        return
    del_bot_mes = await message.answer('Введите слово, которое нужно добавить в список плохих слов:')
    await deleting_a_bot_message(del_bot_mes)  # Удаляем сообщение от бота
    await message.delete()  # Удаляем сообщение с командой
    await AddAndDelBadWords.waiting_for_bad_word.set()  # Переходим в состояние ожидания плохого слова


@dp.message_handler(commands=['del_bad'])
async def delete_bad_handler(message: types.Message):
    """Обработчик команды /del_bad"""
    # Проверяем, вызвал ли команду админ чата
    chat_member = await bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)
    if not chat_member.is_chat_admin():
        del_bot_mes = await message.reply('Эту команду может использовать только администратор чата.')
        await deleting_a_bot_message(del_bot_mes)  # Удаляем сообщение от бота
        await message.delete()  # Удаляем сообщение с командой
        return
    del_bot_mes = await message.answer('Введите слово, которое нужно удалить из базы данных:')
    await deleting_a_bot_message(del_bot_mes)  # Удаляем сообщение от бота
    await message.delete()  # Удаляем сообщение с командой
    await AddAndDelBadWords.del_for_bad_word.set()  # Переходим в состояние ожидания плохого слова


# Команда для получения данных из базы данных
@dp.message_handler(commands=["get_data"])
async def get_data(message: types.Message):
    # Создаем соединение с базой данных
    conn = sqlite3.connect('bad_words.db')
    # Получаем данные из базы данных
    data = conn.execute("SELECT * FROM bad_word_users").fetchall()
    # Закрываем соединение с базой данных
    conn.close()
    # Создаем файл в памяти
    output = io.StringIO()
    # Записываем данные в файл
    for row in data:
        output.write(str(row) + "\n")
    # Отправляем файл пользователю
    output.seek(0)
    await message.answer_document(types.InputFile(output, filename="data.txt"))


@dp.message_handler(state=AddAndDelBadWords.waiting_for_bad_word)
async def process_bad_word(message: types.Message, state: FSMContext):
    """Обработчик текстовых сообщений в состоянии ожидания плохого слова"""
    bad_word = message.text.strip().lower()  # Получаем слово от пользователя
    await writing_bad_words_to_the_database(bad_word)  # Запись запрещенных слов в базу данных
    # Выводим сообщение об успешном добавлении слова
    del_bot_mes = await message.reply(f'Слово "{bad_word}" успешно добавлено в список плохих слов.',
                                      parse_mode=ParseMode.HTML)
    await deleting_a_bot_message(del_bot_mes)  # Удаляем сообщение от бота
    await message.delete()  # Удаляем сообщение с командой
    await state.finish()  # Сбрасываем состояние


@dp.message_handler(state=AddAndDelBadWords.del_for_bad_word)
async def process_bad_word(message: types.Message, state: FSMContext):
    """Обработчик текстовых сообщений в состоянии ожидания плохого слова"""
    bad_word = message.text.strip().lower()  # Получаем слово от пользователя
    await delete_bad_word(bad_word)
    # Выводим сообщение об успешном удалении слова
    del_bot_mes = await message.reply(f'Слово "{bad_word}" успешно удалено из списка плохих слов.',
                                      parse_mode=ParseMode.HTML)
    await deleting_a_bot_message(del_bot_mes)  # Удаляем сообщение от бота
    await message.delete()  # Удаляем сообщение с командой
    await state.finish()  # Сбрасываем состояние


@dp.message_handler()
async def process_message(message: types.Message):
    """Обрабатываем сообщения от пользователей"""
    # Проверяем наличие запрещенных слов в сообщении
    bad_words = await reading_from_the_database_of_forbidden_words()
    for word in bad_words:
        if word[0] in message.text.lower():
            await message.delete()  # Удаляем сообщение от пользователя с запрещенным словом
            warning = await bot.send_message(message.chat.id, f'В вашем сообщении обнаружено запрещенное слово. '
                                                              f'Пожалуйста, не используйте его в дальнейшем.')
            await asyncio.sleep(20)  # Спим 20 секунд
            await warning.delete()  # Удаляем предупреждение от бота

    # Записываем действия пользователя в базу данных для каждого слова в сообщении
    words = message.text.split()
    for word in words:
        await recording_actions_in_the_database(word, message)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)  # Запускаем бота
