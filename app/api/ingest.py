from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.conversation_schema import ConversationSchema
from app.models.database import SessionLocal
from app.models.conversation import Conversation
from worker.tasks import process_conversation

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/ingest")
def ingest_conversation(payload: ConversationSchema, db: Session = Depends(get_db)):

    conversation = Conversation(
        id=payload.conversation_id,
        agent_version=payload.agent_version,
        raw_json=payload.dict(),
    )

    db.add(conversation)
    db.commit()

    # Send to Celery
    process_conversation.delay(payload.conversation_id)

    return {"status": "ingested", "conversation_id": payload.conversation_id}
