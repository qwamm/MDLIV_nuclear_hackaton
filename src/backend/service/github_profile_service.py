from fastapi import HTTPException
from src.database import GithubProfile
from src.database import GithubProfileRepository, UserRepository
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_login.exceptions import InvalidCredentialsException
from starlette.status import HTTP_404_NOT_FOUND
from github import Auth, Github, GithubException
from llm_integration.analyzer import LLM_Analyzer
import datetime

class GithubProfileService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.profile_repository = GithubProfileRepository(session)
        self.client = Github()
        self.__good_comment_threshold = 5
        self.__commits_sha = set()
        self.__pulls_ids = set()
        self.__comments_ids = set()

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
        total_commits = 0

        last_commit_sha = ghp.last_commit_sha
        last_commit_date = datetime.datetime.min
        newest_commit_date = datetime.datetime.min
        newest_commit_sha = ''

        if last_commit_sha != '':
            last_commit_date = repo.get_commit(sha=last_commit_sha).commit.committer.date.replace(tzinfo=None)
            newest_commit_date = last_commit_date
            newest_commit_sha = ''

        for br in repo.get_branches():
            print(br.name)
            for commit in repo.get_commits(sha=br.commit.sha, since=last_commit_date):
                if commit.commit.committer.date.replace(tzinfo=None) > newest_commit_date:
                    newest_commit_date = commit.commit.committer.date.replace(tzinfo=None)
                    newest_commit_sha = commit.sha

                print(commit.sha, commit.commit.message)
                if commit.committer is None or commit.sha in self.__commits_sha or str(commit.sha) == last_commit_sha:
                    continue

                if commit.commit.author.name == user_name:
                    commit_date = commit.commit.committer.date.replace(tzinfo=None)
                    total_commits += ((datetime.datetime.now() - commit_date).days <= 7)
                    self.__commits_sha.add(commit.sha)
        if newest_commit_sha!='':
            await self.drop_last_commit_sha(ghp, newest_commit_sha)
        return total_commits

    async def get_last_week_pulls(self, user_id: int, repo: str) -> int | None:
        if self.client is None:
            return None

        ghp = await  self.profile_repository.get_by_user_id(user_id)
        if ghp is None:
            return None

        repo = self.client.get_repo(repo)
        user_name = self.client.get_user(ghp.github_username).name
        total_pulls = 0

        last_pull_id = ghp.last_pull_id
        last_pull_date = datetime.datetime.min
        newest_pull_date = datetime.datetime.min
        newest_pull_id = ''

        if last_pull_id != -1:
            last_pull_date = repo.get_pull(last_pull_id).created_at.replace(tzinfo=None)
            newest_pull_date = last_pull_date
            newest_pull_id = -1

        for pull in repo.get_pulls():
            if pull.created_at.replace(tzinfo=None) > newest_pull_date:
                newest_pull_date = pull.created_at.replace(tzinfo=None)
                newest_pull_id = pull.number

            if pull.user is None or pull.id in self.__pulls_ids or pull.created_at.replace(tzinfo=None) <= last_pull_date:
                continue

            if pull.user.name == user_name:
                pull_date = pull.created_at.replace(tzinfo=None)
                total_pulls += ((datetime.datetime.now() - pull_date).days <= 7)
                self.__pulls_ids.add(pull.id)
        if newest_pull_id != -1:
            await self.drop_last_pull_id(ghp, newest_pull_id)
        return total_pulls

    # async def get_last_week_useful_comments(self, user_id: int, repo: str) -> int | None:
    #     if self.client is None:
    #         return None
    #
    #     ghp = await  self.profile_repository.get_by_user_id(user_id)
    #     if ghp is None:
    #         return None
    #
    #     try:
    #         analyzer = LLM_Analyzer()
    #     except ValueError:
    #         return None
    #
    #     repo = self.client.get_repo(repo)
    #     user_name = self.client.get_user(ghp.github_username).name
    #     comments_ids = set()
    #     total_useful_comments = 0
    #
    #     for br in repo.get_branches():
    #         for commit in repo.get_commits(sha=br.commit.sha):
    #             for comment in commit.get_comments():
    #                 if comment.id in comments_ids:
    #                     continue
    #                 if comment.user.name == user_name:
    #                     grade = analyzer.grade_comment(comment.body)
    #                     if grade >= self.__good_comment_threshold:
    #                         print(comment.body)
    #                         comment_date = comment.created_at.replace(tzinfo=None)
    #                         total_useful_comments += ((datetime.datetime.now() - comment_date).days <= 7)
    #                         comments_ids.add(comment.id)
    #     return total_useful_comments

    async def get_last_week_comments(self, user_id: int, repo: str, use_llm: bool = True) -> (int | None, int | None):
        if self.client is None:
            return None, None

        ghp = await self.profile_repository.get_by_user_id(user_id)
        if ghp is None:
            return None, None

        analyzer = None
        try:
            analyzer = LLM_Analyzer() if use_llm else None
        except ValueError:
            use_llm = False

        repo = self.client.get_repo(repo)
        user_name = self.client.get_user(ghp.github_username).name
        useful_comments = 0
        total_comments = 0

        last_comment_id = ghp.last_comment_id
        last_comment_date = datetime.datetime.min
        newest_comment_date = datetime.datetime.min
        newest_comment_id = -1

        if last_comment_id != -1:
            found = False
            for br in repo.get_branches():
                for commit in repo.get_commits(sha=br.commit.sha):
                    for comment in commit.get_comments():
                        if comment.id == last_comment_id:
                            last_comment_date = comment.created_at.replace(tzinfo=None)
                            newest_comment_date = last_comment_date
                            newest_comment_id = -1
                            found = True
                            break
                    if found:
                        break
                if found:
                    break

        for br in repo.get_branches():
            for commit in repo.get_commits(sha=br.commit.sha):
                for comment in commit.get_comments():
                    if comment.created_at.replace(tzinfo=None) > newest_comment_date:
                        newest_comment_date = comment.created_at.replace(tzinfo=None)
                        newest_comment_id = comment.id

                    if comment.id in self.__comments_ids or comment.created_at.replace(tzinfo=None) <= last_comment_date:
                        continue
                    if comment.user.name == user_name:
                        print(comment.body)
                        if use_llm:
                            grade = analyzer.grade_comment(comment.body)
                            if grade >= self.__good_comment_threshold:
                                print(grade)
                                comment_date = comment.created_at.replace(tzinfo=None)
                                useful_comments += ((datetime.datetime.now() - comment_date).days <= 7)
                        self.__comments_ids.add(comment.id)
                        total_comments += 1
        if newest_comment_id!=-1:
            await self.drop_last_comment_id(ghp, newest_comment_id)
        return useful_comments, total_comments

    async def drop_last_commit_sha(self, profile: GithubProfile, commit_sha: str) -> None:
        return await self.profile_repository.drop_last_commit_sha(profile, commit_sha)

    async def drop_last_pull_id(self, profile: GithubProfile, pull_id: int) -> None:
        return await self.profile_repository.drop_last_pull_id(profile, pull_id)

    async def drop_last_comment_id(self, profile: GithubProfile, comment_id: int) -> None:
        return await self.profile_repository.drop_last_comment_id(profile, comment_id)
