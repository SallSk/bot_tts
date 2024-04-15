from config import MAX_TTS_SYMBOLS, MAX_USER_TTS_SYMBOLS
import sqlite3
def create_table(db_name="speech_kit.db"):
    try:
        # Создаём подключение к базе данных
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            # Создаём таблицу messages
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                message TEXT,
                tts_symbols INTEGER)
            ''')
            # Сохраняем изменения
            conn.commit()
    except Exception as e:(
        print(f"Error: {e}"))


def insert_row(user_id, text, tts_symbols, db_name="speech_kit.db"):
    try:
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            # Вставляем в таблицу новое сообщение
            cursor.execute('''INSERT INTO messages (user_id, message, tts_symbols)VALUES (?, ?, ?)''',
                           (user_id, text, tts_symbols))
            # Сохраняем изменения
            conn.commit()
    except Exception as e:
        print(f"Error: {e}")


def count_all_symbol(user_id, db_name="speech_kit.db"):
    try:
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            # Считаем, сколько символов использовал пользователь
            cursor.execute('''SELECT SUM(tts_symbols) FROM messages WHERE user_id=?''', (user_id,))
            data = cursor.fetchone()
            # Проверяем data на наличие хоть какого-то полученного результата запроса
            # И на то, что в результате запроса мы получили какое-то число в data[0]
            if data and data[0]:
                # Если результат есть и data[0] == какому-то числу, то
                return data[0]  # возвращаем это число - сумму всех потраченных символов
            else:
                # Результата нет, так как у нас ещё нет записей о потраченных символах
                return 0  # возвращаем 0
    except Exception as e:
        print(f"Error: {e}")


def is_tts_symbol_limit(user_id, text):
    all_symbols = count_all_symbol(user_id) + len(text)

    # Сравниваем all_symbols с количеством доступных пользователю символов
    if all_symbols >= MAX_USER_TTS_SYMBOLS:
        msg = f"Превышен общий лимит SpeechKit TTS {MAX_USER_TTS_SYMBOLS}. Использовано: {all_symbols} символов. Доступно: {MAX_USER_TTS_SYMBOLS - all_symbols}"
        return msg

    # Сравниваем количество символов в тексте с максимальным количеством символов в тексте
    if len(text) >= MAX_TTS_SYMBOLS:
        msg = f"Превышен лимит на запрос SpeechKit TTS {MAX_TTS_SYMBOLS}, в сообщении {len(text)} символов"
        return msg
    return len(text)
