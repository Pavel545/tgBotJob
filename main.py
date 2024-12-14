#@title Полный код бота для самоконтроля
import aiosqlite
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram import F

from fn.asDB import create_table, clear_user_answers, get_quiz_index, get_quiz_results, record_answer
from fn.quiz import quiz_data, get_question, new_quiz

import fn.tools as tools

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

API_TOKEN = 'API_TOKEN'

# Объект бота
bot = Bot(token=API_TOKEN)
# Диспетчер
dp = Dispatcher()








@dp.callback_query(F.data == "right_answer")
async def right_answer(callback: types.CallbackQuery):
    await callback.message.answer("Верно!")

    await tools.transition(callback)


@dp.callback_query(F.data == "wrong_answer")
async def wrong_answer(callback: types.CallbackQuery):
    await callback.message.answer("Неверно!")
    await tools.transition(callback)


# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Начать игру"))
    await message.answer("Добро пожаловать в квиз!", reply_markup=builder.as_markup(resize_keyboard=True))





# Хэндлер на команду /quiz
@dp.message(F.text=="Начать игру")
@dp.message(Command("quiz"))
async def cmd_quiz(message: types.Message):

    await message.answer(f"Давайте начнем квиз!")
    await clear_user_answers(message.from_user.id)
    await new_quiz(message)


# Хэндлер на команду /results

@dp.message(Command("results"))
async def show_results(message: types.Message):
    user_id = message.from_user.id
    results = await get_quiz_results(user_id)

    if not results:
        await message.answer("Вы еще не прошли ни одного квиза.")
        return

    total_questions = len(results)
    correct_answers = sum(1 for result in results if result[2])

    result_message = f"Вы ответили на {total_questions} вопросов.\nПравильных ответов: {correct_answers}\n"

    for question_index, answer, is_correct in results:
        result_message += f"Вопрос {question_index+1}: - {'Правильно' if is_correct else 'Неправильно'}\n"

    await message.answer(result_message)


# Запуск процесса поллинга новых апдейтов
async def main():

    # Запускаем создание таблицы базы данных
    await create_table()

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())