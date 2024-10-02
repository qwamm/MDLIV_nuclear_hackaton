import secrets
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from werkzeug.security import check_password_hash, generate_password_hash

from .. import User
from .. import Organisation


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, id: int) -> User | None:
        stmt = select(User).where(User.id == id).limit(1)
        return await self.session.scalar(stmt)

    async def get_by_username(self, username: str) -> User | None:
        stmt = select(User).where(User.username == username).limit(1)
        return await self.session.scalar(stmt)

    async def get_by_auth(self, username: str, password: str) -> User | None:
        profile = await self.get_by_username(username)
        if profile is None:
            return None
        if not self.compare_password(profile, password):
            return None
        return profile

    async def registration(self, username: str, password: str) -> User | None:
        profile = User(username=username, coins=0)
        self.session.add(profile)
        await self.set_password(profile, password)
        return await self.get_by_id(profile.id)

    async def set_password(self, profile: User, new_password: str) -> None:
        profile.password = generate_password_hash(new_password)
        profile.secret = secrets.token_urlsafe(8)
        await self.session.flush()

    def compare_password(self, profile: User, password: str) -> bool:
        old_password = profile.password
        if old_password is None:
            old_password = ""
        return check_password_hash(old_password, password)

    async def get_organisation(self, profile: User) -> Organisation | None:
        if profile.organisation_id is not None:
            stmt = select(Organisation).where(Organisation.id == profile.organisation_id).limit(1)
            return await self.session.scalar(stmt)
        else:
            return None

    async def incr_coins(self, profile: User, coins: int) -> None:
        profile.coins += coins
        await self.session.commit()
        return None