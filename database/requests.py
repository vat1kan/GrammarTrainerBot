from database.models import async_session
from database.models import User
from sqlalchemy import select, update

async def set_user(tg_id: int) -> None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        
        if not user:
            session.add(User(tg_id=tg_id, lvl='B1', status = 1))
            await session.commit()

async def get_active_users():
    async with async_session() as session:
        active_users = await session.scalars(select(User.tg_id).where(User.status == 1))
        return active_users.all()

async def get_lvl(tg_id: int):
    async with async_session() as session:
        lvl = await session.scalar(select(User.lvl).where(User.tg_id == tg_id))
        return lvl
    
async def upd_level(tg_id: int, new_lvl: str):
    async with async_session() as session:
        stmt = update(User).where(User.tg_id == tg_id).values(lvl=new_lvl)
        await session.execute(stmt)
        await session.commit()

async def get_status(tg_id:int):
    async with async_session() as sessin:
        return await sessin.scalar(select(User.status).where(User.tg_id == tg_id))

async def upd_status(tg_id: int):
    async with async_session() as session:
        await session.execute(
        update(User)
        .where(User.tg_id == tg_id)
        .values(status=(1 - User.status)))
        await session.commit()