import sqlite3


async def reading_from_the_database_of_forbidden_words():
    """Чтение с базы данных запрещенных слов"""
    # Инициализируем базу данных sqlite
    with sqlite3.connect('setting/bad_words.db') as conn:
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS bad_words (id INTEGER PRIMARY KEY AUTOINCREMENT, word TEXT)')
        conn.commit()
        bad_words = cursor.execute('SELECT word FROM bad_words').fetchall()
    return bad_words


async def reading_bad_words_from_the_database():
    """Чтение списка запрещенных слов из базы данных"""
    with sqlite3.connect('setting/bad_words.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT word FROM bad_words')
        data = cursor.fetchall()
        # Преобразуем список кортежей в список слов
        words = [row[0] for row in data]
        return words


async def reading_data_from_the_database():
    """Чтение с базы данных"""
    # Создаем соединение с базой данных
    conn = sqlite3.connect('setting/bad_words.db')
    # Получаем данные из базы данных
    data = conn.execute("SELECT * FROM bad_word_users").fetchall()
    # Закрываем соединение с базой данных
    conn.close()
    return data


async def reading_data_from_the_database_check():
    """Чтение с базы данных check слов"""
    # Создаем соединение с базой данных
    conn = sqlite3.connect('setting/bad_words.db')
    # Получаем данные из базы данных
    data = conn.execute("SELECT * FROM check_word_users").fetchall()
    # Закрываем соединение с базой данных
    conn.close()
    return data


async def reading_from_the_database_of_forbidden_check_word():
    """Чтение из базы данных запрещенных слов"""
    # Инициализируем базу данных sqlite
    with sqlite3.connect('setting/bad_words.db') as conn:
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS check_words (id INTEGER PRIMARY KEY AUTOINCREMENT, word TEXT)')
        conn.commit()
        check_words = cursor.execute('SELECT word FROM check_words').fetchall()
    return check_words
