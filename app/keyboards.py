from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
import config
from app.database.requests import get_payment_link


def get_basic_keyboard():
	kb = ReplyKeyboardMarkup(keyboard=
	[
		[KeyboardButton(text="Events")],
		[KeyboardButton(text="About"), KeyboardButton(text="Contact Us")]
	], resize_keyboard=True,
		input_field_placeholder="Choose an option")
	return kb


def details(event_id):
	kb = InlineKeyboardMarkup(inline_keyboard=[
		[
			InlineKeyboardButton(text="Details", callback_data=f"details_{event_id}")
		]
	])
	return kb


def register_me(event_id):
	kb = InlineKeyboardMarkup(inline_keyboard=[
		[InlineKeyboardButton(text="Забронювати!", callback_data=f"book_{event_id}")]
	])
	return kb


def buy_tickets(event_id):
	kb = InlineKeyboardMarkup(inline_keyboard=[
		[InlineKeyboardButton(text="Купити!", callback_data=f"buy_{event_id}")]
	])
	return kb

async def get_payment(event_id, tg_id):
	kb = InlineKeyboardMarkup(inline_keyboard=[
		[InlineKeyboardButton(text="Buy", url=f"{await get_payment_link(event_id)}?client_reference_id={tg_id}")]
	])
	return kb


def get_quantity_keyboard(available_tickets, event_id):
	kb = InlineKeyboardBuilder()
	for i in range(1, min(available_tickets, 10) + 1):
		kb.button(text=f"{i}", callback_data=f"quantity_{event_id}:{i}")
	kb.adjust(1, 2, 3, 4)
	return kb.as_markup()


def get_follow_keyboard():
	kb = InlineKeyboardMarkup(inline_keyboard=[
		[
			InlineKeyboardButton(text="Instagram", url=config.INSTA),
			InlineKeyboardButton(text="UkrCom Chanel", url=config.TG_CHANEL),
		],
		[InlineKeyboardButton(text="University Chat", url=config.TG_ALL)]
	])
	return kb


def get_contacts():
	kb = InlineKeyboardMarkup(inline_keyboard=[
		[
			InlineKeyboardButton(text="Instagram", url=config.INSTA),
			InlineKeyboardButton(text="Telegram", url=config.TG_ADMIN)
		]
	])
	return kb
