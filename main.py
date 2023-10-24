import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.routers import api_router
from app.core.settings import settings
from app.db.mongodb import connect_to_database, close_database_connection

logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await connect_to_database(path=settings.mongodb_uri)
        yield
    finally:
        close_database_connection(app).close()


app = FastAPI(
    title=settings.project_name,
    version=settings.app_version,
    debug=settings.debug,
    description=settings.project_description,
    lifespan=lifespan
)

app.include_router(api_router, prefix=settings.app_v1_prefix)

if __name__ == "__main__":
    import uvicorn

    logging.info("Initializing server...")
    logging.info("Swagger UI available at http://localhost:8000/docs")

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=settings.debug)
