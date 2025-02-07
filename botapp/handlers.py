import botapp.keyboards as kb
import database.requests as rq
from helpers.geminiRequest import getContent
from aiogram import  html, F, Router, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
import aiocron
import asyncio

router = Router()

@router.message(CommandStart())
async def command_start_handler(message: Message):
    await rq.set_user(message.from_user.id)
    menu_text = await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!\n\nChose the menu category", reply_markup=kb.main_menu)
    global menu_msg_id    
    menu_msg_id = menu_text.message_id

@router.callback_query(F.data == 'quiz')
async def quiz(callback: CallbackQuery):
    global data
    data = await getContent('test')
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.answer('New Quiz created')
    global question_msg_id
    question_text = await callback.message.answer("#test\n\nYour new question is here!\n\n"
                                                  f"<b>{data['question']}</b>\n\n",
                                                  reply_markup = await kb.answer_buttons(data['answers'], data['correct']))
    question_msg_id = question_text.message_id
    if 'menu_msg_id' in globals():
        await msg_delete(callback.bot, callback.message.chat.id, menu_msg_id)


@router.callback_query(F.data == 'word')
async def word(callback: CallbackQuery):
    global data
    data = await getContent('word')
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.answer('New English Word')
    await callback.message.answer("#word\nYour new English word is here!"
                                                f"""
                                                    \n{html.bold('Word: ')}{data['word']}
                                                    \n{html.bold('Part of speech: ')}{data['part']}
                                                    \n{html.bold('Meaning: ')}{data['meaning']}
                                                    \n{html.bold('Synonyms:')}\n{'\n'.join(f"{i+1}. {v}" for i, v in enumerate(data['synonyms']))}
                                                    \n{html.bold('Usage:')}\n{'\n'.join(f"{i+1}. {v}" for i, v in enumerate(data['usage']))}
                                                    \n{html.bold(html.link('EnglishGrammarBot','https://t.me/TestGrammarEnglishBot'))}  
                                                """,
                                                reply_markup = kb.main_menu)
    if 'menu_msg_id' in globals():
        await msg_delete(callback.bot, callback.message.chat.id, menu_msg_id)


@router.callback_query(F.data == 'lvl')
async def levels(callback: CallbackQuery):
    await callback.answer()
    if 'menu_msg_id' in globals():
        await msg_delete(callback.bot, callback.message.chat.id, menu_msg_id)
    await callback.message.edit_reply_markup(reply_markup=None)
    lvl_buttons = await callback.message.answer(f'#lvl\n\nYour current English level is {html.bold(await rq.get_lvl(callback.from_user.id))}'
                                  f'\n\nYou can set a new english level with followed buttons:', 
                                  reply_markup=kb.lvls
                                  )
    global lvl_message
    lvl_message = lvl_buttons.message_id


@router.callback_query(F.data == 'status')
async def upd_status(callback: CallbackQuery):
    current_status = await rq.get_status(callback.from_user.id)
    if (current_status == 0):
        await callback.message.answer(f"#status\n\nYour status set as {html.bold('Active')}.\n"
                                      f"\nThe automatic sending of new questions to you is active.\n"
                                      f'\n{html.bold(html.link('EnglishGrammarBot','https://t.me/TestGrammarEnglishBot'))}',
                                      reply_markup=kb.main_menu)
    else:
        await callback.message.answer(f"#status\n\nYour status set as {html.bold('Disabled')}.\n"
                                      f"\nThe automatic sending of new questions to you is disabled,\n"
                                      f"but you can still use the full functionality of the bot."
                                      f'\n{html.bold(html.link('\nEnglishGrammarBot','https://t.me/TestGrammarEnglishBot'))}',
                                      reply_markup=kb.main_menu)
    await callback.message.edit_reply_markup(reply_markup=None)
    await rq.upd_status(callback.from_user.id)
    if 'menu_msg_id' in globals():
        await msg_delete(callback.bot, callback.message.chat.id, menu_msg_id)
    

async def update_level(callback: CallbackQuery, callback_data: kb.LevelCallback):
    await rq.upd_level(callback.from_user.id, callback_data.level)
    await callback.answer(f"✅ Level {callback_data.level} is set")
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer(
                                    f'#lvl\n\nYour English level updated for {html.bold(callback_data.level)}.\n'
                                    f'\n{html.bold(html.link('EnglishGrammarBot','https://t.me/TestGrammarEnglishBot'))}',
                                    reply_markup=kb.main_menu)
    if 'lvl_message' in globals():
        await msg_delete(callback.bot, callback.message.chat.id, lvl_message)


async def checker(callback: CallbackQuery, callback_data: kb.AnswerCallback):
    if callback_data.index == callback_data.correct:
        await callback.answer("✅ Your answer is correct!")
    else:
        await callback.answer("❌ Your answer is wrong!")

    if 'data' in globals():
        await callback.message.answer(
            f"#answer\n\n{html.bold('Question:')}\n{data['question']}\n\n"
            f"{html.bold('Correct answer: ')}{data['answers'][data['correct']]}\n\n"
            f"{html.bold('Your answer: ')}{data['answers'][callback_data.index]}\n\n"
            f"{html.bold('Explanation:\n')}{data['explanation']}\n"
            f"{html.bold(html.link('\nEnglishGrammarBot','https://t.me/TestGrammarEnglishBot'))}", 
            reply_markup=kb.main_menu)
        if 'question_msg_id' in globals():
            await msg_delete(callback.bot, callback.message.chat.id, callback.message.message_id)
    else:
        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.message.answer(
            f"#error\n\nSorry, an error occured to proccess your answer.\n\nSelect the menu category:", 
            reply_markup=kb.main_menu)


async def msg_delete(bot, chat_id, message_id):
    try:
        await bot.delete_message(chat_id=chat_id, message_id=message_id)
    except Exception as e:
        print(f"Error deleting message: {e}")

async def autoQuestion(bot: Bot):
    print("\n\nAuto Question is triggered")
    global data, question_msg_id
    users = await rq.get_active_users()
    data = await getContent('test')
    for user_id in users:
        try:
            question_text = await bot.send_message(
                user_id,
                "#test\n\nYour new question is here!\n\n"
                f"<b>{data['question']}</b>\n\n",
                reply_markup=await kb.answer_buttons(data['answers'], data['correct']))
            question_msg_id = question_text.message_id
        except Exception as e:
            print(f"\n\n!! Error to send message for {user_id}:\n\n{e}\n\n")

async def setup_cron_jobs(bot: Bot):
    aiocron.crontab("* */2 * * *", func=lambda: asyncio.create_task(autoQuestion(bot))) 

router.callback_query.register(checker, kb.AnswerCallback.filter())
router.callback_query.register(update_level, kb.LevelCallback.filter())