from sqlalchemy import BigInteger, Column, String, Boolean

from bot.db.base import Base

class UsersEntry(Base):
    __tablename__ = "users"
    
    telegram_id = Column(BigInteger, nullable=False, unique=True, primary_key=True)
    name = Column(String, nullable=False)
    status = Column(String, nullable=False)
    blocked = Column(Boolean, nullable=False)