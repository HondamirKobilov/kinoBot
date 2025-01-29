from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from utils.database.models import engine, Kino, Qism


# Kino yaratish
async def create_kino(
    kod: int,
    tizer_message_id: int,
    asosiy_tizer_message_id: int,
    kino_message_id: int,
    kino_nomi: str,
    kino_info: str,
    kino_hajmi: str
) -> Kino:
    async with AsyncSession(engine) as session:
        async with session.begin():
            try:
                new_kino = Kino(
                    kod=kod,
                    tizerMessage_id=tizer_message_id,
                    asosiy_tizer_message_id=asosiy_tizer_message_id,  # Yangi ustun
                    kinoMessage_id=kino_message_id,
                    kino_nomi=kino_nomi,
                    kino_info=kino_info,
                    kino_hajmi=kino_hajmi
                )
                session.add(new_kino)
                await session.flush()
                await session.refresh(new_kino)
                return new_kino

            except SQLAlchemyError as e:
                await session.rollback()
                print(f"Xatolik yuz berdi: {e}")
                raise e
async def get_all_kinolar():
    async with AsyncSession(engine) as session:
        result = await session.execute(select(Kino))
        kinolar = result.scalars().all()
        return kinolar

# Kino mavjudligini tekshirish (nomi bo'yicha)
async def check_kino_exists(kino_nomi):
    async with AsyncSession(engine) as session:
        result = await session.execute(select(Kino).filter(Kino.kino_nomi == kino_nomi))
        kino = result.scalars().first()
        return kino is not None

# Kino olish (kod bo'yicha)
async def get_kino_by_kod(kod):
    async with AsyncSession(engine) as session:
        result = await session.execute(select(Kino).filter(Kino.kod == int(kod)))
        kino = result.scalars().first()
        return kino

# Kino yangilash
async def update_kino(kino_kod: int, **kwargs):
    async with AsyncSession(engine) as session:
        result = await session.execute(select(Kino).where(Kino.kod == kino_kod))
        kino = result.scalar_one_or_none()
        if kino:
            for key, value in kwargs.items():
                if hasattr(kino, key):
                    setattr(kino, key, value)
            await session.commit()
            return kino
        else:
            return None

# Kino o'chirish
async def delete_kino_by_kod(kino_kod: int):
    async with AsyncSession(engine) as session:
        result = await session.execute(select(Kino).where(Kino.kod == kino_kod))
        kino = result.scalar_one_or_none()
        if kino:
            await session.delete(kino)
            await session.commit()
            return True
        return False

# Kino mavjudligini tekshirish (kod bo'yicha)
async def kino_exists(kino_kod):
    kino = await get_kino_by_kod(kino_kod)
    if kino:
        return True, kino
    else:
        return False, None

async def get_tizer_message_id_by_tizer_id(tezer_id: int) -> int:
    async with AsyncSession(engine) as session:
        kino_query = select(Kino).filter(Kino.kod == tezer_id)
        kino_result = await session.execute(kino_query)
        kino = kino_result.scalars().first()
        if kino:
            return kino.tizerMessage_id
        qism_query = select(Qism).filter(Qism.kod == tezer_id)
        qism_result = await session.execute(qism_query)
        qism = qism_result.scalars().first()
        if qism:
            return qism.tizer_message_id
        return None
