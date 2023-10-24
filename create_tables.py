import logging

from app.db.base_model import Base
from app.db.session import engine

logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)


async def create_tables() -> None:
    import app.models  # noqa
    logging.info("Creating tables...")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    logging.info("Tables created successfully.")


if __name__ == "__main__":
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_tables())
    loop.close()
