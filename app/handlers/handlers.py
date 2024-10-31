from aiogram import Router, F
from aiogram.types import Message
from aiogram.types.input_file import InputFile
from aiogram.filters import Command, CommandStart
import logging, config

import app.keyboards as kb
import app.database.requests as rq

router = Router()


@router.message(CommandStart())
async def start(message: Message):
	await rq.set_user(message.from_user.id, message.from_user.username)
	await message.answer_photo(photo=config.LOGO)
	await message.answer(
		"""Ukrainian Community🇺🇦 in London — це енергійна і дружня спільнота українців, яка влаштовує незабутні вечірки та соціальні заходи в самому серці Лондона🔥 
Ми створюємо атмосферу справжнього свята, де можна поринути в рідну культуру, знайти нових друзів, і, звісно ж, добре відпочити.""",
		reply_markup=kb.get_basic_keyboard()
	)
	# await message.answer(
	# 	"Наші заходи — це не просто вечірки. Це події, які об’єднують людей, створюють спогади та дарують відчуття єдності. Ми організовуємо яскраві тематичні заходи, де лунає українська музика, відбуваються танці, конкурси і спеціальні сюрпризи. Також ми проводимо благодійні зустрічі, вечори української культури та інші події, що дозволяють підтримувати зв’язок з батьківщиною і робити щось важливе для нашої спільноти.")
	await message.answer(
		"Приєднуйтесь до нас і станьте частиною незабутніх подій, де українська душа оживає в самому серці Лондона!🤩",
		reply_markup=kb.get_follow_keyboard()
	)


@router.message(F.text == "About")
async def about(message: Message):
	await start(message)


@router.message(F.text == "Contact Us")
async def contact(message: Message):
	await message.answer("Ukrainian Community🇺🇦завжди відкрите для спілкування у разі виникнення якихось проблем або питаннь")
	await message.answer("Також будемо дуже раді якщо ви поділитися з нами вашими враженнями або ідеями на наступні івенти. Ми прислуховуємось до Вас і хочемо зробити все найкраще, аби ви отримали незабутні враження від нашої діяльності")
	await message.answer("PS: Якщо у вас є бажання допомогти нашій команді ви можете навіть приєднатися до нас!")
	await message.answer(
		text="Пишіть нам в телеграм або в особисті повідомлення в інстаграмі",
		reply_markup=kb.get_contacts())


# General fallback handler for unhandled messages
@router.message()
async def unhandled_message(message: Message):
	logging.info(f"Unhandled message: {message.text}")
	with open("unhandled.log", "a") as f:
		f.write(f"{message.date} - {message.from_user.username} unhandled: {message.text}\n")
		f.flush()
	await message.answer("I don't know what you're talking about mate...")
