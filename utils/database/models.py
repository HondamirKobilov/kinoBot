from asyncpg import DuplicateDatabaseError, connect
from sqlalchemy import Column, String, Boolean, DateTime, BigInteger, VARCHAR, Integer
from sqlalchemy import ForeignKey
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from data.config import *
DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
engine = create_async_engine(DATABASE_URL, pool_size=200, max_overflow=2000)
Base = declarative_base()

async def create_database(db_name=DB_NAME):
    conn_info = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/postgres'

    conn = await connect(conn_info)

    try:
        await conn.execute(f'CREATE DATABASE {db_name}')
        print(f'Database {db_name} created successfully.')
    except DuplicateDatabaseError:
        print(f'Database {db_name} already exists.')
    except Exception as e:
        print(f'An error occurred: {e}')
    finally:
        await conn.close()

class User(Base):
    __tablename__ = 'users'
    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, unique=True)
    fullname = Column(String)
    phone = Column(String, nullable=True)
    username = Column(String, nullable=True)
    is_blocked = Column(Boolean, nullable=False, default=False)
    is_premium = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, default=toshkent_now())
    updated_at = Column(DateTime, default=toshkent_now())

class Kino(Base):
    __tablename__ = 'kino'
    id = Column(Integer, primary_key=True, autoincrement=True)  # Asosiy kalit
    kod = Column(Integer, unique=True)
    tizerMessage_id = Column(Integer, unique=True)
    asosiy_tizer_message_id = Column(Integer, unique=True)
    kinoMessage_id = Column(BigInteger, unique=True)
    kino_nomi = Column(String)
    kino_info = Column(String)
    kino_hajmi = Column(String)
class Serial(Base):
    __tablename__ = 'seriallar'
    serial_id = Column(Integer, primary_key=True)
    serial_nomi = Column(String, unique=True)
    qismlar = relationship("Qism", back_populates="serial")

class Qism(Base):
    __tablename__ = 'qismlar'
    id = Column(Integer, primary_key=True, autoincrement=True)  # Asosiy kalit
    kod = Column(Integer, unique=True)
    tizer_message_id = Column(Integer, unique=True)
    asosiy_tizer_message_id = Column(Integer, unique=True)
    kino_message_id = Column(BigInteger, unique=True)
    serial_nomi = Column(String)
    serial_info = Column(String)
    serial_hajmi = Column(String)
    serial_id = Column(Integer, ForeignKey('seriallar.serial_id'))
    serial = relationship("Serial", back_populates="qismlar")