from sqlalchemy import Column, String, JSON, DateTime
from datetime import datetime
from app.models.database import Base


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(String, primary_key=True, index=True)
    agent_version = Column(String)
    raw_json = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
