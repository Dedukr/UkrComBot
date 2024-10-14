from aiogram import Router
from aiogram.types import Message
import logging

router = Router()


# General fallback handler for unhandled messages
@router.message()
async def unhandled_message(message: Message):
	logging.info(f"Unhandled message: {message.text}")
	await message.answer("This command is not handled yet.")
