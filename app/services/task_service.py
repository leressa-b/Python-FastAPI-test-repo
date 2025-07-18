import datetime
import json
import logging
from typing import List, Optional
from app.db.database import TaskDB
from app.models.task import Task, TaskFilter
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

class TaskReviewService:
    def __init__(self, db: Session):
        self.db = db

    def create_review_task(self, user_id: int, title: str, description: str, rating: int, tags: Optional[List[str]] = None) -> TaskDB:

        try:
            suspicious = self._is_suspicious(description, rating)
            tags = tags or []

            task = TaskDB(
                title=title,
                description=description,
                priority="high" if suspicious else "medium",
                status="review_pending" if suspicious else "todo",
                tags=json.dumps(tags + (["suspicious"] if suspicious else [])),
                owner_id=user_id,
                estimated_hours=1,
                actual_hours=None
            )
            self.db.add(task)
            self.db.commit()
            self.db.refresh(task)
            return task
        except SQLAlchemyError as e:
            self.db.rollback()
            logging.error(f"Failed to create review task: {e}")
            raise

    def get_filtered_reviews(
        self,
        user_id: int,
        min_rating: int = 1,
        max_rating: int = 5,
        suspicious_only: bool = False,
        date_from: Optional[datetime.datetime] = None,
        date_to: Optional[datetime.datetime] = None
    ) -> List[TaskDB]:
 
        try:
            query = self.db.query(TaskDB).filter(TaskDB.owner_id == user_id)

            if suspicious_only:
                query = query.filter(TaskDB.tags.like("%suspicious%"))

            if date_from:
                query = query.filter(TaskDB.created_at >= date_from)
            if date_to:
                query = query.filter(TaskDB.created_at <= date_to)

            results = query.order_by(TaskDB.created_at.desc()).all()
            return results
        except SQLAlchemyError as e:
            logging.error(f"Error fetching filtered reviews: {e}")
            return []

    def _is_suspicious(self, description: str, rating: int) -> bool:

        lower_text = description.lower()
        if rating == 5 and any(phrase in lower_text for phrase in ["worst", "never again", "terrible"]):
            return True
        if rating <= 2 and "best" in lower_text:
            return True
        if len(description.strip()) < 10:
            return True
        return False

class TaskService:
    def __init__(self, db):
        self.db = db

    def get_tasks(
        self,
        skip: int = 0,
        limit: int = 100,
        filter_params: Optional[TaskFilter] = None,
        user_id: Optional[int] = None
    ) -> List[Task]:
        return []