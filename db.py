import sqlite3

# Подключение к базе данных (создается новая база, если не существует)
conn = sqlite3.connect('subscriptions.db')
cursor = conn.cursor()

# Создание таблицы для хранения информации о пользователях и их подписках
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    is_premium INTEGER DEFAULT 0
)
''')
conn.commit()
conn.close()

def add_user(user_id, username):
    conn = sqlite3.connect('subscriptions.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    if cursor.fetchone() is None:
        cursor.execute('INSERT INTO users (user_id, username) VALUES (?, ?)', (user_id, username))
    conn.commit()
    conn.close()

def set_premium(user_id, is_premium):
    conn = sqlite3.connect('subscriptions.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET is_premium = ? WHERE user_id = ?', (is_premium, user_id))
    conn.commit()
    conn.close()

def is_premium(user_id):
    conn = sqlite3.connect('subscriptions.db')
    cursor = conn.cursor()
    cursor.execute('SELECT is_premium FROM users WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] == 1 if result else False