from typing import Optional

from sqlalchemy import JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from .. import Base
from . import user


class Organisation(Base):
    __tablename__ = "organisation"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    users: Mapped[List["user.User"]] = relationship(back_populates="organisation")
    name: Mapped[Optional[str]] = mapped_column(unique=True)

    creator_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    creator: Mapped["user.User"] = relationship(back_populates="organisation")

    def __repr__(self) -> str:
        return f"Organisation(id={self.id!r}, users={self.users!r})"
