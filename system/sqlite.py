import sqlite3
from datetime import datetime


async def writing_bad_words_to_the_database(bad_word):
    """Запись запрещенных слов в базу данных bad_words.db"""
    # Инициализируем базу данных sqlite
    with sqlite3.connect('bad_words.db') as conn:
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS bad_words (id INTEGER PRIMARY KEY AUTOINCREMENT, word TEXT)')
        # Добавляем слово в базу данных sqlite
        cursor.execute('INSERT INTO bad_words (word) VALUES (?)', (bad_word,))
        conn.commit()


async def reading_from_the_database_of_forbidden_words():
    """Чтение с базы данных запрещенных слов"""
    # Инициализируем базу данных sqlite
    with sqlite3.connect('bad_words.db') as conn:
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS bad_words (id INTEGER PRIMARY KEY AUTOINCREMENT, word TEXT)')
        conn.commit()
        bad_words = cursor.execute('SELECT word FROM bad_words').fetchall()
    return bad_words


async def delete_bad_word(word):
    """Удаление плохих слов с базы данных"""
    # создаем подключение к базе данных
    with sqlite3.connect('bad_words.db') as conn:
        cursor = conn.cursor()
        # удаляем слово из таблицы
        cursor.execute('DELETE FROM bad_words WHERE word = ?', (word,))
        conn.commit()


async def recording_actions_in_the_database(word, message):
    """Запись действий в базу данных"""
    # Создаем соединение с базой данных
    conn = sqlite3.connect('bad_words.db')
    # Создаем таблицы для хранения информации о пользователях, использующих запрещенные слова, и самих запрещенных слов
    conn.execute('''CREATE TABLE IF NOT EXISTS bad_word_users
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      user_id INTEGER,
                      username TEXT,
                      full_name TEXT,
                      word TEXT,
                      timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.execute('''CREATE TABLE IF NOT EXISTS bad_words
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      word TEXT)''')

    # Проверяем, является ли слово запрещенным
    word_id = conn.execute("SELECT id FROM bad_words WHERE word=?", (word,)).fetchone()
    if word_id:
        # Получаем информацию о пользователе
        user_id = message.from_user.id
        username = message.from_user.username
        full_name = message.from_user.full_name
        word = conn.execute("SELECT word FROM bad_words WHERE id=?", (word_id[0],)).fetchone()[0]
        # Записываем информацию о пользователе в базу данных
        conn.execute("INSERT INTO bad_word_users (user_id, username, full_name, word, timestamp) VALUES (?, ?, ?, ?, ?)",
                     (user_id, username, full_name, word, datetime.now()))
        conn.commit()
    # Закрываем соединение с базой данных
    conn.close()

