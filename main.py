import asyncio

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, CommandStart
from aiogram.types.message import ContentType

import config, logging


bot = Bot(config.TOKEN)
dp = Dispatcher()

async def main():
    await dp.start_polling(bot)


@dp.message()
async def echo(message:types.Message):
    await message.answer(message.text)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')