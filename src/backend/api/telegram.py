from fastapi import Depends
from fastapi_controllers import Controller, delete, get, post
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db_session
from src.database import User
from ..login_manager import manager
from .. import TelegramService, UserService
from src.database import TelegramScheme


class TelegramController(Controller):
    prefix = "/telegram"
    tags = ["telegram"]

    def __init__(self,
                 session: AsyncSession = Depends(get_db_session),
                 user: User = Depends(manager)) -> None:
        self.session = session
        self.user = user

        self.telegram_service = TelegramService(session)
        self.user_service = UserService(session)

    @post("/login")
    async def attach_telegram(self, username: str):
        await self.telegram_service.create(self.user, username)
        await self.session.commit()
        return {"message": "ok"}

    @get("/", response_model=TelegramScheme)
    async def get_telegram(self):
        tg_profile = await self.telegram_service.get_by_user(self.user)
        return tg_profile

    @post("/set_username")
    async def set_username(self, username: str):
        await self.telegram_service.set_username(self.user, username)
        await self.session.commit()
        return {"message": "ok"}

