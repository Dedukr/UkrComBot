import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, LabeledPrice, CallbackQuery, PreCheckoutQuery, SuccessfulPayment
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.keyboard import InlineKeyboardBuilder

import tickets, config, logging

bot = Bot(config.TOKEN)
dp = Dispatcher(storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)

class TicketStates(StatesGroup):
	choosing_quantity = State()


TICKET_PRICE = 1000
CURRENCY = "GBP"
available = tickets.available_tickets


def get_quantity_keyboard(available_tickets):
	kb = InlineKeyboardBuilder()
	for i in range(1, min(available_tickets, 10) + 1):
		kb.button(text=f"{i}", callback_data=f"quantity:{i}")
	return kb.as_markup()


@dp.message(Command('buy'))
async def buy(message: Message, state: FSMContext):
	if available == 0:
		await message.answer("Sorry, no more tickets are available for purchase.")
		await message.answer("But dont be upset, cause we are about to make a new party!")
		await message.answer("Follow us on instagram to be up to date!")
		await message.answer(
			"https://www.instagram.com/uacommunity_gre?utm_source=ig_web_button_share_sheet&igsh=ZDNlZDc0MzIxNw==")
		return

	if available < 10:
		await message.answer(f"Hurry UP!!! There are JUST {available} LEFT")

	await message.answer(
		f"We have {available} tickets available. How many would you like to buy?",
		reply_markup=get_quantity_keyboard(available)
	)
	# if available > 10:
	# 	await message.answer("Notice: you cant buy more than 10 tickets per transaction!")
	await state.set_state(TicketStates.choosing_quantity)


@dp.callback_query(F.data.startswith("quantity:"))
async def process_payment(callback: CallbackQuery, state: FSMContext):
	await callback.answer()
	quantity = int(callback.data.split(":")[1])
	if quantity > available:
		await callback.message.answer(f"Sorry we have got just {available} available tickets")
		return
	total_price = quantity * TICKET_PRICE
	labeled_price = LabeledPrice(label=f"Party ticket x{quantity}", amount=total_price)
	logging.info(f"Sending payment for quantity: {quantity}, Total price: {total_price}")
	await bot.send_invoice(callback.message.chat.id,
	                       title="Ticket to the paradise",
	                       description=f"Purchasing {quantity} entrance ticket(s) for Ukrainian Party",
	                       provider_token=config.PAYMENTS_TOKEN_TEST,
	                       currency=CURRENCY,
	                       prices=[labeled_price],
	                       photo_url="https://t4.ftcdn.net/jpg/00/42/30/93/360_F_42309347_iWqZ6mPcYq6jqVT5SiHVTvBq7mL5Gryp.jpg",
	                       is_flexible=False,
	                       start_parameter="entrance-ticket1",
	                       payload=f"Payment_party1:{quantity}",
	                       need_email=True,
	                       need_name=False,
	                       need_phone_number=False,
	                       need_shipping_address=False,
	                       allow_sending_without_reply=True,
	                       )
	await state.clear()


@dp.pre_checkout_query(F(lambda query: True))
async def pre_checkout_query(pre_check_q: PreCheckoutQuery):
	logging.info(f"Received payment: {pre_check_q}")
	await bot.answer_pre_checkout_query(pre_check_q.id, ok=True)


@dp.message(F.successful_payment)
async def successful_payment(message: Message):
	logging.info(f"SUCCESSFUL PAYMENT: {message.successful_payment}")
	email = message.successful_payment.order_info.email
	purchased_quantity = int(message.successful_payment.invoice_payload.split(":")[-1])
	print(purchased_quantity)
	await bot.send_message(config.ADMIN,
	                       f"@{message.from_user.username}({message.from_user.full_name})\n{email}\nBought a ticket!")
	await bot.send_message(message.chat.id, text=f"Payment was successful!")


@dp.message()
async def echo(message: Message):
	logging.info(f"Unhandled message: {message.text}")
	await message.answer("This command is not handled yet.")


async def main():
	await dp.start_polling(bot)


if __name__ == '__main__':
	try:
		asyncio.run(main())
	except KeyboardInterrupt:
		print('Exit')
