from fastapi import Depends, Response, HTTPException
from fastapi_controllers import Controller, get
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

import json
from datetime import timedelta

from src.database import get_db_session, User
from ..service import GithubProfileService
from src.backend.login_manager import manager
import requests
from ... import DIRECT_URL, CLIENT_ID, CLIENT_SECRET, REDIRECT_URI
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_400_BAD_REQUEST

class GithubController(Controller):
    prefix = "/github_login"
    tags = ["github_login"]

    def __init__(self, session: AsyncSession = Depends(get_db_session)):
        self.session = session
        self.profile_service = GithubProfileService(session)

    @get("/")
    async def login(self, code: str, user=Depends(manager)):
        if code!="":
            response = requests.post(DIRECT_URL, params={
                'client_id': CLIENT_ID,
                'client_secret': CLIENT_SECRET,
                'code': code,
                'redirect_uri': REDIRECT_URI
            })
            token = response.content.decode().split("&")[0].split("=")[-1]
            if user is None:
                raise HTTPException(HTTP_401_UNAUTHORIZED, 'user is unauthorised')
            elif token=='bad_verification_code':
                raise HTTPException(HTTP_400_BAD_REQUEST, 'github returned bad_verification_code')
            else:
                token = response.content.decode().split("&")[0].split("=")[-1]
                github_profile=await self.profile_service.login(user.id, token)
                return {"message": "OK"}
        else:
            return {"message": "no code provided"}