from fastapi import HTTPException
from src.database import User, Organisation, InviteKey
from src.database import OrganisationRepository
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_login.exceptions import InvalidCredentialsException
from starlette.status import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_403_FORBIDDEN


class OrganisationService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.organisation_repository = OrganisationRepository(session)

    async def create(self, creator: User, name: str) -> Organisation:
        organisation = await self.organisation_repository.create(creator, name)
        await self.add_user(organisation, creator)
        if organisation is None:
            raise HTTPException(HTTP_500_INTERNAL_SERVER_ERROR, "Unable to create organisation")
        return organisation

    async def get_by_id(self, id: int) -> Organisation:
        workspace = await self.organisation_repository.get_by_id(id)
        if workspace is None:
            raise HTTPException(HTTP_404_NOT_FOUND, "Workspace not found")
        return workspace

    async def get_users(self, organisation: Organisation) -> list[User]:
        return await self.organisation_repository.get_user_list(organisation)

    async def get_invites(self, organisation: Organisation) -> list[InviteKey]:
        return await self.organisation_repository.get_invites(organisation)

    async def check_not_participant(self, organisation: Organisation, user: User) -> None:
        if user in await self.organisation_repository.get_user_list(organisation):
            raise HTTPException(HTTP_403_FORBIDDEN, "Already participant")

    async def check_participant(self, organisation: Organisation, user: User) -> None:
        if user not in await self.organisation_repository.get_user_list(organisation):
            raise HTTPException(HTTP_403_FORBIDDEN, "Not participant")

    async def check_owner(self, organisation: Organisation, user: User) -> None:
        if self.organisation_repository.get_owner(organisation) != user:
            raise HTTPException(HTTP_403_FORBIDDEN, "Not enough permissions")

    async def add_user(self, organisation: Organisation, user: User) -> None:
        await self.organisation_repository.add_user(organisation, user)

    async def remove_user(self, organisation: Organisation, user: User) -> None:
        await self.organisation_repository.remove_user(organisation, user)

    async def set_repository_full_name(self, organisation: Organisation, repo: str) -> None:
        await self.organisation_repository.set_repository_full_name(organisation, repo)


