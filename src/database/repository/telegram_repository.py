import secrets
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .. import TelegramProfile, User


class TelegramRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, id: int) -> TelegramProfile | None:
        stmt = select(TelegramProfile).where(TelegramProfile.id == id).limit(1)
        return await self.session.scalar(stmt)

    async def get_by_username(self, username: str) -> Optional[TelegramProfile]:
        stmt = select(TelegramProfile).where(TelegramProfile.telegram_username == username).limit(1)
        return await self.session.scalar(stmt)

    async def get_by_user(self, user: User) -> TelegramProfile | None:
        stmt = select(TelegramProfile).where(TelegramProfile.user_id == user.id).limit(1)
        return await self.session.scalar(stmt)

    async def create(self, user: User, username: str) -> Optional[TelegramProfile]:
        if await self.get_by_username(username) is not None:
            return None
        if await self.get_by_user(user) is not None:
            return None
        tg_profile = TelegramProfile(user_id=user.id, telegram_username=username)
        self.session.add(tg_profile)
        await self.session.flush()
        new_key_data = await self.get_by_id(tg_profile.id)
        return new_key_data

    async def set_username(self, tg_profile: TelegramProfile, username: str):
        tg_profile.telegram_username = username
        await self.session.flush()

    async def add_points(self, tg_profile: TelegramProfile, points: int = 1):
        tg_profile.points += points
        await self.session.flush()

