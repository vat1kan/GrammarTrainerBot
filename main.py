import os
import sys
import logging
import asyncio
from quart import Quart, request, jsonify
from aiogram import Bot, Dispatcher
from aiogram.types import Update
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from botapp.handlers import router, auto_quiz_sending, auto_word_sending
#from database.models import async_main

bot = Bot(token=os.getenv("grammarBot"), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
dp.include_router(router)

app = Quart(__name__)

@app.route("/")
async def home():
    return "Бот работает!"

@app.route("/webhook", methods=["POST"])
async def webhook():
    try:
        update_data = await request.get_json()
        logging.info(f"Received update: {update_data}")

        update = Update.model_validate(update_data)

        asyncio.create_task(dp.feed_update(bot, update))
        return "ok", 200
    except Exception as e:
        logging.error(f"Webhook error: {e}")
        return "Internal Server Error", 500

async def on_startup():
    #await async_main()
    #await setup_cron_jobs(bot) 
    await bot.set_webhook("https://grammarbot-450711.lm.r.appspot.com/")
    logging.info("Бот запущен: вебхук установлен, база и рассылка настроены.")


@app.route("/run_quiz_sending", methods=["POST"])
async def run_quiz_sending():
    asyncio.create_task(auto_quiz_sending(bot))
    return jsonify({"status": "Quiz sending started"}), 200

@app.route("/run_word_sending", methods=["POST"])
async def run_word_sending():
    asyncio.create_task(auto_word_sending(bot))
    return jsonify({"status": "Word sending started"}), 200


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(on_startup())

    from gunicorn.app.base import BaseApplication

    class UvicornServer(BaseApplication):
        def __init__(self, app, host="0.0.0.0", port=8080):
            self.options = {
                "bind": f"{host}:{port}",
                "workers": 1,
                "worker_class": "uvicorn.workers.UvicornWorker",
            }
            self.app = app
            super().__init__()

        def load_config(self):
            pass

        def load(self):
            return self.app

    UvicornServer(app).run()
