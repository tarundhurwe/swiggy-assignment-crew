from sqlalchemy import Column, String, Float, DateTime, JSON
from datetime import datetime
from app.models.database import Base


class Evaluation(Base):
    __tablename__ = "evaluations"

    id = Column(String, primary_key=True, index=True)
    conversation_id = Column(String, index=True)

    overall_score = Column(Float)

    scores = Column(JSON)
    tool_evaluation = Column(JSON)
    issues = Column(JSON)
    suggestions = Column(JSON)
    meta_evaluation = Column(JSON)

    created_at = Column(DateTime, default=datetime.utcnow)
