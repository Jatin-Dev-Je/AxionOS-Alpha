from __future__ import annotations

from datetime import datetime
import time
from typing import Any, Optional

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ....db.postgres import get_db
from ....models.task import Task, TaskStatus
from ....core.auth import get_current_user
from ....models.user import User
from ....worker.tasks import execute_task


router = APIRouter()


class CreateTaskRequest(BaseModel):
	type: str
	payload: Optional[dict] = None


class TaskOut(BaseModel):
	id: int
	type: str
	status: str
	payload: Optional[dict] = None
	result: Optional[dict] = None
	error: Optional[str] = None
	created_at: datetime
	started_at: Optional[datetime] = None
	finished_at: Optional[datetime] = None

	class Config:
		from_attributes = True


def _execute_task(db: Session, task_id: int) -> None:
	task: Task | None = db.query(Task).filter(Task.id == task_id).first()
	if not task:
		return
	task.status = TaskStatus.RUNNING
	task.started_at = datetime.utcnow()
	db.add(task)
	db.commit()

	try:
		# Simulate work based on task.type; stub for now
		if task.type == "knowledge_query":
			# pretend to run retrieval
			time.sleep(1)
			task.result = {
				"answer": "This is a stubbed knowledge answer.",
				"sources": [],
			}
		else:
			# generic echo
			time.sleep(0.5)
			task.result = {"echo": task.payload or {}}

		task.status = TaskStatus.SUCCEEDED
		task.finished_at = datetime.utcnow()
		db.add(task)
		db.commit()
	except Exception as e:
		task.status = TaskStatus.FAILED
		task.error = str(e)
		task.finished_at = datetime.utcnow()
		db.add(task)
		db.commit()


@router.post("/", response_model=TaskOut, status_code=status.HTTP_202_ACCEPTED)
def create_task(
	payload: CreateTaskRequest,
	background: BackgroundTasks,
	db: Session = Depends(get_db),
	current_user: User = Depends(get_current_user),
):
	task = Task(type=payload.type, payload=payload.payload or {}, user_email=current_user.email)
	db.add(task)
	db.commit()
	db.refresh(task)
	# Enqueue Celery task
	try:
		execute_task.delay(task.id)
	except Exception:
		# Fallback to in-process if Celery not running
		background.add_task(_execute_task, db, task.id)
	return task


@router.get("/{task_id}", response_model=TaskOut)
def get_task(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
	task = db.query(Task).filter(Task.id == task_id).first()
	if not task:
		raise HTTPException(status_code=404, detail="Task not found")
	if task.user_email and task.user_email != current_user.email:
		raise HTTPException(status_code=403, detail="Forbidden")
	return task

