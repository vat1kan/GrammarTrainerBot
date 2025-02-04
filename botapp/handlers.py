import botapp.keyboards as kb
from helpers.request import gemini_requst
from aiogram import  html, F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery

router = Router()

async def msg_delete(bot, chat_id, message_id):
        try:
            await bot.delete_message(chat_id=chat_id, message_id=message_id)
        except Exception as e:
            print(f"Error deleting message: {e}")

@router.message(CommandStart())
async def command_start_handler(message: Message):
    global menu_msg_id
    menu_text = await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!\n\nChose the menu category", reply_markup=kb.main_menu)    
    menu_msg_id = menu_text.message_id


@router.callback_query(F.data == 'quiz')
async def quiz(callback: CallbackQuery):
    global data
    data = await gemini_requst('test')
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.answer('New Quiz created')
    global question_msg_id
    question_text = await callback.message.answer("#test\n\nYour new question is here!\n\n"
                                                  f"<b>{data['question']}</b>\n\n",
                                                  reply_markup = await kb.answer_buttons(data['answers'], data['correct']))
    question_msg_id = question_text.message_id
    await msg_delete(callback.bot, callback.message.chat.id, menu_msg_id)

async def checker(callback: CallbackQuery, callback_data: kb.AnswerCallback):
    if callback_data.index == callback_data.correct:
        await callback.answer("✅ Your answer is correct!")
    else:
        await callback.answer("❌ Your answer is wrong!")
    await callback.message.answer(
        f"#answer\n\n{html.bold('Question:')}\n{data['question']}\n\n"
        f"{html.bold('Correct answer: ')}{data['answers'][data['correct']]}\n\n"
        f"{html.bold('Your answer: ')}{data['answers'][callback_data.index]}\n\n"
        f"{html.bold('Explanation:\n')}{data['explanation']}\n"
        f"{html.bold(html.link('\nEnglishGrammarBot','https://t.me/TestGrammarEnglishBot'))}", 
        reply_markup=kb.main_menu
        )
    await msg_delete(callback.bot, callback.message.chat.id, question_msg_id)


@router.callback_query(F.data == 'word')
async def quiz(callback: CallbackQuery):
    global data
    data = await gemini_requst('word')
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.answer('New English Word')
    await callback.message.answer("#word\nYour new English word is here!"
                                                f"""
                                                    \n{html.bold('Word: ')}{data['word']}
                                                    \n{html.bold('Part of speech: ')}{data['part']}
                                                    \n{html.bold('Meaning: ')}{data['meaning']}
                                                    \n{html.bold('Synonyms:')}\n{'\n'.join(f"{i+1}. {v}" for i, v in enumerate(data['synonyms']))}
                                                    \n{html.bold('Usage:')}\n{'\n'.join(f"{i+1}. {v}" for i, v in enumerate(data['usage']))}
                                                    \n{html.bold(html.link('\nEnglishGrammarBot','https://t.me/TestGrammarEnglishBot'))}  
                                                """,
                                                reply_markup = kb.main_menu)
    await msg_delete(callback.bot, callback.message.chat.id, menu_msg_id)

router.callback_query.register(checker, kb.AnswerCallback.filter())