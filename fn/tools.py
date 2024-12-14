from fn.asDB import record_answer, update_quiz_index, get_quiz_index
from fn.quiz import quiz_data,get_question

async def transition(callback):
    user_id = callback.from_user.id
    current_question_index = await get_quiz_index(user_id)

    # Записываем ответ пользователя
    await record_answer(user_id, current_question_index, callback.data,  True if callback.data == 'right_answer' else False)

    # Удаляем клавиатуру и добавляем текст ответа пользователя
    # await callback.message.de()
  

    # Обновление номера текущего вопроса в базе данных
    current_question_index += 1
    await update_quiz_index(user_id, current_question_index)

    if current_question_index < len(quiz_data):
        await get_question(callback.message, user_id)
    else:
        await callback.message.answer("Это был последний вопрос. Квиз завершен! Чтобы посмотреть результат введите /results")
