from sqlalchemy import BigInteger, String, ForeignKey, LargeBinary, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from typing import List, Optional
from config import SQLAlCHEMY_URL

engine = create_async_engine(url=SQLAlCHEMY_URL)

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
	pass


class User(Base):
	__tablename__ = "users"

	id: Mapped[int] = mapped_column(primary_key=True)
	tg_id = mapped_column(BigInteger)
	username: Mapped[str] = mapped_column(String)
	email:Mapped[str]=mapped_column(String, nullable=True)
	my_events:Mapped[Optional[List["Event"]]]=relationship(
		back_populates="people",
		secondary="participants"
	)


class Event(Base):
	__tablename__ = "events"

	id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
	poster: Mapped[str] = mapped_column()
	name: Mapped[str] = mapped_column(String(32))
	description: Mapped[str] = mapped_column(String(1000))
	price: Mapped[int] = mapped_column(insert_default=0)
	payment_link: Mapped[str] = mapped_column(nullable=True)
	date = mapped_column(DateTime)
	available: Mapped[int] = mapped_column()
	participants: Mapped[int] = mapped_column(insert_default=0)
	people:Mapped[Optional[List["User"]]]=relationship(
		back_populates="my_events",
		secondary="participants"
	)


class UserEvents(Base):
	__tablename__ = "participants"

	user_id:Mapped[int]=mapped_column(
		ForeignKey("users.id"),
		primary_key=True
	)

	event_id:Mapped[int]=mapped_column(
		ForeignKey("events.id"),
		primary_key=True
	)


async def asyncmain():
	async with engine.begin() as conn:
		await conn.run_sync(Base.metadata.create_all)
