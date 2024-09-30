from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR

from src.database import InviteKey, User, Organisation
from src.database import InviteRepository
from . import OrganisationService
# from Site.service.workspace_profile_service import WorkspaceProfileService
# from Site.service.workspace_service import WorkspaceService


class InviteService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

        self.organisation_service = OrganisationService(session)
        self.invite_repository = InviteRepository(session)

    async def create_invite(self, initiator: User, use_limit: int) -> InviteKey:
        invite_key = await self.invite_repository.create(initiator, use_limit=use_limit)
        if invite_key is None:
            raise HTTPException(HTTP_500_INTERNAL_SERVER_ERROR, "Unable to create invite")
        return invite_key

    async def activate_invite(self, invite: InviteKey, user: User):
        if invite.use_limit <= 0:
            raise HTTPException(HTTP_400_BAD_REQUEST, "Invite expired")
        await self.organisation_service.check_not_participant(invite.organisation, user)
        await self.organisation_service.add_user(invite.organisation, user)
        await self.invite_repository.decrease_uselimit(invite)

    async def get_by_key(self, token: str):
        invite = await self.invite_repository.get_by_key(token)
        if invite is None or invite.use_limit <= 0:
            raise HTTPException(HTTP_404_NOT_FOUND, "Invite not found")
        return invite

    async def get_by_id(self, id: int):
        invite = await self.invite_repository.get_by_id(id)
        if invite is None or invite.use_limit <= 0:
            raise HTTPException(HTTP_404_NOT_FOUND, "Invite not found")
        return invite

    async def deactivate_invite(self, invite: InviteKey):
        await self.invite_repository.deactivate(invite)
