from aiogram.utils.keyboard import InlineKeyboardBuilder


# Helper function for generating quantity keyboard
def get_quantity_keyboard(available_tickets):
	kb = InlineKeyboardBuilder()
	for i in range(1, min(available_tickets, 10) + 1):
		kb.button(text=f"{i}", callback_data=f"quantity:{i}")
	return kb.as_markup()
