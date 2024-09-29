from fastapi import HTTPException
from src.database import User
from src.database import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_login.exceptions import InvalidCredentialsException
from starlette.status import HTTP_400_BAD_REQUEST

class UserService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

        self.profile_repository = UserRepository(session)

    async def login(self, login: str, password: str) -> User:
        profile = await self.profile_repository.get_by_auth(login, password)
        if profile is None:
            raise InvalidCredentialsException
        return profile

    async def registration(self, login, password, repeat_password):
        if password != repeat_password:
            raise HTTPException(HTTP_400_BAD_REQUEST, "Passwords don't match")
        if await self.profile_repository.get_by_username(login) is not None:
            raise HTTPException(HTTP_400_BAD_REQUEST, "User already exist")
        await self.profile_repository.registration(login, password)