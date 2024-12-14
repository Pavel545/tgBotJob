quiz_data = [
    {
        'question': 'Какая река является самой длинной в мире?',
        'options': ['Нил', 'Амазонка', 'Миссисипи', 'Янцзы'],
        'correct_option': 0
    },
    {
        'question': 'Кто написал роман "Война и мир"?',
        'options': ['Лев Толстой', 'Федор Достоевский', 'Антон Чехов', 'Иван Тургенев'],
        'correct_option': 0
    },
    {
        'question': 'Какой элемент таблицы Менделеева имеет атомный номер 1?',
        'options': ['Гелий', 'Водород', 'Литий', 'Бeryлий'],
        'correct_option': 1
    },
    {
        'question': 'Кто такой Авраам Линкольн?',
        'options': ['16-й президент США', 'Изобретатель телефона', 'Писатель-романист', 'Композитор'],
        'correct_option': 0
    },
    {
        'question': 'Какой из этих городов находится на острове?',
        'options': ['Лондон', 'Париж', 'Афины', 'Стокгольм'],
        'correct_option': 3
    },
    {
        'question': 'Какое животное не может бегать?',
        'options': ['Тигр', 'Кенгуру', 'Черепаха', 'Лошадь'],
        'correct_option': 2
    },
    {
        'question': 'Какой год называется годом великого переселения народов?',
        'options': ['121 год до н.э.', '376 год н.э.', '1054 год н.э.', '1492 год н.э.'],
        'correct_option': 1
    },
    {
        'question': 'Какой из этих цветов не является основным цветом?',
        'options': ['Красный', 'Желтый', 'Синий', 'Зеленый'],
        'correct_option': 3
    },
    {
        'question': 'Какой из этих предметов не может плавать?',
        'options': ['Корабль', 'Камень', 'Плавающий мяч', 'Надувной матрас'],
        'correct_option': 1
    },
    {
        'question': 'Какой из этих месяцев не имеет 31 день?',
        'options': ['Январь', 'Март', 'Май', 'Июнь'],
        'correct_option': 1
    }
]


from fn.asDB import update_quiz_index, get_quiz_index
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import  types

async def new_quiz(message):
    # получаем id пользователя, отправившего сообщение
    user_id = message.from_user.id
    # сбрасываем значение текущего индекса вопроса квиза в 0
    current_question_index = 0
    await update_quiz_index(user_id, current_question_index)

    # запрашиваем новый вопрос для квиза
    await get_question(message, user_id)


async def get_question(message, user_id):

    # Запрашиваем из базы текущий индекс для вопроса
    current_question_index = await get_quiz_index(user_id)
    # Получаем индекс правильного ответа для текущего вопроса
    correct_index = quiz_data[current_question_index]['correct_option']
    # Получаем список вариантов ответа для текущего вопроса
    opts = quiz_data[current_question_index]['options']

    # Функция генерации кнопок для текущего вопроса квиза
    # В качестве аргументов передаем варианты ответов и значение правильного ответа (не индекс!)
    kb = generate_options_keyboard(opts, opts[correct_index])
    # Отправляем в чат сообщение с вопросом, прикрепляем сгенерированные кнопки
    await message.answer(f"{quiz_data[current_question_index]['question']}", reply_markup=kb)

def generate_options_keyboard(answer_options, right_answer):
  # Создаем сборщика клавиатур типа Inline
    builder = InlineKeyboardBuilder()

    # В цикле создаем 4 Inline кнопки, а точнее Callback-кнопки
    for option in answer_options:
        builder.add(types.InlineKeyboardButton(
            # Текст на кнопках соответствует вариантам ответов
            text=option,
            # Присваиваем данные для колбэк запроса.
            # Если ответ верный сформируется колбэк-запрос с данными 'right_answer'
            # Если ответ неверный сформируется колбэк-запрос с данными 'wrong_answer'
            callback_data="right_answer" if option == right_answer else "wrong_answer")
        )

    # Выводим по одной кнопке в столбик
    builder.adjust(1)
    return builder.as_markup()