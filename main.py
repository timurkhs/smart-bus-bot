import logging
import asyncio
from aiogram import Bot, Dispatcher

import config as cf
logging.basicConfig(level=logging.INFO)
from app.handlers import router


async def main():
    bot = Bot(token=cf.TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')

        