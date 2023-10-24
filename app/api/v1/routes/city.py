from typing import List

import requests
from fastapi import APIRouter, HTTPException
from starlette.responses import JSONResponse

from app.schemas.schema_city import CityIbgeSchema

router = APIRouter()


@router.get("/get_city/{uf}", summary="Get city by UF", response_model=List[CityIbgeSchema])
async def get_city(UF: str):
    """
    Recuperar as cidades de um estado através da sigla, necessária para o scraping avançado, pois o usuário
    seleciona o estado e a cidade.
    """
    if UF.upper() not in ['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA',
                          'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN',
                          'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO']:
        raise HTTPException(status_code=400, detail="Estado inválido, apenas a sigla é permitida")

    url = f'https://servicodados.ibge.gov.br/api/v1/localidades/estados/{UF}/municipios'

    try:
        response = requests.get(url)
        response.raise_for_status()

        if response.status_code == 200:
            data = response.json()
            cities = [{'id': city['id'], 'nome': city['nome']} for city in data]
            return JSONResponse(content=cities)
        else:
            return JSONResponse(content=[])

    except requests.exceptions.HTTPError as e:
        raise SystemExit(e)
