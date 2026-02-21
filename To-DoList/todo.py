from datetime import datetime

class Task:
    def __init__(self, title, description = '', task_id = None):
        self.id = task_id
        self.title = title
        self.description = description
        self.completed = False
        self.completed_at = None
    
    def mark_completed(self):
        self.completed = True
        self.completed_at = datetime.now()

    def mark_incomplete(self):
        self.completed = False
        self.completed_at = None

class TaskManager:
    def __init__(self):
        self.tasks = {}
        self.next_id = 1

    def add_task(self, title, description=''):
        task = Task(title, description, self.next_id)
        self.tasks[self.next_id] = task
        self.next_id += 1
        return task
    
    def get_task(self, task_id):
        return self.tasks.get(task_id)
    
    def get_all_tasks(self):
        return list(self.tasks.values())
    
    def update_task(self, task_id, title = None, description = None):
        task = self.get_task(task_id)
        if not task:
            return False
        if title:
            task.title = title
        if description:
            task.description = description
        return True
    
    def delete_task(self, task_id):
        if task_id in self.tasks:
            del self.tasks[task_id]
            return True
        return False

    def mark_completed(self, task_id):
        task = self.get_task(task_id)
        if task:
            task.mark_completed()
            return True
        return False
    
    def mark_incomplete(self, task_id):
        task = self.get_task(task_id)
        if task:
            task.mark_incomplete()
            return True
        return False
    
    


        