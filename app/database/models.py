from sqlalchemy import BigInteger, String, ForeignKey, LargeBinary, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from config import SQLAlCHEMY_URL

engine = create_async_engine(url=SQLAlCHEMY_URL)

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
	pass


class User(Base):
	__tablename__ = "users"

	id: Mapped[int] = mapped_column(primary_key=True)
	tg_id = mapped_column(BigInteger)
	email: Mapped[str] = mapped_column(String, nullable=True)


# events:Mapped[list["Events"]] = relationship()


class Event(Base):
	__tablename__ = "events"

	id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
	poster: Mapped[str] = mapped_column()
	name: Mapped[str] = mapped_column(String(32))
	description: Mapped[str] = mapped_column(String(1000))
	price: Mapped[int] = mapped_column()
	payment_link: Mapped[str] = mapped_column(nullable=True)
	date = mapped_column(DateTime)
	available: Mapped[int] = mapped_column()
	# people: Mapped[list["User"]] = relationship()
	participants: Mapped[int] = mapped_column(default=0)


async def asyncmain():
	async with engine.begin() as conn:
		await conn.run_sync(Base.metadata.create_all)
