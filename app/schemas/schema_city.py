from pydantic import BaseModel


class CityIbgeSchema(BaseModel):
    id: int
    name: str
