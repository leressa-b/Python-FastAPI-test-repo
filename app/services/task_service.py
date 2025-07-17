import json
import re
import time
from typing import Any, Dict, List, Optional
from app.models.task import Task, TaskFilter

class TaskProcessor:
    """Processes and validates task data with various transformations."""
    
    def __init__(self):
        self.valid_statuses = ['pending', 'running', 'completed', 'failed']
        self.email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    
    def process_task_batch(self, tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Process a batch of tasks with validation and transformation."""
        results = {
            'valid_tasks': [],
            'invalid_tasks': [],
            'user_emails': [],
            'task_summary': {}
        }
        

        for task in tasks:

            if task.get('status') not in self.valid_statuses:
                results['invalid_tasks'].append(task)
                continue
            

            processed_task = self._transform_task(task)
            
    
            if 'user_email' in task:
                if self.email_pattern.match(task['user_email']):
                    results['user_emails'].append(task['user_email'])
            
            results['valid_tasks'].append(processed_task)
        
 
        for task in results['valid_tasks']:
            status = task['status']
            if status in results['task_summary']:
                results['task_summary'][status] += 1
            else:
                results['task_summary'][status] = 1
        

        results['valid_tasks'].sort(key=lambda x: x.get('priority', 0), reverse=True)
        
        return results
    
    def _transform_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Transform task data with various processing steps."""
        transformed = json.loads(json.dumps(task))
        

        transformed['processed_at'] = time.time()
        

        if 'name' in transformed:
            transformed['name'] = transformed['name'].strip().lower()
        
  
        complexity = 0
        if 'description' in transformed:
            complexity += len(transformed['description']) // 100
        if 'requirements' in transformed:
            complexity += len(transformed['requirements'])
        transformed['complexity_score'] = complexity
        
        return transformed
    
    def find_tasks_by_user(self, tasks: List[Dict[str, Any]], user_email: str) -> List[Dict[str, Any]]:
        """Find all tasks assigned to a specific user."""
        user_tasks = []
        for task in tasks:
            if task.get('user_email') == user_email:
                user_tasks.append(task)
        return user_tasks
    
    def get_high_priority_tasks(self, tasks: List[Dict[str, Any]], min_priority: int = 8) -> List[Dict[str, Any]]:
        """Get tasks with priority above threshold."""
        high_priority = []
        for task in tasks:
            if task.get('priority', 0) >= min_priority:
                high_priority.append(task)
        return high_priority
    
    def calculate_user_workload(self, tasks: List[Dict[str, Any]]) -> Dict[str, int]:
        """Calculate workload distribution across users."""
        workload = {}
        for task in tasks:
            user = task.get('user_email', 'unassigned')
            if user in workload:
                workload[user] += 1
            else:
                workload[user] = 1
        return workload

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