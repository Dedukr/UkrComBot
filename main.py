import asyncio

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, CommandStart
from aiogram.types.message import ContentType

import config, logging


bot = Bot(config.TOKEN)
dp = Dispatcher()

async def main():
    await dp.start_polling(bot)

PRICE = [
    types.LabeledPrice(label="Entrance Ticket", amount=1000),
]# in coins

@dp.message(Command('buy'))
async def buy(message:types.Message):
    currency="GBP"
    await bot.send_invoice(message.chat.id,

                           title="Ticket to the paradise",
                           description="Purchasing an entrance ticket for Ukrainian Party",
                           provider_token=config.PAYMENTS_TOKEN_TEST,
                           currency=currency,
                           photo_url="https://t4.ftcdn.net/jpg/00/42/30/93/360_F_42309347_iWqZ6mPcYq6jqVT5SiHVTvBq7mL5Gryp.jpg",
                           is_flexible=False,
                           prices=PRICE,
                           start_parameter="entrance-ticket1",
                           payload="Payment_party1",
                           need_email=True,
                           need_name=False,
                           need_phone_number=False,
                           need_shipping_address=False,
                           allow_sending_without_reply=True,

                           )

@dp.pre_checkout_query(lambda query:True)
async def pre_checkout_query(pre_check_q:types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_check_q.id, ok=True)

@dp.message(F.successful_payment)
async def successful_payment(message:types.Message):
    logging.info(f"SUCCESSFUL PAYMENT: {message.successful_payment}")
    email = message.successful_payment.order_info.email
    await bot.send_message(config.ADMIN, f"@{message.from_user.username}({message.from_user.full_name})\n{email}\nBought a ticket!")
    await bot.send_message(message.chat.id, text=f"Payment was successful!")
@dp.message()
async def echo(message:types.Message):
    await message.answer(message.text)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')