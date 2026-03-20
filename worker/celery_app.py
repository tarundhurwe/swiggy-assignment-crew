from celery import Celery
from dotenv import load_dotenv

load_dotenv()

celery_app = Celery(
    "worker", broker="redis://redis:6379/0", backend="redis://redis:6379/0"
)

celery_app.conf.task_routes = {"worker.tasks.*": {"queue": "default"}}
