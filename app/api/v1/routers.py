from fastapi import APIRouter

from app.api.v1.routes import user, basic_search, advanced_search, city, download_excel

api_router = APIRouter()

api_router.include_router(user.router, prefix="/users", tags=["Users"])
api_router.include_router(basic_search.router, prefix="/scraping_data", tags=["Scraping Data"])
api_router.include_router(advanced_search.router, prefix="/scraping_data", tags=["Scraping Data"])
api_router.include_router(city.router, prefix="/ibge", tags=["Get City - IBGE"])
api_router.include_router(download_excel.router, prefix="/download_excel", tags=["Download Excel"])