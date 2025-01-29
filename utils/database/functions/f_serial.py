from sqlalchemy import select, func, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from utils.database.models import Serial, Kino
from utils.database.models import engine, Qism

async def create_serial(serial_nomi):
    async with AsyncSession(engine) as session:  # AsyncSession yaratish
        try:
            new_serial = Serial(serial_nomi=serial_nomi)
            session.add(new_serial)
            await session.commit()  # O'zgarishlarni bazaga yuborish
            return new_serial
        except Exception as e:
            await session.rollback()
            raise e
async def create_qism(
    kod: int,
    tizer_message_id: int,
    asosiy_tizer_message_id: int,
    kino_message_id: int,
    serial_nomi: str,
    serial_info: str,
    serial_hajmi: str,
    serial_id: int
) -> Qism:
    async with AsyncSession(engine) as session:
        try:
            # Qism obyekti yaratish
            new_qism = Qism(
                kod=kod,
                tizer_message_id=tizer_message_id,
                asosiy_tizer_message_id=asosiy_tizer_message_id,  # Yangi ustun
                kino_message_id=kino_message_id,
                serial_nomi=serial_nomi,
                serial_info=serial_info,
                serial_hajmi=serial_hajmi,
                serial_id=serial_id
            )
            # Obyektni sessiyaga qo'shish
            session.add(new_qism)
            await session.commit()  # O'zgarishlarni bazaga saqlash
            await session.refresh(new_qism)  # Yaratilgan obyektni yangilash
            return new_qism
        except SQLAlchemyError as e:
            await session.rollback()  # Xatolik bo'lsa, rollback qilish
            raise e
async def fetch_all_serials():
    async with AsyncSession(engine) as session:
        query = select(Serial)
        result = await session.execute(query)
        serials = result.scalars().all()
        return serials

async def count_serial_parts(serial_id: int) -> int:
    async with AsyncSession(engine) as session:
        try:
            result = await session.execute(
                select(func.count(Qism.id)).where(Qism.serial_id == serial_id)
            )
            parts_count = result.scalar()
            return parts_count if parts_count is not None else 0
        except Exception as e:
            print(f"Xatolik yuz berdi: {str(e)}")
            return 0

async def fetch_serial_parts(serial_id):
    if not isinstance(serial_id, int):
        print(f"Invalid serial_id type: {type(serial_id)}")
        return []
    async with AsyncSession(engine) as session:
        try:
            result = await session.execute(
                select(Qism).where(Qism.serial_id == serial_id)
            )
            parts = result.scalars().all()
            return parts
        except Exception as e:
            print(f"Xatolik yuz berdi: {str(e)}")
            return []
async def fetch_serial_by_id(serial_id: int):
    async with AsyncSession(engine) as session:
        try:
            result = await session.execute(select(Serial).where(Serial.serial_id == serial_id))
            serial = result.scalars().first()  # Agar serial topilsa, birinchi topilgan ob'ektni qaytaradi
            return serial
        except Exception as e:
            print(f"Xatolik yuz berdi: {str(e)}")
            return None
async def check_qism_exists(serial_id: int, kino_nomi: str) -> bool:
    async with AsyncSession(engine) as session:
        result = await session.execute(
            select(Qism).where(Qism.serial_id == serial_id, Qism.serial_nomi == kino_nomi)
        )
        existing_qism = result.scalars().first()
        return existing_qism is not None
async def get_serial_name_by_id(serial_id: int) -> str:
    async with AsyncSession(engine) as session:
        result = await session.execute(
            select(Serial.serial_nomi).where(Serial.serial_id == serial_id)
        )
        serial_nomi = result.scalar()
        return serial_nomi
async def get_all_qism_names_by_serial_id(serial_id: int) -> list[str]:
    async with AsyncSession(engine) as session:
        result = await session.execute(
            select(Qism.serial_nomi).where(Qism.serial_id == serial_id)
        )
        qism_names = result.scalars().all()  # Barcha nomlarni olish
        return qism_names

async def delete_serial_and_parts(serial_id: int) -> bool:
    async with AsyncSession(engine) as session:
        try:
            async with session.begin():
                await session.execute(
                    delete(Qism).where(Qism.serial_id == serial_id)
                )
                await session.execute(
                    delete(Serial).where(Serial.serial_id == serial_id)
                )

            return True  # Muvaffaqiyatli bajarilgan
        except Exception as e:
            print(f"Xatolik yuz berdi: {e}")
            return False  # Xatolik yuz bergan
async def fetch_parts_by_serial_id(serial_id: int) -> list:
    async with AsyncSession(engine) as session:
        result = await session.execute(
            select(Qism).where(Qism.serial_id == serial_id)
        )
        return result.scalars().all()
async def update_serial_name(serial_id: int, new_name: str) -> Serial:
    async with AsyncSession(engine) as session:
        result = await session.execute(
            select(Serial).where(Serial.serial_id == serial_id)
        )
        serial = result.scalar_one_or_none()
        if serial:
            serial.serial_nomi = new_name
            await session.commit()
            await session.refresh(serial)
            return serial
        else:
            raise ValueError("Serial topilmadi.")
async def get_serial_by_id(serial_id: int):
    async with AsyncSession(engine) as session:
        result = await session.execute(
            select(Serial).where(Serial.serial_id == serial_id)
        )
        serial = result.scalar_one_or_none()  # Agar topilsa, birinchi natijani qaytaradi
        return serial
async def get_part_by_id(part_id: int):
    async with AsyncSession(engine) as session:
        result = await session.execute(
            select(Qism).where(Qism.id == int(part_id))
        )
        return result.scalar_one_or_none()
async def get_part_by_id1(part_id: int):
    async with AsyncSession(engine) as session:
        result = await session.execute(
            select(Qism).where(Qism.kod == int(part_id))
        )
        return result.scalar_one_or_none()
async def delete_part_by_id(part_id: int) -> bool:
    async with AsyncSession(engine) as session:
        result = await session.execute(
            select(Qism).where(Qism.id == part_id)
        )
        part = result.scalar_one_or_none()

        if part:
            await session.delete(part)
            await session.commit()
            return True
        return False
async def update_part_name_in_db(part_id: int, new_name: str) -> bool:
    async with AsyncSession(engine) as session:
        result = await session.execute(
            select(Qism).where(Qism.id == part_id)
        )
        part = result.scalar_one_or_none()

        if part:
            part.serial_nomi = new_name
            await session.commit()
            return True
        return False
async def update_part_info_in_db(part_id: int, new_info: str) -> bool:
    async with AsyncSession(engine) as session:
        result = await session.execute(
            select(Qism).where(Qism.id == part_id)
        )
        part = result.scalar_one_or_none()
        if part:
            part.serial_info = new_info
            await session.commit()
            return True
        return False
async def delete_part_by_id1(part_id: int) -> bool:
    async with AsyncSession(engine) as session:
        result = await session.execute(
            select(Qism).where(Qism.id == part_id)
        )
        part = result.scalar_one_or_none()

        if part:
            await session.delete(part)
            await session.commit()
            return True
        return False
async def check_kino_id(kino_id: int) -> str:
    async with AsyncSession(engine) as session:
        kino_query = await session.execute(select(Kino).where(Kino.kod == kino_id))
        kino_result = kino_query.scalar_one_or_none()
        if kino_result:
            return f"kino_{kino_id}"
        qism_query = await session.execute(select(Qism).where(Qism.kod == kino_id))
        qism_result = qism_query.scalar_one_or_none()
        if qism_result:
            return f"serial_{kino_id}"
        raise ValueError("kino_id na Kino, na Qism jadvalida topilmadi")
async def check_kino_id1(kino_id):
    async with AsyncSession(engine) as session:
        kino = await session.execute(select(Kino).where(Kino.kod == kino_id))
        if kino.scalar():
            return "kino"

        serial = await session.execute(select(Qism).where(Qism.kod == kino_id))
        if serial.scalar():
            return "serial"

    return None  # Agar hech narsa topilmasa

async def fetch_serial_parts1(kod):
    async with AsyncSession(engine) as session:
        result = await session.execute(select(Qism).where(Qism.kod == kod))
        qism = result.scalar_one_or_none()
        if qism:
            serial_id = qism.serial_id
            serial_parts_result = await session.execute(select(Qism).where(Qism.serial_id == serial_id))
            return serial_parts_result.scalars().all()
    return []

async def get_serial_id(qism_id: int) -> int:
    async with AsyncSession(engine) as session:
        query = await session.execute(select(Qism.serial_id).where(Qism.kod == qism_id))
        serial_id = query.scalar_one_or_none()
        if not serial_id:
            raise ValueError("Serial ID topilmadi")
        return serial_id

async def get_serial_parts(serial_id: int):
    async with AsyncSession(engine) as session:
        query = await session.execute(select(Qism).where(Qism.serial_id == serial_id))
        return query.scalars().all()
