import re

from fastapi import APIRouter, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from starlette import status
from starlette.responses import JSONResponse

from app.core.deps import get_current_user
from app.db.mongodb import get_mongo_db
from app.exceptions.exception_auth import NotAuthenticatedException
from app.helpers.create_excel import create_excel
from app.helpers.scraping_casa_dados import scraper
from app.models import UserModel
from app.schemas.schema_scraping import BasicScrapingDataSchema, ResponseBasicScrapingData

router = APIRouter()


@router.post("/basic_search", summary="Basic scraping data", response_model=ResponseBasicScrapingData)
async def basic_search(request: BasicScrapingDataSchema, current_user: UserModel = Depends(get_current_user),
                       db: AsyncIOMotorDatabase = Depends(get_mongo_db)) -> JSONResponse:
    """Pesquisa básica de dados de uma empresa, informar apenas o CNPJ para realizar a pesquisa."""

    if not current_user:
        raise NotAuthenticatedException()

    cnpj = request.cnpj
    cnpj = re.sub(r'\D', '', cnpj)

    result = scraper.basic_scraping_casa_dados(cnpj)

    if result is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Não foi possível realizar o scraping dos dados.")

    collection_basic = db['basic_search']
    await collection_basic.update_one(
        {"user_id": current_user.id, "result": result},
        {"$set": {"result.CNPJ": cnpj}},
        upsert=True
    )

    create_excel(result, endpoint='basic_search')

    return JSONResponse(content={"results": result})
