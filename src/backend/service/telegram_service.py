from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR, HTTP_403_FORBIDDEN

from src.database import TelegramProfile, User, Organisation
from src.database import InviteRepository, TelegramRepository


class TelegramService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.telegram_repository = TelegramRepository(session)

    async def create(self, initiator: User, username: str) -> TelegramProfile:
        tg_profile = await self.telegram_repository.create(initiator, username)
        if tg_profile is None:
            raise HTTPException(HTTP_403_FORBIDDEN, "User already linked or username already taken")
        return tg_profile

    async def set_username(self, initiator: User, username: str):
        tg_profile = await self.telegram_repository.get_by_user(initiator)
        if tg_profile is None:
            raise HTTPException(HTTP_404_NOT_FOUND, "Telegram profile not found")
        await self.telegram_repository.set_username(tg_profile, username)

    async def get_by_id(self, id: int):
        tg_profile = await self.telegram_repository.get_by_id(id)
        if tg_profile is None:
            raise HTTPException(HTTP_404_NOT_FOUND, "Telegram profile not found")
        return tg_profile

    async def get_by_user(self, user: User):
        tg_profile = await self.telegram_repository.get_by_user(user)
        if tg_profile is None:
            raise HTTPException(HTTP_404_NOT_FOUND, "Telegram profile not found")
        # await self.session.refresh(tg_profile)
        return tg_profile

    async def add_points(self, tg_profile: TelegramProfile):
        await self.telegram_repository.add_points(tg_profile)