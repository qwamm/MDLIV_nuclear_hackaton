from fastapi import HTTPException
from src.database import GithubProfile
from src.database import GithubProfileRepository
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_login.exceptions import InvalidCredentialsException
from starlette.status import HTTP_404_NOT_FOUND
from github import Auth, Github, GithubException
import datetime

class GithubProfileService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.profile_repository = GithubProfileRepository(session)
        self.client = Github()

    def initialise_github_client(self, auth_token: str) -> Github | None:
        auth = Auth.Token(auth_token)
        client = Github(auth=auth)
        try:
            login = client.get_user().login
        except GithubException:
            return None
        return client

    def __del__(self):
        if self.client is not None:
            self.client.close()

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

    async def get_by_user_id(self, user_id: int) -> GithubProfile:
        profile=await self.profile_repository.get_by_user_id(user_id)
        if profile is None:
            raise HTTPException(HTTP_404_NOT_FOUND, "github profile not found")
        else:
            return profile

    async def login(self, user_id: int, auth_token: str) -> GithubProfile:
        profile = await self.profile_repository.github_login(user_id, auth_token)
        if profile is None:
            raise InvalidCredentialsException
        return profile

    async def get_last_week_commits(self, user_id: int, repo: str) -> int | None:
        if self.client is None:
            return None

        ghp = await  self.profile_repository.get_by_user_id(user_id)
        if ghp is None:
            return None

        repo = self.client.get_repo(repo)
        user_name = self.client.get_user(ghp.github_username).name
        commits_sha = set()
        total_commits = 0

        for br in repo.get_branches():
            for commit in repo.get_commits(sha=br.commit.sha):
                if commit.committer is None or commit.sha in commits_sha:
                    continue

                if commit.commit.author.name == user_name:
                    commit_date = commit.commit.committer.date.replace(tzinfo=None)
                    total_commits += ((datetime.datetime.now() - commit_date).days <= 7)
                    commits_sha.add(commit.sha)
        return total_commits

    async def get_last_week_pulls(self, user_id: int, repo: str) -> int | None:
        if self.client is None:
            return None

        ghp = await  self.profile_repository.get_by_user_id(user_id)
        if ghp is None:
            return None

        repo = self.client.get_repo(repo)
        user_name = self.client.get_user(ghp.github_username).name
        pulls_ids = set()
        total_pulls = 0

        for pull in repo.get_pulls():
            if pull.user is None or pull.id in pulls_ids:
                continue
            if pull.user.name == user_name:
                pull_date = pull.created_at.replace(tzinfo=None)
                total_pulls += ((datetime.datetime.now() - pull_date).days <= 7)
                pulls_ids.add(pull.id)
        return total_pulls

    async def get_last_week_comments(self, user_id: int, repo: str) -> int | None:
        if self.client is None:
            return None

        ghp = await  self.profile_repository.get_by_user_id(user_id)
        if ghp is None:
            return None

        repo = self.client.get_repo(repo)
        user_name = self.client.get_user(ghp.github_username).name
        comments_ids = set()
        total_comments = 0

        for br in repo.get_branches():
            for commit in repo.get_commits(sha=br.commit.sha):
                for comment in commit.get_comments():
                    if comment.id in comments_ids:
                        continue
                    if comment.user.name == user_name:
                        comment_date = comment.created_at.replace(tzinfo=None)
                        total_comments += ((datetime.datetime.now() - comment_date).days <= 7)
                        comments_ids.add(comment.id)
        return total_comments