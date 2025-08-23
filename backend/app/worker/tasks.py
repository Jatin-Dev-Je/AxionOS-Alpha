from __future__ import annotations

from datetime import datetime
from sqlalchemy.orm import Session

from .celery_app import celery_app
from ..db.postgres import SessionLocal
from ..models.task import Task, TaskStatus


@celery_app.task(name="axionos.execute_task")
def execute_task(task_id: int) -> None:
    db: Session = SessionLocal()
    try:
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            return
        task.status = TaskStatus.RUNNING
        task.started_at = datetime.utcnow()
        db.add(task)
        db.commit()

        # TODO: branch by task.type; for now implement a stub
        if task.type == "knowledge_query":
            task.result = {
                "answer": "This is a Celery-executed stubbed knowledge answer.",
                "sources": [],
            }
        else:
            task.result = {"echo": task.payload or {}}

        task.status = TaskStatus.SUCCEEDED
        task.finished_at = datetime.utcnow()
        db.add(task)
        db.commit()
    except Exception as e:
        # best-effort failure update
        try:
            task = db.query(Task).filter(Task.id == task_id).first()
            if task:
                task.status = TaskStatus.FAILED
                task.error = str(e)
                task.finished_at = datetime.utcnow()
                db.add(task)
                db.commit()
        finally:
            pass
    finally:
        db.close()
