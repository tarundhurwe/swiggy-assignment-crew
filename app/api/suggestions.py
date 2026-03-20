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


@router.get("/suggestions")
def get_suggestions(db: Session = Depends(get_db)):
    results = db.query(Evaluation).all()

    all_suggestions = []

    for r in results:
        if r.suggestions:
            print(r.suggestions)
            all_suggestions.extend(r.suggestions)

    return {"suggestions": all_suggestions}
