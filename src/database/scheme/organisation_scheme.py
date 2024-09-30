from pydantic import BaseModel
from . import UserScheme


class OrganisationScheme(BaseModel):
    id: int
    name: str
    creator: UserScheme

    class Config:
        orm_mode = True
