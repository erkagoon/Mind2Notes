from models.BaseDB import BaseDB
import sqlite3
import os

class CategoriesDB(BaseDB):
    def __init__(self, db_name):
        # Obtenez le chemin du répertoire où se trouve ce fichier
        dir_path = os.path.dirname(os.path.abspath(__file__))
        # Créez le chemin complet vers la base de données
        full_db_path = os.path.join(dir_path, db_name)

        super().__init__(full_db_path)
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            project_id INTEGER,
            FOREIGN KEY (project_id) REFERENCES projects(id)
        )
        ''')
        self.conn.commit()

    def insert(self, name, project_id, description=None):
        try:
            self.cursor.execute("INSERT INTO categories (name, project_id, description) VALUES (?, ?, ?)", (name, project_id, description))
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Erreur lors de l'insertion: {e}")

    def delete(self, id):
        try:
            self.cursor.execute("DELETE FROM categories WHERE id=?", (id,))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Erreur lors de la suppression: {e}")

    def update(self, id, name=None, description=None, project_id=None):
        try:
            updates = []
            parameters = []
            if name:
                updates.append("name=?")
                parameters.append(name)
            if description:
                updates.append("description=?")
                parameters.append(description)
            if project_id:
                updates.append("project_id=?")
                parameters.append(project_id)
            
            if updates:
                parameters.append(id)
                self.cursor.execute(f"UPDATE categories SET {', '.join(updates)} WHERE id=?", tuple(parameters))
                self.conn.commit()
        except sqlite3.Error as e:
            print(f"Erreur lors de la mise à jour: {e}")


    def fetch_all(self):
        self.cursor.execute("SELECT * FROM categories")
        return self.cursor.fetchall()
    
    def fetch_by_project_id(self, project_id):
        self.cursor.execute("SELECT * FROM categories WHERE project_id=?", (project_id,))
        return self.cursor.fetchall()
