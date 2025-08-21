from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import String, Integer, DateTime, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import JSON

from ..db.postgres import Base


class TaskStatus(str):
	QUEUED = "queued"
	RUNNING = "running"
	SUCCEEDED = "succeeded"
	FAILED = "failed"


class Task(Base):
	__tablename__ = "tasks"

	id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
	# e.g., "knowledge_query" or other task kinds
	type: Mapped[str] = mapped_column(String(64), index=True)
	status: Mapped[str] = mapped_column(String(16), default=TaskStatus.QUEUED, index=True)

	# Optional association to a user (not enforced with FK for now to keep quick setup)
	user_email: Mapped[Optional[str]] = mapped_column(String(320), nullable=True, index=True)

	# JSON payload and results
	payload: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
	result: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
	error: Mapped[Optional[str]] = mapped_column(String, nullable=True)

	created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
	started_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
	finished_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

