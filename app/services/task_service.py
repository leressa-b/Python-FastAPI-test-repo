from typing import List, Optional
from app.models.task import Task, TaskFilter
import time

class SmartCache:
    def __init__(self, max_size=100):
        self._cache = {}
        self._access_times = {}
        self._max_size = max_size
    
    def get(self, key):
        if key in self._cache:
            self._access_times[key] = time.time()
            return self._cache[key]
        return None
    
    def put(self, key, value):
        current_time = time.time()
        
        if len(self._cache) >= self._max_size:
            oldest_key = min(self._access_times.keys(), 
                           key=lambda k: self._access_times[k])
            del self._cache[oldest_key]
            del self._access_times[oldest_key]
        
        self._cache[key] = value
        self._access_times[key] = current_time


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