from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from settings import Settings

settings = Settings()

DATABASE_URL = settings.mysql_url
engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession
)

Base = declarative_base()