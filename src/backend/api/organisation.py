from fastapi import Depends, Response
from fastapi_controllers import Controller, get, post
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db_session
from src.database import User
from src.database import OrganisationScheme, UserScheme
from .. import OrganisationService, UserService
# from DataBase.schemes.invite import InviteInfo
# from DataBase.schemes.role_scheme import RoleScheme
# from DataBase.schemes.workspace_profile import WorkspaceProfileScheme
# from DataBase.schemes.workspace_scheme import WorkspaceScheme
from ..login_manager import manager


class CreateOrganisationRequest(BaseModel):
    name: str

class ChangeWorkspaceUserRoleRequest(BaseModel):
    workspace_profile_id: int
    role_id: int


class InviteCreateRequest(BaseModel):
    use_limit: int = Field(ge=0, le=11)


class InviteCreated(BaseModel):
    key: str


class KickRequest(BaseModel):
    user_id: int


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

    @get("/", response_model=OrganisationScheme)
    async def get_organisation(self):
        return self.user.organisation

    @post("/", response_model=OrganisationScheme)
    async def create_workspace(self, request: CreateOrganisationRequest):
        organisation = await self.organisation_service.create(self.user, request.name)
        await self.organisation_service.add_user(organisation, self.user)
        await self.session.commit()
        return organisation

    @post("/{organisation_id}/kick")
    async def kick(self,
                   request: KickRequest,
                   workspace_id: int):
        organisation = await self.organisation_service.get_by_id(workspace_id)
        user = await self.user_service.get_by_id(request.user_id)
        await self.organisation_service.check_owner(organisation, user)
        await self.organisation_service.remove_user(organisation, user)
        await self.session.commit()
        return {"message": "OK"}

    @post("/{organisation_id}/leave")
    async def organisation_leave(self, organisation_id: int):
        organisation = await self.organisation_service.get_by_id(organisation_id)
        await self.organisation_service.remove_user(organisation, self.user)
        await self.session.commit()
        return {"message": "OK"}

    @get("/{organisation_id}/members", response_model=list[UserScheme])
    async def get_workspace_members(self, organisation_id: int):
        organisation = await self.organisation_service.get_by_id(organisation_id)
        await self.organisation_service.check_participant(organisation, self.user)
        return await self.organisation_service.get_users(organisation)

    # TODO: here
    # @get("/{workspace_id}/invite", response_model=list[InviteInfo])
    # async def get_workspace_invites(self,
    #                                 workspace_id: int):
    #     workspace = await self.workspace_service.get_by_id(workspace_id)
    #     workspace_profile = await self.workspace_profile_service.get_by_bind(self.profile, workspace)
    #     await self.workspace_profile_service.check_permission(workspace_profile, Permissions.moderate_workspace)
    #
    #     return self.workspace_service.get_invites(workspace)
    #
    # @post("/{workspace_id}/invite", response_model=InviteCreated)
    # async def create_workspace_invite(self,
    #                                   workspace_id: int,
    #                                   request: InviteCreateRequest):
    #     workspace = await self.workspace_service.get_by_id(workspace_id)
    #     workspace_profile = await self.workspace_profile_service.get_by_bind(self.profile, workspace)
    #     await self.workspace_profile_service.check_permission(workspace_profile, Permissions.moderate_workspace)
    #
    #     invite = await self.workspace_service.create_invite(workspace_profile, request.use_limit)
    #     await self.session.commit()
    #     return InviteCreated(key=invite.key)
