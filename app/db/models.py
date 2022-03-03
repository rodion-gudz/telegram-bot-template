from sqlalchemy import Column, BigInteger, String

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, unique=True, autoincrement=False)
    username = Column(String, unique=True)
