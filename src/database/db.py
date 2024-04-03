from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine
from src.conf.config import config


class DataBaseSessionManager:
    def __init__(self, url: str):
        self._engine: AsyncEngine | None = create_async_engine(url, echo=False)  # Создание движка
        self._session_maker: async_sessionmaker = async_sessionmaker(autocommit=False, autoflush=False,
                                                                     bind=self._engine)  # Фабрика сессий

    @asynccontextmanager  # декоратор, который превращает функцию в менеджер контекста
    async def session(self):
        if self._session_maker is None:  # проверка, что фабрика сессий была инициализирована.
            raise Exception("Session is not initialized")
        session = self._session_maker()  # Создание новой сесии БД
        try:
            yield session
        except Exception as e:
            print(e)
            await session.rollback()
        finally:
            await session.close()


sessionmanager = DataBaseSessionManager(config.DB_URL)


async def get_db():
    async with sessionmanager.session() as session:
        yield session