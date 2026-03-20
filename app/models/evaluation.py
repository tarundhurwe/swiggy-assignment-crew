from sqlalchemy import Column, String, Float, DateTime
from datetime import datetime
from app.models.database import Base


class Evaluation(Base):
    __tablename__ = "evaluations"

    id = Column(String, primary_key=True, index=True)
    conversation_id = Column(String)
    overall_score = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
