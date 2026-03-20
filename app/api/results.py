from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.database import SessionLocal
from app.models.evaluation import Evaluation

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/results/{conversation_id}")
def get_results(conversation_id: str, db: Session = Depends(get_db)):
    result = db.query(Evaluation).filter_by(conversation_id=conversation_id).first()

    if not result:
        return {"error": "Not found"}

    return {
        "conversation_id": conversation_id,
        "scores": result.scores,
        "tool_evaluation": result.tool_evaluation,
        "issues": result.issues,
        "suggestions": result.suggestions,
        "meta_evaluation": result.meta_evaluation,
    }
