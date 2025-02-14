# from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
# from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
# from sqlalchemy import BigInteger, String, Boolean

# engine = create_async_engine(url='sqlite+aiosqlite:///tmp/db.sqlite3')

# async_session = async_sessionmaker(engine)


# class Base(AsyncAttrs, DeclarativeBase):
#     pass


# class User(Base):
#     __tablename__ = 'users'

#     id: Mapped[int] = mapped_column(primary_key=True)
#     tg_id = mapped_column(BigInteger)
#     lvl: Mapped[str] = mapped_column(String(2))
#     status: Mapped[bool] = mapped_column(Boolean)


# async def async_main():
#     async with engine.begin() as connection:
#         await connection.run_sync(Base.metadata.create_all)

import asyncio
from google.cloud import firestore

db = firestore.Client()
users_ref = db.collection("users")

class User:
    @staticmethod
    async def create_user(tg_id: int):
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, lambda: users_ref.document(str(tg_id)).set({
            "lvl": "B1",
            "status": True
        }, merge=True))

    @staticmethod
    async def get_user(tg_id: int):
        loop = asyncio.get_running_loop()
        doc = await loop.run_in_executor(None, lambda: users_ref.document(str(tg_id)).get())
        return doc.to_dict() if doc.exists else None

    @staticmethod
    async def update_level(tg_id: int, new_lvl: str):
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, lambda: users_ref.document(str(tg_id)).update({"lvl": new_lvl}))

    @staticmethod
    async def get_active_users():
        loop = asyncio.get_running_loop()
        docs = await loop.run_in_executor(None, lambda: users_ref.where("status", "==", True).stream())
        return [doc.id for doc in docs]

    @staticmethod
    async def update_status(tg_id: int):
        loop = asyncio.get_running_loop()
        doc = await loop.run_in_executor(None, lambda: users_ref.document(str(tg_id)).get())
        if doc.exists:
            current_status = doc.to_dict().get("status", True)
            await loop.run_in_executor(None, lambda: users_ref.document(str(tg_id)).update({"status": not current_status}))

