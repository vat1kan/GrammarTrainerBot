import botapp.keyboards as kb
import database.requests as rq
from helpers.geminiRequest import get_quiz, get_word
from aiogram import  html, F, Router, Bot
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
import aiocron
import asyncio

router = Router()

@router.message(CommandStart())
async def command_start_handler(message: Message):
    await rq.set_user(message.from_user.id)
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!\n\nChose the menu category", reply_markup=kb.main_menu)
    try:
        await msg_delete(message.bot, message.chat.id, message.message_id)
    except Exception as e:
        print(f"\nFailed to delete /start message {message.message_id} in chat {message.chat.id}:\n {e}\n")


@router.message(Command("menu"))
async def command_menu_handler(message: Message):
    try:
        await message.answer("Choose the menu category:", reply_markup=kb.main_menu)
        try:
            await msg_delete(message.bot, message.chat.id, message.message_id)
        except Exception as e:
            print(f"\nFailed to delete /menu message {message.message_id} in chat {message.chat.id}:\n {e}\n")
    except Exception as e:
        print(f"\nError sending menu keyboard to {message.chat.id}: {e}\n")

@router.callback_query(F.data == "menu")
async def get_menu_keyboard_callback(callback: CallbackQuery):
    try:
        await callback.message.edit_text("Choose the menu category:", reply_markup=kb.main_menu)
    except Exception as e:
        print(f"\nError editing message in chat {callback.message.chat.id}: {e}\n")


@router.callback_query(F.data == 'quiz')
async def send_quiz(callback: CallbackQuery):
    await create_quiz(bot=callback.bot, chat_id=callback.message.chat.id, menu = 1)
    await callback.message.edit_reply_markup(reply_markup=None)


@router.callback_query(F.data == 'word')
async def send_word(callback: CallbackQuery):
    try: 
        await create_word_message(callback.bot, callback.message.chat.id, menu = 1)
    except Exception as e:
        await callback.message.answer(f"#error\n\nSorry, an error occured to proccess your word message.\n\nTry to get a new one.", reply_markup=kb.main_menu)
        print(f"Error to send word to {callback.message.chat.id}:\n{e}")
    await callback.message.edit_reply_markup(reply_markup=None)


@router.callback_query(F.data == 'lvl')
async def levels(callback: CallbackQuery):
    try: 
        await callback.message.answer(f'#lvl\n\nYour current English level is {html.bold(await rq.get_lvl(callback.from_user.id))}'
                                      f'\n\nYou can set a new english level with followed buttons:', reply_markup=kb.lvls)
    except Exception as e:
        await callback.message.answer(f"#error\n\nSorry, an error occured to proccess your English level.\n\nTry one more time later.", reply_markup=kb.main_menu)
        print(f"Error to send lvl message to {callback.message.chat.id}:\n{e}")
    await callback.message.edit_reply_markup(reply_markup=None)


@router.callback_query(F.data == 'status')
async def upd_status(callback: CallbackQuery):
    try:
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
        await rq.upd_status(callback.from_user.id)
    except Exception as e:
        await callback.message.answer(f"#error\n\nSorry, an error occured to proccess your bot status.\n\nTry one more time later.", reply_markup=kb.main_menu)
        print(f"Error to update status for user {callback.message.chat.id}:\n{e}")
    await callback.message.edit_reply_markup(reply_markup=None)
    


async def update_level(callback: CallbackQuery, callback_data: kb.LevelCallback):
    try:
        await rq.upd_level(callback.from_user.id, callback_data.level)
        await callback.message.answer(
                                        f'#lvl\n\nYour English level updated for {html.bold(callback_data.level)}.\n'
                                        f'\n{html.bold(html.link('EnglishGrammarBot','https://t.me/TestGrammarEnglishBot'))}',
                                        reply_markup=kb.main_menu)
        await msg_delete(callback.bot, callback.message.chat.id, callback.message.message_id)
    except Exception as e:
        await callback.message.answer(f"#error\n\nSorry, an error occured to proccess your bot status.\n\nTry one more time later.", reply_markup=kb.main_menu)
        print(f"Error to update level for user {callback.message.chat.id}:\n{e}")
    await callback.message.edit_reply_markup(reply_markup=None)



async def msg_delete(bot, chat_id, message_id):
    try:
        await bot.delete_message(chat_id=chat_id, message_id=message_id)
    except Exception as e:
        print(f"Error deleting message: {e}")


async def auto_quiz_sending(bot: Bot):
    users = await rq.get_active_users()
    for user_id in users:
        try:
            await create_quiz(bot, user_id, 0)
        except Exception as e:
            print(f"\nFailed to send quiz message automaticaly for {user_id}:\n {e}\n")

async def auto_word_sending(bot: Bot):
    users = await rq.get_active_users()
    for user_id in users:
        try:
            await create_word_message(bot, user_id, 0)
        except Exception as e:
            print(f"\nFailed to send word message automaticaly for {user_id}:\n {e}\n")


async def setup_cron_jobs(bot: Bot):
    schedule = {
        "0 10 * * *": auto_quiz_sending,
        "0 12 * * *": auto_word_sending,
        "0 14 * * *": auto_quiz_sending,
        "0 16 * * *": auto_word_sending,
        "0 18 * * *": auto_quiz_sending,
        "0 20 * * *": auto_word_sending,
    }
    for time, task in schedule.items():
        aiocron.crontab(time, func=lambda t=task: asyncio.create_task(t(bot)))


async def create_quiz(bot: Bot, chat_id: int, menu: int):
    data = await get_quiz()
    try:
        await bot.send_poll(
            chat_id = chat_id,
            question=f"New Grammar Quiz\n\n{data['question']}",
            options=data['answers'],
            type='quiz',
            correct_option_id=data['correct'],
            explanation=data['explanation'],
            reply_markup=kb.main_menu if menu == 1 else None
        )
    except Exception as e:
        await bot.send_message(chat_id, f"#error\n\nSorry, an error occured to proccess your quiz.\n\nTry to get a new one.", reply_markup=kb.main_menu)
        print(f"Error to send word to {chat_id}:\n{e}")


async def create_word_message(bot: Bot, chat_id: int, menu: int):
    data = await get_word()
    await bot.send_message(chat_id, "#word\nYour new English word is here!"
                                                    f"""
                                                        \n{html.bold('Word: ')}{data['word']}
                                                        \n{html.bold('Part of speech: ')}{data['part']}
                                                        \n{html.bold('Meaning: ')}{data['meaning']}
                                                        \n{html.bold('Synonyms:')}\n{'\n'.join(f"{i+1}. {v}" for i, v in enumerate(data['synonyms']))}
                                                        \n{html.bold('Usage:')}\n{'\n'.join(f"{i+1}. {v}" for i, v in enumerate(data['usage']))}
                                                        \n{html.bold(html.link('EnglishGrammarBot','https://t.me/TestGrammarEnglishBot'))}  
                                                    """, reply_markup=kb.main_menu if menu == 1 else None)

router.callback_query.register(update_level, kb.LevelCallback.filter())