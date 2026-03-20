from fastapi import FastAPI
from app.models.database import Base, engine
from app.models import conversation, evaluation
from app.api import ingest
from app.api import results, suggestions

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Evaluation Pipeline",
    description="Automated evaluation system for AI agents",
    version="1.0.0",
)


@app.get("/")
def health_check():
    return {"status": "ok", "message": "System is operational"}


app.include_router(ingest.router)
app.include_router(results.router)
app.include_router(suggestions.router)
