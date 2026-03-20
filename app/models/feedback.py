from sqlalchemy import Column, String, Integer, JSON, Float
from app.models.database import Base


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(String, primary_key=True)
    conversation_id = Column(String, index=True)

    user_rating = Column(Integer)
    ops_quality = Column(String)

    annotations = Column(JSON)  # raw annotator data

    agreement_score = Column(Float)
    final_label = Column(String)
