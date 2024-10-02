from pydantic import BaseModel
from . import UserScheme


class TelegramScheme(BaseModel):
    id: int
    telegram_username: str
    points: int
    user: UserScheme

    class Config:
        orm_mode = True
