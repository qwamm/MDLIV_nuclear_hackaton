from fastapi import Depends, Response, HTTPException
from fastapi_controllers import Controller, get
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

import json
from datetime import timedelta

from src.database import get_db_session, User
from ..service import GithubProfileService, OrganisationService, UserService
from src.backend.login_manager import manager
import requests
from src import DIRECT_URL, CLIENT_ID, CLIENT_SECRET, REDIRECT_URI
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

class ActivityResponse(BaseModel):
    commits: int
    pulls: int
    comments: int
    useful_comments_percentage: float
    score: float

class GithubController(Controller):
    prefix = "/github"
    tags = ["github"]

    def __init__(self, session: AsyncSession = Depends(get_db_session), user=Depends(manager)):
        self.session = session
        self.user = user
        self.profile_service = GithubProfileService(session)
        self.organisation_service = OrganisationService(session)
        self.user_service = UserService(session)

    @get("/login")
    async def login(self, code: str):
        if code!="":
            response = requests.post(DIRECT_URL, params={
                'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
                'code': code,
                'redirect_uri': REDIRECT_URI
            })
            token = response.content.decode().split("&")[0].split("=")[-1]
            if self.user is None:
                raise HTTPException(HTTP_401_UNAUTHORIZED, 'user is unauthorised')
            elif token=='bad_verification_code':
                raise HTTPException(HTTP_400_BAD_REQUEST, 'github returned bad_verification_code')
            else:
                token = response.content.decode().split("&")[0].split("=")[-1]
                github_profile=await self.profile_service.login(self.user.id, token)
                return {"message": "OK"}
        else:
            return {"message": "no code provided"}


    @get("/activity", response_model=ActivityResponse)
    async def get_activity(self):
        if self.user is None:
            raise HTTPException(HTTP_401_UNAUTHORIZED, 'user is unauthorised')
        elif self.user.organisation_id is None:
            raise HTTPException(HTTP_404_NOT_FOUND, 'your organisation not found')
        else:
            ghp = await self.profile_service.get_by_user_id(self.user.id)
            if ghp is None:
                raise HTTPException(HTTP_404_NOT_FOUND, 'github profile not found')
            self.profile_service.client = self.profile_service.initialise_github_client(ghp.auth_token)

            organisation = await self.organisation_service.get_by_id(self.user.organisation_id)
            if organisation.repository_full_name is None:
                raise HTTPException(HTTP_404_NOT_FOUND, 'your organisation does not have repo, contact the creator to add')
            else:
                total_commits = await self.profile_service.get_last_week_commits(self.user.id, str(organisation.repository_full_name))
                total_pulls = await self.profile_service.get_last_week_pulls(self.user.id, str(organisation.repository_full_name))
                total_useful_comments, total_comments = await self.profile_service.get_last_week_comments(self.user.id, str(organisation.repository_full_name), False)
                #total_useful_comments = await self.profile_service.get_last_week_useful_comments(self.user.id, str(organisation.repository_full_name))
                if any((total_comments, total_commits, total_pulls)) is None:
                    raise HTTPException(HTTP_400_BAD_REQUEST, 'github has not returned either commits, pulls or comments')
                else:
                    good_comments_percentage = 0.0
                    if total_useful_comments is not None and total_comments is not None and total_comments != 0:
                        good_comments_percentage = total_useful_comments/total_comments
                    print(good_comments_percentage*100, end='%\n')
                    score = 0.6 * total_commits + good_comments_percentage * total_comments + 0.1 * total_pulls
                    await self.user_service.incr_coins(ghp.user_id, score.__ceil__())
                    return ActivityResponse(commits=total_commits, pulls=total_pulls, comments=total_comments, useful_comments_percentage=good_comments_percentage, score=score)
