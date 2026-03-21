from celery import Celery
from dotenv import load_dotenv

load_dotenv()

celery_app = Celery(
    "worker", broker="redis://redis:6379/0", backend="redis://redis:6379/0"
)

# 🔥 REQUIRED
celery_app.autodiscover_tasks(["worker"])

# Optional but clean
celery_app.conf.update(task_default_queue="default")
