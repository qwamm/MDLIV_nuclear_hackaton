from typing import Optional

from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column
from .. import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[Optional[str]]
    secret: Mapped[Optional[str]]

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.username!r})"