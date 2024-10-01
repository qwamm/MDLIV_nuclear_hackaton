from pydantic import BaseModel
from . import UserScheme
from . import OrganisationScheme


class InviteScheme(BaseModel):
    id: int
    use_limit: int
    key: str
    creator: UserScheme
    organisation: OrganisationScheme

    class Config:
        orm_mode = True
