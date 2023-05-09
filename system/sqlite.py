import sqlite3
from datetime import datetime


async def writing_bad_words_to_the_database(bad_word, user_id, username, user_full_name, chat_id, chat_title):
    """
    Запись запрещенных слов в базу данных setting/bad_words.db, при добавлении нового слова функция ищет дубликаты слов,
    и при нахождении оставляет одно слово без повтора"""
    # Инициализируем базу данных sqlite
    with sqlite3.connect('setting/bad_words.db') as conn:
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS bad_words (id INTEGER PRIMARY KEY AUTOINCREMENT, word TEXT, '
                       'user_id INTEGER, username TEXT, user_full_name TEXT, chat_id INTEGER, chat_title TEXT)')
        # Получаем список всех слов в базе данных sqlite
        cursor.execute('SELECT word FROM bad_words')
        existing_words = [row[0] for row in cursor.fetchall()]
        # Проверяем, есть ли новое слово уже в списке существующих слов
        if bad_word in existing_words:
            # Если новое слово уже есть в базе данных, то удаляем его
            cursor.execute('DELETE FROM bad_words WHERE word = ?', (bad_word,))
        # Добавляем слово в базу данных sqlite
        cursor.execute('INSERT INTO bad_words (word, user_id, username, user_full_name, chat_id, chat_title) '
                       'VALUES (?, ?, ?, ?, ?, ?)',
                       (bad_word, user_id, username, user_full_name, chat_id, chat_title))
        conn.commit()


async def writing_check_words_to_the_database(bad_word, user_id, username, user_full_name, chat_id, chat_title):
    """
    Запись check слов в базу данных setting/bad_words.db, при добавлении нового слова функция ищет дубликаты слов, и при
    нахождении оставляет одно слово без повтора"""
    # Инициализируем базу данных sqlite
    with sqlite3.connect('setting/bad_words.db') as conn:
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS check_words (id INTEGER PRIMARY KEY AUTOINCREMENT, word TEXT, '
                       'user_id INTEGER, username TEXT, user_full_name TEXT, chat_id INTEGER, chat_title TEXT)')
        # Получаем список всех слов в базе данных sqlite
        cursor.execute('SELECT word FROM bad_words')
        existing_words = [row[0] for row in cursor.fetchall()]
        # Проверяем, есть ли новое слово уже в списке существующих слов
        if bad_word in existing_words:
            # Если новое слово уже есть в базе данных, то удаляем его
            cursor.execute('DELETE FROM check_words WHERE word = ?', (bad_word,))
        # Добавляем слово в базу данных sqlite
        cursor.execute('INSERT INTO check_words (word, user_id, username, user_full_name, chat_id, chat_title) '
                       'VALUES (?, ?, ?, ?, ?, ?)',
                       (bad_word, user_id, username, user_full_name, chat_id, chat_title))
        conn.commit()


async def delete_bad_word(word):
    """Удаление плохих слов с базы данных"""
    # создаем подключение к базе данных
    with sqlite3.connect('setting/bad_words.db') as conn:
        cursor = conn.cursor()
        # удаляем слово из таблицы
        cursor.execute('DELETE FROM bad_words WHERE word = ?', (word,))
        conn.commit()


async def recording_actions_in_the_database(word, message):
    """Запись действий в базу данных запрещенных слов"""
    # Создаем соединение с базой данных
    conn = sqlite3.connect('setting/bad_words.db')
    # Создаем таблицы для хранения информации о пользователях, использующих запрещенные слова, и самих запрещенных слов
    conn.execute('''CREATE TABLE IF NOT EXISTS bad_word_users
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, username TEXT, full_name TEXT,
                      word TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.execute('''CREATE TABLE IF NOT EXISTS bad_words (id INTEGER PRIMARY KEY AUTOINCREMENT, word TEXT)''')
    # Проверяем, является ли слово запрещенным
    conn.execute("SELECT id FROM bad_words WHERE word=?", (word,)).fetchone()
    # Получаем информацию о пользователе
    user_id = message.from_user.id
    username = message.from_user.username
    full_name = message.from_user.full_name
    conn.execute("INSERT INTO bad_word_users (user_id, username, full_name, word, timestamp) VALUES (?, ?, ?, ?, ?)",
                (user_id, username, full_name, word, datetime.now()))
    conn.commit()
    # Закрываем соединение с базой данных
    conn.close()


async def recording_actions_check_word_in_the_database(word, message):
    """Запись действий в базу данных check слов"""
    # Создаем соединение с базой данных
    conn = sqlite3.connect('setting/bad_words.db')
    # Создаем таблицы для хранения информации о пользователях, использующих запрещенные слова, и самих запрещенных слов
    conn.execute('''CREATE TABLE IF NOT EXISTS check_word_users (user_id INTEGER, username TEXT, full_name TEXT,
                                                                 word TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.execute('''CREATE TABLE IF NOT EXISTS check_word_users (word TEXT)''')
    # Получаем информацию о пользователе
    user_id = message.from_user.id
    username = message.from_user.username
    full_name = message.from_user.full_name
    # Записываем информацию о пользователе в базу данных
    conn.execute("INSERT INTO check_word_users (user_id, username, full_name, word, timestamp) VALUES (?, ?, ?, ?, ?)",
                (user_id, username, full_name, word, datetime.now()))
    conn.commit()
    # Закрываем соединение с базой данных
    conn.close()
