import datetime

from app.database.models import async_session
from app.database.models import User, Event
from sqlalchemy import select, update, delete


async def set_user(tg_id, email):
	async with async_session() as session:
		user = await session.scalar(select(User).where(User.tg_id == tg_id))

		if not user:
			session.add((User(tg_id=tg_id, email=email)))
			await session.commit()


async def get_current_events():
	async with async_session() as session:
		return await session.scalars(select(Event).where(Event.date > datetime.datetime.now()))


async def get_detailed_event(event_id: int):
	async with async_session() as session:
		return await session.scalar(select(Event).where(Event.id == event_id))


async def add_participant(event_id: int):
	async with async_session() as session:
		async with session.begin():
			await session.execute(
				update(Event).where(Event.id == event_id).values(participants=Event.participants + 1)
			)
			await session.commit()
