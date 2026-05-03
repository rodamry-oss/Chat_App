from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from app.db.base_class import Base
from datetime import datetime


class Message(Base):
    __tablename__= "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    content = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)