from typing import Annotated

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

engine = create_async_engine("sqlite+aiosqlite:///recipes.db")
Session = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


idpk = Annotated[int, mapped_column(primary_key=True)]


class Recipes(Base):
    __tablename__ = "recipes"

    id: Mapped[idpk]
    title: Mapped[str] = mapped_column(nullable=False)
    views: Mapped[int] = mapped_column(default=0)
    cooking_time: Mapped[int] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    ingredients: Mapped[str] = mapped_column(nullable=False)
