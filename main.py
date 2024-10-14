import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

import config, logging
from app.handlers import tickets_handlers
from app.handlers import handlers

# Initialize bot, dispatcher, and routers
bot = Bot(config.TOKEN)
dp = Dispatcher(storage=MemoryStorage())

logging.basicConfig(level=logging.INFO)


# Main function to start the bot
async def main():
	try:
		# Include ticket-related router
		dp.include_router(tickets_handlers.ticket_router)
		# Include the router in the dispatcher
		dp.include_router(handlers.router)
		await bot.send_message(config.DEV, "Bot started")
		await dp.start_polling(bot)
	finally:
		await bot.session.close()  # Close the bot session to avoid issues
		logging.info("Bot shut down gracefully")


if __name__ == '__main__':
	try:
		asyncio.run(main())
	except KeyboardInterrupt:
		print('Bot stopped manually')
