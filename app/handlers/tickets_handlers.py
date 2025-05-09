import stripe
from aiogram import Router, F
from aiogram.types import Message, LabeledPrice, CallbackQuery, PreCheckoutQuery
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import logging, random
import config

import app.keyboards as kb
import app.database.requests as rq

# Router for ticket purchase
ticket_router = Router()


# State management for ticket purchase
class TicketStates(StatesGroup):
	choosing_quantity = State()


@ticket_router.message(Command("events"))
async def events(message: Message):
    current_events = await rq.get_current_events()
    if current_events:
        for event in current_events:
            await message.answer_photo(photo=event.poster, reply_markup=kb.details(event.id))
    else:
        await message.answer("Ми зараз активно працюємо над створенням нових незабутніх івентів для вас")
        await message.answer("Слідкуйте за нами шоб дізнатися більше", reply_markup=kb.get_follow_keyboard())


@ticket_router.message(F.text == "Events")
async def events_from_keyboard(message: Message):
	await events(message)


@ticket_router.callback_query(F.data.startswith("details_"))
async def event_details(callback: CallbackQuery):
	await callback.answer()
	event_id = int(callback.data.split("_")[1])
	event = await rq.get_detailed_event(event_id)
	await callback.message.answer_photo(event.poster)
	await callback.message.answer(event.name)
	if event.price or event.payment_link:
		await callback.message.answer(text=f"Price: £{event.price}")
		await callback.message.answer(text=event.description,
									  reply_markup=await kb.get_payment(event_id, callback.from_user.id))
	else:
		await callback.message.answer(event.description, reply_markup=kb.register_me(event_id))


@ticket_router.callback_query(F.data.startswith("book_"))
async def book_attendance(callback: CallbackQuery):
	await callback.answer()
	event_id = int(callback.data.split("_")[1])
	event = await rq.get_detailed_event(event_id)
	await rq.add_participant(event_id)
	await callback.message.bot.send_message(chat_id=config.ADMIN,
	                                        text=f"{callback.message.date.strftime('%m/%d/%Y, %H:%M:%S')} - @{callback.from_user.username} {callback.from_user.full_name} ({callback.from_user.id})\nBooked a ticket for {event.name}!")
	with open(f"/home/ubuntu/bots/UkrComBot/{event.name}.log", "a") as f:
		f.write(f"{callback.message.date} - {callback.from_user.username} ({callback.from_user.id}) booked\n")
		f.flush()

	await callback.message.answer("Успішно заброньовано✅\nЗустрінемось на івенті!")

# @ticket_router.callback_query(F.date.startswith("buy_"))
# async def buy(callback: CallbackQuery, state: FSMContext):
# 	await callback.answer()
# 	event_id = int(callback.data.split("_")[1])
# 	event = await rq.get_detailed_event(event_id)
# 	if event.available == 0:
# 		await callback.message.answer("Sorry, no more tickets are available for purchase.")
# 		await callback.message.answer("But don't be upset, because we're about to announce a new party!")
# 		await callback.message.answer("Follow us on Instagram to stay updated!")
# 		await callback.message.answer(config.INSTA)
# 		return
#
# 	if event.available < 10:
# 		await callback.message.answer(f"Hurry up! There are JUST {event.available} tickets left!")
#
#
# 	await callback.message.answer(
# 		f"We have {event.available} tickets available. How many would you like to buy?",
# 		reply_markup=kb.get_quantity_keyboard(event.available, event_id))
# 	await state.set_state(TicketStates.choosing_quantity)


# @ticket_router.callback_query(F.data.startswith("quantity:"))
# async def process_quantity_selection(callback: CallbackQuery, state: FSMContext):
# 	await callback.answer()
# 	quantity = int(callback.data.split(":")[1])
# 	event_id = int(callback.data.split("_")[1])
# 	event = await rq.get_detailed_event(event_id)
# 	if quantity > event.available:
# 		await callback.message.answer(f"Sorry, now we only have {event.available} tickets available.")
# 		await callback.message.answer(
# 			f"We have {event.available} tickets available. How many would you like to buy?",
# 			reply_markup=kb.get_quantity_keyboard(event.available, event_id))
# 		await state.set_state(TicketStates.choosing_quantity)
# 		return
#
# 	# Store the selected quantity in the state
# 	await state.update_data(quantity=quantity)
# 	await callback.message.answer(f"You selected {quantity} ticket(s). Now processing the payment...")
#
# 	total_price = quantity * event.price


# labeled_price = LabeledPrice(label=f"Party ticket x{quantity}", amount=total_price)
# logging.info(f"Sending to the invoice for quantity: {quantity}, Total price: {total_price}")
# await send_invoice(callback.message, quantity, labeled_price)


# async def send_invoice(message, quantity, labeled_price):
# 	try:
# 		await message.send_invoice(
# 			title="Ticket to the Paradise",
# 			description=f"Purchasing {quantity} entrance ticket(s) for Ukrainian Party",
# 			provider_token=config.PAYMENTS_TOKEN_LIVE,
# 			currency=config.CURRENCY,
# 			prices=[labeled_price],
# 			max_tip_amount=config.TICKET_PRICE,
# 			suggested_tip_amounts=[100, 200, 500, 1000],
# 			photo_url=,
# 			is_flexible=False,
# 			start_parameter="entrance-ticket1",
# 			payload=f"Payment_party1:{quantity}",
# 			need_email=True,
# 			allow_sending_without_reply=True,
# 		)
# 	except Exception as e:
# 		logging.error(f"Error sending invoice: {e}")
# 		await message.send_message("Sorry, something went wrong while sending the invoice. Please try again later.")


# @ticket_router.pre_checkout_query()
# async def pre_checkout_handler(pre_checkout_query: PreCheckoutQuery):
# 	logging.info(f"Received pre-checkout query: {pre_checkout_query}")
# 	try:
# 		# await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)
# 		await pre_checkout_query.answer(True)
# 		logging.info(f"Pre-checkout query answered for id: {pre_checkout_query.id}")
# 	except Exception as e:
# 		logging.error(f"Error answering pre-checkout query: {e}")
#
# 	logging.info("success sent")
#
#
# @ticket_router.message(F.successful_payment)
# async def successful_payment(message: Message):
# 	logging.info(f"SUCCESSFUL PAYMENT: {message.successful_payment}")
# 	email = message.successful_payment.order_info.email
# 	purchased_quantity = int(message.successful_payment.invoice_payload.split(":")[-1])
# 	await message.send_message(
# 		config.ADMIN,
# 		f"@{message.from_user.username} ({message.from_user.full_name})\n{email}\nBought {purchased_quantity} ticket(s)!"
# 	)
# 	await message.answer(text="Payment was successful!")
# 	tickets.available_tickets -= int(message.successful_payment.total_amount / config.TICKET_PRICE)
