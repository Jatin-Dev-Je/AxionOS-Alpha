from __future__ import annotations

from datetime import datetime
from sqlalchemy.orm import Session

from .celery_app import celery_app
from ..db.postgres import SessionLocal
from ..models.task import Task, TaskStatus
from ..services.llm import llm_chat
from ..db.weaviate import weaviate_bm25_search


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
            q = ""
            if isinstance(task.payload, dict):
                q = str(task.payload.get("q", "")).strip()
            # Retrieve context from Weaviate (optional)
            context_snippets = []
            docs = weaviate_bm25_search(class_name="Document", query=q, limit=5) if q else []
            for d in docs:
                text = d.get("text")
                if text:
                    context_snippets.append(text)
            context_text = "\n\n".join(context_snippets[:3])
            messages = [
                {"role": "system", "content": "You are AxionOS Knowledge Agent. Use the provided context if relevant."},
                {"role": "system", "content": f"Context:\n{context_text}"},
                {"role": "user", "content": q or "What do you know?"},
            ]
            answer = llm_chat(messages)
            task.result = {"answer": answer, "sources": [{"type": "weaviate", "count": len(docs)}]}
        else:
            if task.type == "llm_chat":
                messages = task.payload.get("messages") if isinstance(task.payload, dict) else None
                if not messages:
                    messages = [{"role": "user", "content": str(task.payload)}]
                answer = llm_chat(messages)
                task.result = {"answer": answer}
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
