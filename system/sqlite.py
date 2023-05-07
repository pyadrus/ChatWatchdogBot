import sqlite3


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
    # создаем подключение к базе данных
    with sqlite3.connect('bad_words.db') as conn:
        cursor = conn.cursor()
        # удаляем слово из таблицы
        cursor.execute('DELETE FROM bad_words WHERE word = ?', (word,))
        conn.commit()
