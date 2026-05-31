from sqlalchemy import Column, DateTime, Integer, String, DATETIME
from app.db.base_class import Base
from datetime import datetime


class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    from_user = Column(String, index=True, nullable=False)
    to_user   = Column(String, index=True, nullable=False)
    content   = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)