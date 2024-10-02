from fastapi import Depends
from fastapi_controllers import Controller, delete, get, post
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db_session
from src.database import User
from ..login_manager import manager
from .. import InviteService, OrganisationService, UserService


class InviteController(Controller):
    prefix = "/invite"
    tags = ["invite"]

    def __init__(self,
                 session: AsyncSession = Depends(get_db_session),
                 user: User = Depends(manager)) -> None:
        self.session = session
        self.user = user

        self.organisation_service = OrganisationService(session)
        self.user_service = UserService(session)
        self.invite_service = InviteService(session)

    @post("/{token}")
    async def activate_invite(self, token: str):
        invite = await self.invite_service.get_by_key(token)
        user = await self.user_service.get_by_id(self.user.id)
        await self.invite_service.activate_invite(invite, user)
        await self.session.commit()
        return {"message": "ok"}

    @delete("/{id}")
    async def deactivate_invite(self, id: int):
        invite = await self.invite_service.get_by_id(id)
        await self.invite_service.deactivate_invite(invite)
        await self.session.commit()
        return {"message": "ok"}

