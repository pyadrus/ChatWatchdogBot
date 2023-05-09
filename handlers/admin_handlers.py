import asyncio
import io

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ParseMode

from system.dispatcher import dp, bot, AddAndDelBadWords
from system.dispatcher import time_del
from system.read_sqlite import reading_from_the_database_of_forbidden_check_word, reading_data_from_the_database, \
    reading_bad_words_from_the_database, reading_from_the_database_of_forbidden_words, \
    reading_data_from_the_database_check
from system.sqlite import delete_bad_word, recording_actions_check_word_in_the_database
from system.sqlite import recording_actions_in_the_database
from system.sqlite import writing_bad_words_to_the_database
from system.sqlite import writing_check_words_to_the_database

info = '''
<b>✅ Основные команды бота:</b>
/start         – 🤖 Запустить бота.
/help          – 🤖 Получить информацию о работе с ботом.
/add_bad       – 🧾 Добавить запрещенное слово.
/del_bad       – 🧾 Удалить запрещенное слово.
/add_check     – 🧾 Добавить check слов.
/get_data      – 🧾 Получить список пользователей, использующих запрещенные слова,
/get_bad_words – 🧾 Получить список запрещенных слов.
/get_data_check– 🧾 Получить список check слов.
<u>@PyAdminRUS</u>   – 🔗 Связаться с разработчиком бота 🤖.
'''


@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message) -> None:
    """Отвечаем на команду /start"""
    await message.reply(info, parse_mode="HTML")


@dp.message_handler(commands=["help"])
async def help_handler(message: types.Message) -> None:
    """Отвечаем на команду /help"""
    await message.reply(info, parse_mode="HTML")


@dp.message_handler(commands=['add_bad'])
async def cmd_add_bad(message: types.Message):
    """Обработчик команды /add_bad"""
    # Проверяем, вызвал ли команду админ чата
    chat_member = await bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)
    if not chat_member.is_chat_admin():
        await message.reply('Эту команду может использовать только администратор чата.')
        return
    await message.answer('Введите слово, которое нужно добавить в список плохих слов:')
    await AddAndDelBadWords.waiting_for_bad_word.set()  # Переходим в состояние ожидания плохого слова


@dp.message_handler(commands=['add_check'])
async def cmd_add_check(message: types.Message):
    """Обработчик команды /add_check"""
    # Получаем информацию о пользователе
    user = await bot.get_chat_member(message.chat.id, message.from_user.id)
    # Проверяем, является ли пользователь администратором чата
    if user.status in ("administrator", "creator"):
        await message.answer('Введите check слово, которое нужно добавить в список check слов:')
        await AddAndDelBadWords.waiting_for_check_word.set()  # Переходим в состояние ожидания плохого слова
    else:
        # Отправляем сообщение о том, что пользователь не является администратором чата
        await message.reply("Команда доступна только администраторам чата.")


@dp.message_handler(commands=['del_bad'])
async def delete_bad_handler(message: types.Message):
    """Обработчик команды /del_bad"""
    # Проверяем, вызвал ли команду админ чата
    chat_member = await bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)
    if not chat_member.is_chat_admin():
        await message.reply('Эту команду может использовать только администратор чата.')
        return
    await message.answer('Введите слово, которое нужно удалить из базы данных:')
    await AddAndDelBadWords.del_for_bad_word.set()  # Переходим в состояние ожидания плохого слова


@dp.message_handler(commands=["get_data_bad"])
async def get_data(message: types.Message):
    """Команда для получения данных из базы данных с помощью команды /get_data"""
    # Получаем информацию о пользователе
    user = await bot.get_chat_member(message.chat.id, message.from_user.id)
    # Проверяем, является ли пользователь администратором чата
    if user.status in ("administrator", "creator"):
        # Получаем данные из базы данных
        data = await reading_data_from_the_database()
        # Создаем файл в памяти
        output = io.StringIO()
        # Записываем данные в файл
        for row in data:
            output.write(str(row) + "\n")
        # Отправляем файл пользователю в личку
        output.seek(0)
        await bot.send_document(message.from_user.id, types.InputFile(output, filename="data_bad.txt"))
        # Отправляем сообщение с результатом в личку пользователю
        await bot.send_message(message.from_user.id, "Данные успешно отправлены вам в личку.")
    else:
        # Отправляем сообщение о том, что пользователь не является администратором чата
        await message.reply("Команда доступна только администраторам чата.")


@dp.message_handler(commands=["get_data_check"])
async def get_data_check(message: types.Message):
    """Команда для получения данных из базы данных с помощью команды /get_data_check"""
    # Получаем информацию о пользователе
    user = await bot.get_chat_member(message.chat.id, message.from_user.id)
    # Проверяем, является ли пользователь администратором чата
    if user.status in ("administrator", "creator"):
        # Получаем данные из базы данных
        data = await reading_data_from_the_database_check()
        # Создаем файл в памяти
        output = io.StringIO()
        # Записываем данные в файл
        for row in data:
            output.write(str(row) + "\n")
        # Отправляем файл пользователю в личку
        output.seek(0)
        await bot.send_document(message.from_user.id, types.InputFile(output, filename="data_check.txt"))
        # Отправляем сообщение с результатом в личку пользователю
        await bot.send_message(message.from_user.id, "Данные успешно отправлены вам в личку.")
    else:
        # Отправляем сообщение о том, что пользователь не является администратором чата
        await message.reply("Команда доступна только администраторам чата.")


@dp.message_handler(commands=["get_bad_words"])
async def get_bad_words(message: types.Message):
    """Команда для получения списка запрещенных слов /get_bad_words"""
    user = await bot.get_chat_member(message.chat.id, message.from_user.id)
    # Проверяем, является ли пользователь администратором чата
    if user.status in ("administrator", "creator"):
        bad_words = await reading_bad_words_from_the_database()
        output = io.StringIO()
        for word in bad_words:
            output.write(word + "\n")
        output.seek(0)
        await bot.send_document(message.from_user.id, types.InputFile(output, filename="bad_words.txt"))
    else:
        await message.answer("Вы должны быть администратором чата, чтобы получить список запрещенных слов.")


@dp.message_handler(state=AddAndDelBadWords.waiting_for_bad_word)
async def process_bad_word(message: types.Message, state: FSMContext):
    """Обработчик текстовых сообщений в состоянии ожидания плохого слова"""
    bad_word = message.text.strip().lower()  # Получаем слово от пользователя
    user_id = message.from_user.id  # Получаем ID пользователя
    username = message.from_user.username  # Получаем username пользователя
    user_full_name = message.from_user.full_name  # Получаем Ф.И. пользователя
    chat_id = message.chat.id  # Получаем ID чата / канала
    chat_title = message.chat.title  # Получаем название чата / канала
    await writing_bad_words_to_the_database(bad_word, user_id, username, user_full_name, chat_id,
                                            chat_title)  # Запись запрещенных слов в базу данных
    # Выводим сообщение об успешном добавлении слова
    await message.reply(f'✅ Слово успешно добавлено ➕ в список плохих слов 🤬.', parse_mode=ParseMode.HTML)
    await state.finish()  # Сбрасываем состояние


@dp.message_handler(state=AddAndDelBadWords.del_for_bad_word)
async def process_bad_word(message: types.Message, state: FSMContext):
    """Обработчик текстовых сообщений в состоянии ожидания плохого слова"""
    bad_word = message.text.strip().lower()  # Получаем слово от пользователя
    await delete_bad_word(bad_word)
    # Выводим сообщение об успешном удалении слова
    await message.reply(f'Слово успешно удалено ➖ из списка плохих слов 🤬.', parse_mode=ParseMode.HTML)
    await state.finish()  # Сбрасываем состояние


@dp.message_handler(state=AddAndDelBadWords.waiting_for_check_word)
async def process_check_word(message: types.Message, state: FSMContext):
    """Обработчик текстовых сообщений в состоянии ожидания плохого слова"""
    bad_word = message.text.strip().lower()  # Получаем слово от пользователя
    user_id = message.from_user.id  # Получаем ID пользователя
    username = message.from_user.username  # Получаем username пользователя
    user_full_name = message.from_user.full_name  # Получаем Ф.И. пользователя
    chat_id = message.chat.id  # Получаем ID чата / канала
    chat_title = message.chat.title  # Получаем название чата / канала
    await writing_check_words_to_the_database(bad_word, user_id, username, user_full_name, chat_id,
                                              chat_title)  # Запись запрещенных слов в базу данных
    # Выводим сообщение об успешном добавлении слова
    await message.reply(f'✅ Слово успешно добавлено ➕ в список check слов.', parse_mode=ParseMode.HTML)
    await state.finish()  # Сбрасываем состояние


@dp.message_handler()
async def process_message(message: types.Message):
    """Обрабатываем сообщения от пользователей"""
    # Проверяем наличие запрещенных слов в сообщении
    bad_words = await reading_from_the_database_of_forbidden_words()
    for word in bad_words:
        if word[0] in message.text.lower():
            await recording_actions_in_the_database(word[0], message)
            await message.delete()  # Удаляем сообщение от пользователя с запрещенным словом
            warning = await bot.send_message(message.chat.id, f'В вашем сообщении обнаружено запрещенное слово. '
                                                              f'Пожалуйста, не используйте его в дальнейшем.')
            await asyncio.sleep(int(time_del))  # Спим 20 секунд
            await warning.delete()  # Удаляем предупреждение от бота

    # Проверяем наличие запрещенных слов для проверки в сообщении
    check_words = await reading_from_the_database_of_forbidden_check_word()
    for check_word in check_words:
        if check_word[0] in message.text.lower():
            await recording_actions_check_word_in_the_database(check_word[0], message)


def admin_handlers():
    """Регистрируем handlers для администраторов группы / каналов"""
    dp.register_message_handler(cmd_add_check)  # Команда /add_check
    dp.register_message_handler(cmd_add_bad)  # Команда /add_bad
    dp.register_message_handler(send_welcome)  # Команда /start
    dp.register_message_handler(help_handler)  # Команда /help
    dp.register_message_handler(delete_bad_handler)  # Команда /del_bad
    dp.register_message_handler(get_data)  # Команда /get_data
    dp.register_message_handler(get_bad_words)  # Команда /get_bad_words
    dp.register_message_handler(get_data_check)  # Команда /get_data_check
