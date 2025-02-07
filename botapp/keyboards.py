from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

class AnswerCallback(CallbackData, prefix="answer"):
    index: int
    correct: int

class LevelCallback(CallbackData, prefix="level"):
    level: str

menu_button = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Menu')]])


main_menu = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='New Question', callback_data='quiz'),
                                                  InlineKeyboardButton(text='Get vocabulary ', callback_data='word')],
                                                  [InlineKeyboardButton(text='Change Level', callback_data='lvl'),
                                                  InlineKeyboardButton(text='Change Status', callback_data='status')]])

lvls = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='A1', callback_data = LevelCallback(level='A1').pack()),
                                            InlineKeyboardButton(text='A2 ', callback_data = LevelCallback(level='A2').pack())],
                                            [InlineKeyboardButton(text='B1', callback_data = LevelCallback(level='B1').pack()),
                                            InlineKeyboardButton(text='B2', callback_data = LevelCallback(level='B2').pack())],
                                            [InlineKeyboardButton(text='C1', callback_data = LevelCallback(level='C1').pack()),
                                            InlineKeyboardButton(text='C2', callback_data = LevelCallback(level='C2').pack())],
                                            [InlineKeyboardButton(text='Back To Menu', callback_data='menu')]])

async def answer_buttons(answers, correct):
    keyboard = InlineKeyboardBuilder()
    for index, item in enumerate(answers):
        keyboard.add(InlineKeyboardButton(text=f"{item}", callback_data = AnswerCallback(index=index, correct=correct).pack()))
    if len(answers[0]) > 30:
        return keyboard.adjust(1).as_markup()
    else:
        return keyboard.adjust(2).as_markup()
    