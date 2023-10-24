import re
from typing import Optional

from pydantic import BaseModel, EmailStr, validator, constr


class UserBaseSchema(BaseModel):
    id: Optional[int] = None
    name: Optional[str]
    phone: Optional[str]
    email: EmailStr

    class Config:
        from_attributes = True

    @validator("email")
    def validate_email_format(cls, value):
        if "@" not in value:
            raise ValueError("E-mail inválido")
        return value

    @validator('name')
    def validate_name(cls, value):
        preposicoes = ['das', 'dos', 'de', 'da', 'do']
        nome = ' '.join(word for word in re.split(r'\s+', value) if word.lower() not in preposicoes)

        if len(nome.split()) < 2:
            raise ValueError("O nome deve conter no mínimo duas palavras")

        return value


class UserSchemaCreate(UserBaseSchema):
    password: constr(min_length=8)
