from typing import Optional

from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from .. import Base
from src.database import models
from typing import List


class User(Base):
    __tablename__ = "user_table"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str | None]
    secret: Mapped[str | None]

    organisation_id: Mapped[Optional[int]] = mapped_column(ForeignKey("organisation_table.id"))
    organisation: Mapped[Optional["Organisation"]] = relationship(back_populates="users", foreign_keys="User.organisation_id", lazy="selectin")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.username!r})"


class Organisation(Base):
    __tablename__ = "organisation_table"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    users: Mapped[List["User"]] = relationship(back_populates="organisation", primaryjoin="Organisation.id==User.organisation_id", lazy="selectin")
    name: Mapped[Optional[str]] = mapped_column(unique=True)

    creator_id: Mapped[int] = mapped_column(ForeignKey("user_table.id"))
    creator: Mapped["User"] = relationship(foreign_keys="Organisation.creator_id", lazy="selectin")
    repository_full_name: Mapped[Optional[str]] = mapped_column(unique=True)

    def __repr__(self) -> str:
        return f"Organisation(id={self.id!r}, users={self.users!r})"


class InviteKey(Base):
    __tablename__ = "key_data_table"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    key: Mapped[str]
    use_limit: Mapped[int] = mapped_column(default=1)

    creator_id: Mapped[int] = mapped_column(ForeignKey("user_table.id"))
    creator: Mapped["User"] = relationship()

    organisation_id: Mapped[int] = mapped_column(ForeignKey("organisation_table.id"))
    organisation: Mapped["Organisation"] = relationship()

class GithubProfile(Base):
    __tablename__ = "github_profile"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    github_username: Mapped[str] = mapped_column(unique=True)
    auth_token: Mapped[Optional[str]]
    user_id: Mapped[int] = mapped_column(ForeignKey("user_table.id"))
    user: Mapped["User"] = relationship(foreign_keys="GithubProfile.user_id")

    def __repr__(self) -> str:
        return f"GithubProfile(id={self.id!r}, github_username={self.github_username!r}, auth_token={self.auth_token!r}, user_id={self.user_id!r})"