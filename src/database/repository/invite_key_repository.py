import secrets
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .. import InviteKey, Organisation, User


class InviteRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, id: int) -> InviteKey | None:
        stmt = select(InviteKey).where(InviteKey.id == id).limit(1)
        return await self.session.scalar(stmt)

    async def get_by_key(self, key: str) -> InviteKey | None:
        stmt = select(InviteKey).where(InviteKey.key == key).limit(1)
        return await self.session.scalar(stmt)

    async def create(self, user: User, use_limit=-1) -> Optional[InviteKey]:
        key = secrets.token_urlsafe(8)
        key_data = InviteKey(creator_id=user.id, key=key, use_limit=use_limit, organisation_id=user.organisation_id)
        self.session.add(key_data)
        await self.session.flush()
        new_key_data = await self.get_by_id(key_data.id)
        return new_key_data

    async def decrease_uselimit(self, key_data: InviteKey):
        key_data.use_limit -= 1
        await self.session.flush()

    async def deactivate(self, key_data: InviteKey):
        key_data.use_limit = 0
        await self.session.flush()
