from celery import Celery
import os

REDIS_URL = os.getenv("REDIS_URL", "redis://127.0.0.1:6379/0")

celery = Celery(
    "yield_curve_creator",
    broker=REDIS_URL,
    backend=REDIS_URL,
)

# Opciones opcionales
celery.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="America/Argentina/Buenos_Aires",
    enable_utc=True,
)
from celery import Celery
import os

CELERY_BROKER_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
CELERY_RESULT_BACKEND = CELERY_BROKER_URL

celery = Celery(
    "yield_curve_creator",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
    include=["app.tasks"]
)
