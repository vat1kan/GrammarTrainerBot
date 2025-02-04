from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

class AnswerCallback(CallbackData, prefix="answer"):
    index: int
    correct: int

menu_button = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Menu')]])


main_menu = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='New Question', callback_data='quiz'),
                                                  InlineKeyboardButton(text='Get vocabulary ', callback_data='word')],
                                                  [InlineKeyboardButton(text='Change Level', callback_data='upd_lvl'),
                                                  InlineKeyboardButton(text='Change Status', callback_data='upd_status')]])

async def answer_buttons(answers, correct):
    keyboard = InlineKeyboardBuilder()
    for index, item in enumerate(answers):
        keyboard.add(InlineKeyboardButton(text=f"{item}", callback_data = AnswerCallback(index=index, correct=correct).pack()))
    if len(answers[0]) > 30:
        return keyboard.adjust(1).as_markup()
    else:
        return keyboard.adjust(2).as_markup()
    