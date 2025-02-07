import asyncio
import logging
import sys
import os
from botapp.handlers import router, setup_cron_jobs
from database.models import async_main

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

    
async def main():
    await async_main()
    bot = Bot(token=os.getenv('grammarBot'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    dp.include_router(router)

    await setup_cron_jobs(bot)

    await dp.start_polling(bot)


logging.basicConfig(level=logging.INFO, stream=sys.stdout)
asyncio.run(main())