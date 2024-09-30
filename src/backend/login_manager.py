import json

from fastapi_login import LoginManager

from src.database import sessionmanager
from src.database import UserRepository
from src import SECRET_KEY
from src.exceptions import NotAuthenticatedException


manager = LoginManager(SECRET_KEY, token_url='/api/auth/login',
                       use_cookie=True, not_authenticated_exception=NotAuthenticatedException)


@manager.user_loader()
async def load_user(userStr: str):  # could also be an asynchronous function
    async with sessionmanager.session() as session:
        profileRepository = UserRepository(session)
        user: dict = json.loads(userStr)
        id: int | None = user.get("ID", None)
        secret = user.get("Secret", None)
        if id is None or user is None:
            return None
        profile = await profileRepository.get_by_id(id)
        if profile is None:
            return None
        if profile.secret == secret:
            return profile
        return None