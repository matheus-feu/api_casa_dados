from datetime import date
from typing import Optional, Union

from pydantic import BaseModel, validator
from validate_docbr import CNPJ

from app.helpers.utils import convert_state_abbreviation_to_name


class BasicScrapingDataSchema(BaseModel):
    """Schema for basic scraping data"""
    cnpj: str

    class Config:
        from_attributes = True

        json_schema_extra = {
            "example": {
                "cnpj": "00000000000191"
            }
        }

    @validator('cnpj')
    def validate_cnpj(cls, value):
        if CNPJ().validate(value):
            return value
        raise ValueError('CNPJ inválido')


class AdvancedScrapingDataSchema(BaseModel):
    """Schema for advanced scraping data"""
    social_reason: Optional[str] = None
    cnae: Optional[Union[int, str]] = None
    legal_nature: Optional[Union[int, str]] = None
    state: Optional[str] = None
    city: Optional[str] = None
    neighborhood: Optional[str] = None
    cep: Optional[str] = None
    situation: Optional[str] = None
    ddd: Optional[int] = None
    date_from: Optional[date] = None
    date_to: Optional[date] = None
    share_capital_from: Optional[float] = None
    share_capital_to: Optional[float] = None
    qnt_pages: Optional[int] = None

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "social_reason": "Empresa Teste",
                "cnae": 123456,
                "legal_nature": "1015 - SOCIEDADE ANÔNIMA FECHADA",
                "state": "SP",
                "city": "São Paulo",
                "neighborhood": "Vila Mariana",
                "cep": "04117091",
                "situation": "ATIVA",
                "ddd": 11,
                "date_from": "2021-01-01",
                "date_to": "2021-01-31",
                "share_capital_from": 1000.00,
                "share_capital_to": 100000.00,
                "qnt_pages": 1
            }
        }

    @validator('qnt_pages')
    def validate_qnt_pages(cls, value):
        if value > 50:
            raise ValueError('Quantidade de páginas inválida, o valor máximo é 50')
        return value

    @validator('cep')
    def validate_cep(cls, value):
        if len(str(value)) != 8:
            raise ValueError('CEP inválido, apenas 8 dígitos são permitidos')
        return value

    @validator('ddd')
    def validate_ddd(cls, value):
        if len(str(value)) != 2:
            raise ValueError('DDD inválido, apenas 2 dígitos são permitidos')
        return value

    @validator('state')
    def validate_state(cls, value):
        if len(value) != 2:
            raise ValueError('Estado inválido, apenas a sigla é permitida')
        return convert_state_abbreviation_to_name(value)

    @validator('situation')
    def validate_situation(cls, value):
        upper_value = value.upper()
        if upper_value not in ['ATIVA', 'BAIXADA', 'SUSPENSA', 'INAPTA', 'NULA']:
            raise ValueError('Situação inválida, apenas ATIVA, BAIXADA, SUSPENSA, INAPTA ou NULA são permitidos')
        return upper_value


class ResponseBasicScrapingData(BaseModel):
    """Schema for response basic scraping data"""
    result: list[dict]


class ResponseAdvancedScrapingData(BaseModel):
    """Schema for response advanced scraping data"""
    results: list[dict]
    num_results: str
    qnt_pages: int
