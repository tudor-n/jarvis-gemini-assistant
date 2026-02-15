import sqlite3
import os
import sys
from datetime import datetime
from typing import Optional

class Database:
    def __init__(self, db_relative_path: str = "data/projects.db"):
        if getattr(sys, 'frozen', False):
            base_dir = os.path.dirname(sys.executable)
        else:
            base_dir = os.path.dirname(os.path.abspath(__file__))
        
        self.db_path = os.path.join(base_dir, db_relative_path)
        
        db_dir = os.path.dirname(self.db_path)
        if not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)
            
        self.init_database()

    def get_connection(self):
        try:
            conn = sqlite3.connect(self.db_path, timeout=10)
            return conn
        except sqlite3.OperationalError as e:
            print(f"Database connection error: {e}")
            raise
    
    def init_database(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL UNIQUE,
                description TEXT,
                status TEXT DEFAULT 'active',
                category TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS characteristics (
                id INTEGER PRIMARY KEY,
                project_id INTEGER,
                key TEXT NOT NULL,
                value TEXT,
                FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY,
                project_id INTEGER,
                task TEXT NOT NULL,
                priority TEXT DEFAULT 'medium',
                status TEXT DEFAULT 'pending',
                due_date DATE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP,
                FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
            )
        ''')
        conn.commit()
        conn.close()
        print(f"SYSTEM | Database linked at: {self.db_path}")

    def add_project(self, name: str, description: str = "", category: str = "") -> int:
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO projects (name, description, category) VALUES (?,?,?)",
                (name, description, category)
            )
            conn.commit()
            project_id = cursor.lastrowid
            return project_id
        except sqlite3.OperationalError as e:
            print(f"Database operation error (add_project): {e}")
            raise
        finally:
            try: conn.close()
            except: pass
    
    def get_all_projects(self) -> list:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM projects WHERE status = 'active'")
        projects = cursor.fetchall()
        conn.close()
        return projects
    
    def get_project_by_name(self, name: str):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM projects WHERE name = ?", (name,))
        project = cursor.fetchone()
        conn.close()
        return project
    
    def add_todo(self, project_id: int, task: str, priority: str = "medium") -> int:
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO todos(project_id, task, priority) VALUES (?,?,?)",
                (project_id, task, priority)
            )
            conn.commit()
            todo_id = cursor.lastrowid
            return todo_id
        except sqlite3.OperationalError as e:
            print(f"Database operation error (add_todo): {e}")
            raise
        finally:
            try: conn.close()
            except: pass
    
    def get_todos_for_project(self, project_id: int) -> list:
        conn=self.get_connection()
        cursor=conn.cursor()
        cursor.execute(
            "SELECT * FROM todos WHERE project_id = ? AND status = 'pending' ",
            (project_id,)
        )
        todos = cursor.fetchall()
        conn.close()
        return todos
    
    def complete_todo(self, todo_id: int):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE todos SET status = 'completed', completed_at = ? WHERE id = ?",
            (datetime.now(), todo_id)
        )
        conn.commit()
        conn.close()
    
    def add_characteristic(self, project_id: int, key: str, value: str):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO characteristics (project_id, key, value) VALUES (?,?,?)",
            (project_id, key, value)
        )
        conn.commit()
        conn.close()
    
    def get_characteristics(self, project_id: int) -> list:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT key, value FROM characteristics WHERE project_id=?",
            (project_id,)
        )
        chars = cursor.fetchall()
        conn.close()
        return chars
    
    def remove_project(self, project_id: int):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM projects WHERE id = ?", (project_id,))
        conn.commit()
        conn.close()

    def remove_task(self, task_id: int):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM todos WHERE id = ?", (task_id,))
        conn.commit()
        conn.close()

    def update_project_description(self, project_id: int, description: str):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE projects SET description = ?, updated_at = ? WHERE id = ?",
            (description, datetime.now(), project_id)
        )
        conn.commit()
        conn.close()

    def update_task_priority(self, task_id: int, priority: str):  
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE todos SET priority = ? WHERE id = ?",
            (priority, task_id)
        )
        conn.commit()
        conn.close()

    def update_project_category(self, project_id: int, category: str):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE projects SET category = ?, updated_at = ? WHERE id = ?",
            (category, datetime.now(), project_id)
        )
        conn.commit()
        conn.close()

    def remove_characteristic(self, project_id: int, key: str):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM characteristics WHERE project_id = ? AND key = ?",
            (project_id, key)
        )
        conn.commit()
        conn.close()

    def update_project_status(self, project_id: int, status: str):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE projects SET status = ?, updated_at = ? WHERE id = ?",
            (status, datetime.now(), project_id)
        )
        conn.commit()
        conn.close()