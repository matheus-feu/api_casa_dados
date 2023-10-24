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
from app.schemas.schema_scraping import ResponseAdvancedScrapingData, AdvancedScrapingDataSchema

router = APIRouter()


@router.post("/advanced_search", summary="Advanced scraping data", response_model=ResponseAdvancedScrapingData)
async def advanced_search(request: AdvancedScrapingDataSchema,
                          current_user: UserModel = Depends(get_current_user),
                          db: AsyncIOMotorDatabase = Depends(get_mongo_db)) -> JSONResponse:
    """Pesquisa avançada de dados de uma empresa, os parâmetros são opcionais, a quantidade de páginas é limitada a 50, caso
    desejar quantas quer que sejam retornadas, basta passar o parâmetro qnt_pages com o valor desejado."""

    if not current_user:
        raise NotAuthenticatedException()

    result, num_results, qnt_pages = scraper.advanced_scraping_casa_dados(**request.dict())

    if result is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Não foi possível realizar o scraping dos dados.")

    if isinstance(result, list):
        create_excel(result, 'advanced_search')

    collection_advanced = db['advanced_search']
    for item in result:
        cnpj = item.get('cnpj')
        if cnpj:
            cnpj = re.sub(r'\D', '', cnpj)

        await collection_advanced.update_one(
            {"user_id": current_user.id, "result": item},
            {"$set": {"cnpj": cnpj}},
            upsert=True
        )

    return JSONResponse(content={"results": result, "num_results": num_results, "qnt_pages": qnt_pages})
