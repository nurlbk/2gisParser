from pydantic import BaseModel


class Place(BaseModel):
    name: str
    type: str
    phone: str
    address: str
    distinct: str
    rating: str
    link: str

