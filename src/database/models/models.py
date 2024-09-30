from typing import Optional

from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from .. import Base
from src.database import models
from typing import List


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str | None]
    secret: Mapped[str | None]

    organisation_id: Mapped[Optional[int]] = mapped_column(ForeignKey("organisation.id"))
    organisation: Mapped[Optional["Organisation"]] = relationship(foreign_keys='User.organisation_id')

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.username!r})"


class Organisation(Base):
    __tablename__ = "organisation"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    users_id: Mapped[List[int]] = mapped_column(ForeignKey("user.id"))
    users: Mapped[List["User"]] = relationship(foreign_keys="Organisation.users_id")
    name: Mapped[Optional[str]] = mapped_column(unique=True)

    creator_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    creator: Mapped["User"] = relationship(foreign_keys="Organisation.creator_id")

    def __repr__(self) -> str:
        return f"Organisation(id={self.id!r}, users={self.users!r})"


class InviteKey(Base):
    __tablename__ = "key_data"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    key: Mapped[str]
    use_limit: Mapped[int] = mapped_column(default=1)

    creator_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    creator: Mapped["User"] = relationship()

    organisation_id: Mapped[int] = mapped_column(ForeignKey("organisation.id"))
    organisation: Mapped["Organisation"] = relationship()