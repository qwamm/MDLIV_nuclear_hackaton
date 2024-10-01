from fastapi import HTTPException
from src.database import GithubProfile
from src.database import GithubProfileRepository
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_login.exceptions import InvalidCredentialsException
from starlette.status import HTTP_404_NOT_FOUND


class GithubProfileService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.profile_repository = GithubProfileRepository(session)

    async def get_by_github_username(self, github_username: str) -> GithubProfile:
        profile=await self.profile_repository.get_by_github_username(github_username)
        if profile is None:
            raise HTTPException(HTTP_404_NOT_FOUND, "github profile not found")
        else:
            return profile

    async def get_by_auth_token(self, auth_token: str) -> GithubProfile:
        profile=await self.profile_repository.get_by_auth_token(auth_token)
        if profile is None:
            raise HTTPException(HTTP_404_NOT_FOUND, "github profile not found")
        else:
            return profile

    async def login(self, user_id: int, auth_token: str) -> GithubProfile:
        profile = await self.profile_repository.github_login(user_id, auth_token)
        if profile is None:
            raise InvalidCredentialsException
        return profile