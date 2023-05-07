import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode

from system.sqlite import reading_from_the_database_of_forbidden_words, writing_bad_words_to_the_database

BOT_TOKEN = '6030769434:AAH6I8EolvOSpBQppNv1wtu91d1sD7GPeDs'  # Установите ваш токен Telegram

bot = Bot(token=BOT_TOKEN)  # Инициализируем бота и диспетчер
dp = Dispatcher(bot, storage=MemoryStorage())


class AddBadWords(StatesGroup):
    """Создаем состояние для добавления плохих слов"""
    waiting_for_bad_word = State()


@dp.message_handler(commands=['add_bad'])
async def cmd_add_bad(message: types.Message):
    """Обработчик команды /add_bad"""
    # Проверяем, вызвал ли команду админ чата
    chat_member = await bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)
    if not chat_member.is_chat_admin():
        await message.reply('Эту команду может использовать только администратор чата.')
        return
    await message.answer('Введите слово, которое нужно добавить в список плохих слов:')
    await AddBadWords.waiting_for_bad_word.set()  # Переходим в состояние ожидания плохого слова


@dp.message_handler(state=AddBadWords.waiting_for_bad_word)
async def process_bad_word(message: types.Message, state: FSMContext):
    """Обработчик текстовых сообщений в состоянии ожидания плохого слова"""
    bad_word = message.text.strip().lower()  # Получаем слово от пользователя
    await writing_bad_words_to_the_database(bad_word)  # Запись запрещенных слов в базу данных
    # Выводим сообщение об успешном добавлении слова
    await message.reply(f'Слово "{bad_word}" успешно добавлено в список плохих слов.', parse_mode=ParseMode.HTML)
    await state.finish()  # Сбрасываем состояние


@dp.message_handler(lambda message: True)
async def check_for_bad_words(message: types.Message):
    """Функция для проверки наличия запрещенных слов в сообщении"""
    bad_words = await reading_from_the_database_of_forbidden_words()  # Считываем запрещенные слова с базы данных
    for word in bad_words:
        if word[0] in message.text.lower():
            await message.delete()  # Удаляем сообщение от пользователя с запрещенным словом
            warning = await bot.send_message(message.chat.id, f'В вашем сообщении обнаружено запрещенное слово.'
                                                              f'\nПожалуйста, не используйте его в дальнейшем.')
            await asyncio.sleep(20)  # Спим 20 секунд
            await warning.delete()  # Удаляем сообщение от бота


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)  # Запускаем бота
