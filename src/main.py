from aiogram import Dispatcher, Bot
from settings import TOKEN
from handlers import router
import logging
import asyncio

bot = Bot(token=TOKEN)
dp = Dispatcher()
dp.include_router(router=router)
logging.basicConfig(level=logging.INFO)


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
