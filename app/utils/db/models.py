# sourcery skip: avoid-builtin-shadow
from sqlalchemy import BigInteger, Column

from app.utils.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, unique=True, autoincrement=False)
