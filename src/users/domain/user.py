from sqlalchemy.orm import Mapped, mapped_column

from src.core.models.base import Base


class User(Base):
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)