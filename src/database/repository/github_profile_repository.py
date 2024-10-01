import secrets
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from werkzeug.security import check_password_hash, generate_password_hash

from .. import User
from .. import GithubProfile
import github as git

class GithubProfileRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, id: int) -> GithubProfile | None:
        stmt = select(GithubProfile).where(GithubProfile.id == id).limit(1)
        return await self.session.scalar(stmt)

    async def get_by_github_username(self, github_username: str) -> GithubProfile | None:
        stmt = select(GithubProfile).where(GithubProfile.github_username == github_username).limit(1)
        return await self.session.scalar(stmt)

    async def get_by_auth_token(self, auth_token: str) -> GithubProfile | None:
        stmt = select(GithubProfile).where(GithubProfile.auth_token==auth_token).limit(1)
        return await self.session.scalar(stmt)

    async def get_by_user_id(self, user_id: int) -> GithubProfile | None:
        stmt = select(GithubProfile).where(GithubProfile.user_id==user_id).limit(1)
        return await self.session.scalar(stmt)

    async def github_login(self, user_id: int, auth_token: str) -> GithubProfile | None:
        stmt=select(GithubProfile).where(GithubProfile.user_id==user_id).limit(1)
        ghp: GithubProfile | None =await self.session.scalar(stmt)
        if ghp is None:
            git_client=git.Github(auth=git.Auth.Token(auth_token))
            try:
                github_profile=GithubProfile(github_username=git_client.get_user().login, auth_token=auth_token, user_id=user_id)
            except git.GithubException:
                git_client.close()
                return None
            git_client.close()
            self.session.add(github_profile)
            await self.session.commit()
        else:
            ghp.auth_token=auth_token
            await self.session.flush()

        return await self.get_by_user_id(user_id)