from typing import Optional

from fastapi import Depends
from fastapi_controllers import Controller, get
from pydantic import BaseModel

from src.database import get_db_session
from src.database import User, Organisation
from src.database import UserScheme, OrganisationScheme
from ..login_manager import manager
from .. import OrganisationService


class InfoResponse(BaseModel):
    auth: bool
    user: UserScheme | None
    organisation: OrganisationScheme | None

    class Config:
        orm_mode = True


class UserController(Controller):
    prefix = "/user"
    tags = ["user"]

    def __init__(self, session=Depends(get_db_session)):
        self.organisation_service = OrganisationService(session)

    @get("/", response_model=InfoResponse)
    async def getInfo(self, user: User | None = Depends(manager.optional)):
        response = {"auth": user is not None,
                    "user": user,
                    "organisation": await self.organisation_service.get_by_user(user) if user else None}
        return response
