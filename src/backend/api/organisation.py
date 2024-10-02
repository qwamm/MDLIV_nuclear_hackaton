from fastapi import Depends, Response, HTTPException
from fastapi_controllers import Controller, get, post
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db_session
from src.database import User
from src.database import OrganisationScheme, UserScheme, InviteScheme
from .. import OrganisationService, UserService, InviteService
from ..login_manager import manager
from starlette.status import HTTP_403_FORBIDDEN

class CreateOrganisationRequest(BaseModel):
    name: str


class InviteCreateRequest(BaseModel):
    use_limit: int = Field(ge=0)


class InviteCreated(BaseModel):
    key: str


class KickRequest(BaseModel):
    user_id: int

class SetRepoRequest(BaseModel):
    repo_name: str

class OrganisationController(Controller):
    prefix = "/organisation"
    tags = ["organisation"]

    def __init__(self,
                 session: AsyncSession = Depends(get_db_session),
                 user: User = Depends(manager)) -> None:
        self.session = session
        self.user = user

        self.organisation_service = OrganisationService(session)
        self.user_service = UserService(session)
        self.invite_service = InviteService(session)

    @get("/", response_model=OrganisationScheme)
    async def get_organisation(self):
        return await self.organisation_service.get_by_user(self.user)

    @post("/", response_model=OrganisationScheme)
    async def create_organisation(self, request: CreateOrganisationRequest):
        user = await self.user_service.get_by_id(self.user.id)
        organisation = await self.organisation_service.create(user, request.name)
        await self.organisation_service.add_user(organisation, user)
        await self.session.commit()
        return organisation

    @post("/{organisation_id}/kick")
    async def organisation_kick(self, request: KickRequest, organisation_id: int):
        organisation = await self.organisation_service.get_by_id(organisation_id)
        user = await self.user_service.get_by_id(request.user_id)
        await self.organisation_service.check_owner(organisation, self.user)
        await self.organisation_service.check_not_participant(organisation, user)
        await self.organisation_service.remove_user(organisation, user)
        await self.session.commit()
        return {"message": "OK"}

    @post("/{organisation_id}/leave")
    async def organisation_leave(self, organisation_id: int):
        user = await self.user_service.get_by_id(self.user.id)
        organisation = await self.organisation_service.get_by_id(organisation_id)
        await self.organisation_service.check_participant(organisation, user)
        await self.organisation_service.remove_user(organisation, user)
        await self.session.commit()
        return {"message": "OK"}

    @get("/{organisation_id}/members", response_model=list[UserScheme])
    async def get_organisation_members(self, organisation_id: int):
        organisation = await self.organisation_service.get_by_id(organisation_id)
        await self.organisation_service.check_participant(organisation, self.user)
        return await self.organisation_service.get_users(organisation)

    @get("/invite", response_model=list[InviteScheme])
    async def get_organisation_invites(self, organisation_id: int):
        organisation = await self.organisation_service.get_by_id(organisation_id)
        await self.organisation_service.check_owner(organisation, self.user)
        return await self.organisation_service.get_invites(organisation)

    @post("/invite", response_model=InviteCreated)
    async def create_organisation_invite(self, request: InviteCreateRequest):
        invite = await self.invite_service.create_invite(self.user, request.use_limit)
        await self.session.commit()
        return InviteCreated(key=invite.key)

    @post("/repo")
    async def set_repo_name(self, request: SetRepoRequest):
        organisation = await self.organisation_service.get_by_id(self.user.organisation_id)
        if self.user.id != organisation.creator_id:
            raise HTTPException(HTTP_403_FORBIDDEN, 'only creator can change organisation repo')
        else:
            await self.organisation_service.set_repository_full_name(organisation, request.repo_name)
            await self.session.commit()
            return {"message": "OK"}