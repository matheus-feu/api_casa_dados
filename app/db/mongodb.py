import logging

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.core.settings import settings


async def get_mongo_db() -> AsyncIOMotorDatabase:
    mongo_client = AsyncIOMotorClient(settings.mongodb_uri)
    return mongo_client['casa_dados']


async def connect_to_database(path: str):
    """
    Conecta ao banco de dados MongoDB.

    Args:
        path (str): A URL de conexão com o MongoDB.

    Returns:
        AsyncIOMotorClient: O cliente do MongoDB conectado.
    """
    try:
        logging.info("Connecting to MongoDB...")
        mongo_client = AsyncIOMotorClient(path)
        logging.info("Connected to MongoDB.")
        return mongo_client
    except Exception as e:
        logging.error(f"Failed to connect to MongoDB: {str(e)}")
        raise


async def close_database_connection(client: AsyncIOMotorClient):
    """
    Fecha a conexão com o banco de dados MongoDB.

    Args:
        client (AsyncIOMotorClient): O cliente do MongoDB.
    """
    try:
        logging.info("Closing MongoDB connection...")
        client.close()
        logging.info("MongoDB connection closed.")
    except Exception as e:
        logging.error(f"Failed to close MongoDB connection: {str(e)}")
        raise
