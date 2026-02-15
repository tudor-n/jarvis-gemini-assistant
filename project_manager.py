from database import Database

class ProjectManager:  
    
    def __init__(self):
        self.db = Database()
        print("Project Manager initialized.")
    
    def create_project(self, name:  str, description: str = "", category: str = "") -> int:
        project_id = self. db.add_project(name, description, category)
        print(f"Project '{name}' created with ID: {project_id}")
        return project_id
    
    def list_projects(self) -> list:
        return self.db.get_all_projects()
    
    def get_project(self, name: str):
        return self.db.get_project_by_name(name)
    
    def create_task(self, project_id: int, task: str, priority: str = "medium") -> int:
        task_id = self.db. add_todo(project_id, task, priority)
        print(f"Task '{task}' created with ID: {task_id}")
        return task_id
    
    def list_tasks(self, project_id: int) -> list:
        return self. db.get_todos_for_project(project_id)
    
    def complete_task(self, task_id: int):
        self.db.complete_todo(task_id)
        print(f"Task {task_id} marked as completed.")
    
    def add_characteristic(self, project_id: int, key: str, value: str):
        self.db. add_characteristic(project_id, key, value)
        print(f"Added characteristic:  {key} = {value}")
    
    def get_characteristics(self, project_id:  int) -> list:
        return self. db.get_characteristics(project_id)
    
    def delete_project(self, project_id: int):
        self.db.remove_project(project_id)
        print(f"Project {project_id} has been deleted.")

    def delete_task(self, task_id: int):
        self.db.remove_task(task_id)
        print(f"Task {task_id} has been deleted.")

    def add_description(self, project_id: int, description: str):
        self.db.update_project_description(project_id, description)
        print(f"Updated project {project_id} description.")

    def update_task_priority(self, task_id: int, priority: str):
        self.db.update_task_priority(task_id, priority)
        print(f"Updated task {task_id} priority to {priority}.")

    def add_category(self, project_id: int, category: str):
        self.db.update_project_category(project_id, category)
        print(f"Updated project {project_id} category to {category}.")

    def delete_characteristic(self, project_id: int, key: str):
        self.db.remove_characteristic(project_id, key)
        print(f"Deleted characteristic '{key}' from project {project_id}.")

    def add_status_update(self, project_id: int, status: str):
        self.db.update_project_status(project_id, status)
        print(f"Updated project {project_id} status to {status}.")