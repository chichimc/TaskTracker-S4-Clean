from app.models.task import Task


class TaskService:
    def __init__(self, storage=None):
        if storage is None:
            raise ValueError("TaskService requires a repository (storage) via dependency injection.")
        self.storage = storage

    def get_all_tasks(self):
        return self.storage.get_all_tasks()

    def get_tasks(self):
        return self.get_all_tasks()

    def add_task(self, title, description=None):
        if not title or title is None:
            raise ValueError("Title is required")

        new_task_dict = self.storage.add_task(title, description)

        return new_task_dict

    def complete_task(self, task_id):
        updated_task_dict = self.storage.update_task(task_id, completed=True)

        if updated_task_dict:
            return updated_task_dict
        return None

    def delete_task(self, task_id):
        deleted_task_dict = self.storage.delete_task(task_id)

        return deleted_task_dict

    def clear_tasks(self):
        self.storage.clear_tasks()
