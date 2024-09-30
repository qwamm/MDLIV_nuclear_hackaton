from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .. import Base
from . import User, Organisation


class InviteKey(Base):
    __tablename__ = "key_data"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    key: Mapped[str]
    use_limit: Mapped[int] = mapped_column(default=1)

    creator_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    creator: Mapped[User] = relationship(back_populates="invite_keys")

    organisation_id: Mapped[int] = mapped_column(ForeignKey("organisation.id"))
    organisation: Mapped[Organisation] = relationship(back_populates="invite_keys")
