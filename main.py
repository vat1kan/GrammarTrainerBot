import asyncio
import logging
import sys
import os
from botapp.handlers import router

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

    
async def main():
    TOKEN = os.getenv('grammarBot')
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


logging.basicConfig(level=logging.INFO, stream=sys.stdout)
asyncio.run(main())