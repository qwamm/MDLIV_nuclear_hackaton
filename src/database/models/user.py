from typing import Optional

from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from .. import Base
from . import organisation


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str | None]
    secret: Mapped[str | None]

    organisation_id: Mapped[int | None] = mapped_column(ForeignKey("organisation.id"))
    organisation: Mapped[Optional["organisation.Organisation"]] = relationship(back_populates="users")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.username!r}), organisation={self.organisation!r}"
