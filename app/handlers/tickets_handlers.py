from aiogram import Router, F
from aiogram.types import Message, LabeledPrice, CallbackQuery, PreCheckoutQuery
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import logging, random
import config, tickets

from main import bot
import app.keyboards as kb

# Router for ticket purchase
ticket_router = Router()
available = tickets.available_tickets


# State management for ticket purchase
class TicketStates(StatesGroup):
	choosing_quantity = State()


def get_event_photo():
	return random.choice(config.PHOTO_URL)


@ticket_router.message(Command('buy'))
async def buy(message: Message, state: FSMContext):
	if available == 0:
		await message.answer("Sorry, no more tickets are available for purchase.")
		await message.answer("But don't be upset, because we're about to announce a new party!")
		await message.answer("Follow us on Instagram to stay updated!")
		await message.answer(
			"https://www.instagram.com/uacommunity_gre?utm_source=ig_web_button_share_sheet&igsh=ZDNlZDc0MzIxNw==")
		return

	if available < 10:
		await message.answer(f"Hurry up! There are JUST {available} tickets left!")

	await message.answer(
		f"We have {available} tickets available. How many would you like to buy?",
		reply_markup=kb.get_quantity_keyboard(available)
	)
	await state.set_state(TicketStates.choosing_quantity)


@ticket_router.callback_query(F.data.startswith("quantity:"))
async def process_quantity_selection(callback: CallbackQuery, state: FSMContext):
	await callback.answer()
	quantity = int(callback.data.split(":")[1])
	if quantity > available:
		await callback.message.answer(f"Sorry, we only have {available} tickets available.")
		return

	# Store the selected quantity in the state
	await state.update_data(quantity=quantity)
	await callback.message.answer(f"You selected {quantity} ticket(s). Now processing payment...")

	total_price = quantity * config.TICKET_PRICE
	labeled_price = LabeledPrice(label=f"Party ticket x{quantity}", amount=total_price)
	logging.info(f"Sending to the invoice for quantity: {quantity}, Total price: {total_price}")
	await send_invoice(callback.message.chat.id, quantity, labeled_price)


async def send_invoice(chat_id, quantity, labeled_price):
	try:
		await bot.send_invoice(
			chat_id=chat_id,
			title="Ticket to the Paradise",
			description=f"Purchasing {quantity} entrance ticket(s) for Ukrainian Party",
			provider_token=config.PAYMENTS_TOKEN_TEST,
			currency=config.CURRENCY,
			prices=[labeled_price],
			photo_url=get_event_photo(),
			is_flexible=False,
			start_parameter="entrance-ticket1",
			payload=f"Payment_party1:{quantity}",
			need_email=True,
			allow_sending_without_reply=True,
		)
	except Exception as e:
		logging.error(f"Error sending invoice: {e}")
		await bot.send_message(chat_id,
		                       "Sorry, something went wrong while sending the invoice. Please try again later.")


@ticket_router.pre_checkout_query()
async def pre_checkout_handler(pre_checkout_query: PreCheckoutQuery):
	logging.info(f"Received pre-checkout query: {pre_checkout_query}")
	try:
		await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True, error_message=None)
		logging.info(f"Pre-checkout query answered for id: {pre_checkout_query.id}")
	except Exception as e:
		logging.error(f"Error answering pre-checkout query: {e}")


@ticket_router.message(F.successful_payment)
async def successful_payment(message: Message):
	logging.info(f"SUCCESSFUL PAYMENT: {message.successful_payment}")
	email = message.successful_payment.order_info.email
	purchased_quantity = int(message.successful_payment.invoice_payload.split(":")[-1])
	await bot.send_message(
		config.ADMIN,
		f"@{message.from_user.username} ({message.from_user.full_name})\n{email}\nBought {purchased_quantity} ticket(s)!"
	)
	await bot.send_message(message.chat.id, text="Payment was successful!")
