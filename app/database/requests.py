import datetime

from sqlalchemy import delete, select, update

import config
from app.database.models import Event, User, async_session


async def set_user(message, tg_id, username):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if not user:
            session.add((User(tg_id=tg_id, username=username)))
            await session.commit()
            await message.bot.send_message(
                chat_id=config.ADMIN,
                text=f"New Customer @{message.from_user.username} ({message.from_user.full_name})",
            )


async def get_current_events():
    async with async_session() as session:
        result = await session.execute(
            select(Event).where(Event.date > datetime.datetime.now())
        )
        return result.scalars().all()


async def get_detailed_event(event_id: int):
    async with async_session() as session:
        return await session.scalar(select(Event).where(Event.id == event_id))


async def get_payment_link(event_id: int):
    async with async_session() as session:
        return await session.scalar(
            select(Event.payment_link).where(Event.id == event_id)
        )


async def add_participant(event_id: int):
    async with async_session() as session:
        async with session.begin():
            await session.execute(
                update(Event)
                .where(Event.id == event_id)
                .values(participants=Event.participants + 1)
            )
            await session.commit()
