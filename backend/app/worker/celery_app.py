from __future__ import annotations

from celery import Celery
from ..config import REDIS_URL


celery_app = Celery(
    "axionos",
    broker=REDIS_URL,
    backend=REDIS_URL,
)

# Reasonable defaults
celery_app.conf.update(
    task_acks_late=True,
    worker_max_tasks_per_child=100,
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
)
