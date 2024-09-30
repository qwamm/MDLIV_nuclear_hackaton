from pydantic import BaseModel


class UserScheme(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True
