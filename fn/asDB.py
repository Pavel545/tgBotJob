import aiosqlite
DB_NAME = 'quiz_bot.db'

# Создание таблицы
async def create_table():
    # Создаем соединение с базой данных (если она не существует, то она будет создана)
    async with aiosqlite.connect(DB_NAME) as db:
        # Выполняем SQL-запрос для создания таблицы quiz_state
        await db.execute('''CREATE TABLE IF NOT EXISTS quiz_state (user_id INTEGER PRIMARY KEY, question_index INTEGER)''')

        # Выполняем SQL-запрос для создания таблицы user_answers
        await db.execute('''
            CREATE TABLE IF NOT EXISTS user_answers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                question_index INTEGER,
                answer TEXT,
                is_correct BOOLEAN
            )
        ''')

        # Сохраняем изменения
        await db.commit()

# запись пользователя или изменение
async def update_quiz_index(user_id, index):
    # Создаем соединение с базой данных (если она не существует, она будет создана)
    async with aiosqlite.connect(DB_NAME) as db:
        # Вставляем новую запись или заменяем ее, если с данным user_id уже существует
        await db.execute('INSERT OR REPLACE INTO quiz_state (user_id, question_index) VALUES (?, ?)', (user_id, index))
        # Сохраняем изменения
        await db.commit()

# функция, которая получит текущее значение question_index в базе данных для заданного пользователя.
async def get_quiz_index(user_id):
     # Подключаемся к базе данных
     async with aiosqlite.connect(DB_NAME) as db:
        # Получаем запись для заданного пользователя
        async with db.execute('SELECT question_index FROM quiz_state WHERE user_id = (?)', (user_id, )) as cursor:
            # Возвращаем результат
            results = await cursor.fetchone()
            if results is not None:
                return results[0]
            else:
                return 0
            
# Функция для записи ответа пользователя в базу данных
async def record_answer(user_id, question_index, answer, is_correct):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''
            INSERT INTO user_answers (user_id, question_index, answer, is_correct)
            VALUES (?, ?, ?, ?)
        ''', (user_id, question_index, answer, is_correct))
        await db.commit()


async def get_quiz_results(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('''
            SELECT question_index, answer, is_correct
            FROM user_answers
            WHERE user_id = ?
            ORDER BY question_index
        ''', (user_id,)) as cursor:
            results = await cursor.fetchall()
            return results
        
# подчистка
async def clear_user_answers(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('DELETE FROM user_answers WHERE user_id = ?', (user_id,))
        await db.commit()