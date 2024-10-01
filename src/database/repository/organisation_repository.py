import secrets
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from werkzeug.security import check_password_hash, generate_password_hash

from .. import Organisation, User, InviteKey


class OrganisationRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, id: int) -> Optional[Organisation]:
        stmt = select(Organisation).where(Organisation.id == id).limit(1)
        return await self.session.scalar(stmt)

    async def get_by_name(self, name: str) -> Optional[Organisation]:
        stmt = select(Organisation).where(Organisation.name == name).limit(1)
        return await self.session.scalar(stmt)

    async def create(self, creator: User, name: str) -> Optional[Organisation]:
        organisation = Organisation(name=name, creator_id=creator.id)
        self.session.add(organisation)
        await self.session.flush()
        new_organisation = await self.get_by_id(organisation.id)
        return new_organisation

    async def get_user_list(self, organisation: Organisation) -> list[User]:
        stmt = select(User).where(User.organisation_id == organisation.id)
        return list((await self.session.scalars(stmt)).all())

    async def set_repository_full_name(self, organisation: Organisation, repo: str):
        organisation_db: Organisation | None = await self.get_by_id(organisation.id)
        organisation_db.repository_full_name = repo
        await self.session.flush()
        return None

    @staticmethod
    async def get_owner(organisation: Organisation) -> User:
        return organisation.creator

    async def add_user(self, organisation: Organisation, user: User) -> None:
        if user.organisation_id != organisation.id:
            stmt = select(User).where(User.id==user.id).limit(1)
            user_db = await self.session.scalar(stmt)
            user_db.organisation_id = organisation.id
            await self.session.flush()

    async def remove_user(self, organisation: Organisation, user: User) -> None:
        if organisation.creator_id != user.id:
            user.organisation_id = None
            organisation.users.remove(user)
            await self.session.flush()

    async def get_invites(self, organisation: Organisation) -> list[InviteKey]:
        stmt = select(InviteKey).where(InviteKey.organisation_id == organisation.id)
        return list((await self.session.scalars(stmt)).all())
