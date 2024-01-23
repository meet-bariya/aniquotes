from .db import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.sql.expression import text
from sqlalchemy.sql import func

class Quote(Base):
    __tablename__ = 'quote'

    id = Column(Integer, primary_key=True)
    anime = Column(String, nullable=False)
    quote = Column(String, nullable=False)
    character = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(),onupdate=func.now())

# class Anime(Base):
#     __tablename__ = 'anime'

#     id = Column(Integer, primary_key=True)
#     name = Column(String)


# class Character(Base):
#     __tablename__ = 'character'

#     id = Column(Integer, primary_key=True)
#     name = Column(String, nullable=False)
#     anime_id = Column(Integer, ForeignKey("anime.id"))